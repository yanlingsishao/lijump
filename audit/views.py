import json,os
from django.shortcuts import render, redirect ,HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .server import WSSHBridge
from .server import add_log
from audit import models
import random,string
import datetime
from audit import task_handler
from django import conf
import zipfile
from wsgiref.util import FileWrapper #from django.core.servers.basehttp import FileWrapper


# Create your views here.

@login_required
def index(request):
    return redirect("/navi/")


def acc_login(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect(request.GET.get("next") or "/")
        else:
            error = "Wrong username or password !"
    return render(request, "login.html",{"error":error})


@login_required
def acc_logout(request):
    logout(request)
    return redirect("/login/")


@login_required
def host_list(request):
    return render(request, "hostlist.html")


@login_required
def slb_list(request):
    slb = models.Slb.objects.all()
    return render(request,"slblist.html",locals())


@login_required
def get_host_list(request):
    gid = request.GET.get("gid")
    if gid:
        if gid == "-1": # 未分组
            host_list = request.user.account.host_user_binds.all()
            print(host_list)
        else:
            group_obj = request.user.account.host_groups.get(id=gid)
            host_list = group_obj.host_user_binds.all()
        data = json.dumps(list(host_list.values("id","host__hostname","host__ip_addr",
                                "host__port","host_user__username","host__idc__name")))
        return HttpResponse(data)


@login_required
def get_token(request):
    """
    生产token并返回
    :param request:
    :return:
    """
    print(request.POST)
    bind_host_id = request.POST.get("bind_host_id")


@login_required
def connect_host(request,user_bind_host_id):
    # 如果当前请求不是websocket方式，则退出
    if not request.environ.get("wsgi.websocket"):
        return HttpResponse("错误，非websocket请求")
    try:
        remote_user_bind_host = request.user.account.host_user_binds.get(id=user_bind_host_id)
    except Exception as e:
        message = "无效的账户，或者无权访问" + str(e)
        add_log(request.user,message,log_type="2")
        return HttpResponse("请求主机异常"+message)
    username = remote_user_bind_host.host.ip_addr
    print(username,request.META.get("REMOTE_ADDR"))
    message = "来自{remote}的请求 尝试连接 -> {username}@{hostname} <{ip}:{port}>".format(
        remote = request.META.get("REMOTE_ADDR"),# 请求地址
        username = remote_user_bind_host.host_user.username,
        hostname = remote_user_bind_host.host.hostname,
        ip = remote_user_bind_host.host.ip_addr,
        port = remote_user_bind_host.host.port,
    )
    add_log(request.user, message, log_type="0")
    bridge = WSSHBridge(request.environ.get("wsgi.websocket"),request.user)
    try:
        bridge.open(
            hostname=remote_user_bind_host.host.ip_addr,
            port=remote_user_bind_host.host.port,
            username=remote_user_bind_host.host_user.username,
            password=remote_user_bind_host.host_user.password,
                    )
    except Exception as e:
        message = "尝试连接{0}的过程中发生错误 ：{1}\n".format(
            remote_user_bind_host.host.hostname,e
        )
        print(message)
        add_log(request.user, message, log_type="2")
        return HttpResponse("错误！无法建立SSH连接！")
    print(request.GET.get("copytext"))
    bridge.shell()

    # if request.method == "POST":
    #     bridge._forword_copybound("123")
    request.environ.get("wsgi.websocket").close()
    print("用户断开连接....")
    message = "来自{remote}的请求 断开连接 -> {username}@{hostname} <{ip}:{port}>".format(
        remote = request.META.get("REMOTE_ADDR"),# 请求地址
        username = remote_user_bind_host.host_user.username,
        hostname = remote_user_bind_host.host.hostname,
        ip = remote_user_bind_host.host.ip_addr,
        port = remote_user_bind_host.host.port,
    )
    add_log(request.user, message, log_type="0")
    return HttpResponse("200,ok")

@login_required
def get_log(request):
    # 如果有权限管理
    # if request.user.is_superuser:
    #     logs = models.AccessLog.objects.all()
    #     return render(request,"ssh_log.html",locals())
    # else:
    #     redirect("/")
    logs = models.AccessLog.objects.all()
    return render(request, "ssh_log.html", locals())

@login_required
def multi_cmd(request):

    return render(request, "multi_cmd_bak.html")


@login_required
def multi_file_transfer(request):
    random_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
    #return render(request,'multi_file_transfer.html',{'random_str':random_str})
    return render(request,'multi_file_transfer.html',locals())


@login_required
@csrf_exempt
def task_file_upload(request):
    random_str = request.GET.get('random_str')
    upload_to = "%s/%s/%s" %(conf.settings.FILE_UPLOADS,request.user.account.id,random_str)
    if not os.path.isdir(upload_to):
        os.makedirs(upload_to,exist_ok=True)

    file_obj = request.FILES.get('file')
    f = open("%s/%s"%(upload_to,file_obj.name),'wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()
    print(file_obj)

    return HttpResponse(json.dumps({'status':0}))


def send_zipfile(request,task_id,file_path):
    """
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory. A similar approach can
    be used for large dynamic PDF files.
    """
    zip_file_name = 'task_id_%s_files' % task_id
    archive = zipfile.ZipFile(zip_file_name , 'w', zipfile.ZIP_DEFLATED)
    file_list = os.listdir(file_path)
    for filename in file_list:
        archive.write('%s/%s' %(file_path,filename),arcname=filename)
    archive.close()
    wrapper = FileWrapper(open(zip_file_name,'rb'))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % zip_file_name
    response['Content-Length'] = os.path.getsize(zip_file_name)
    #temp.seek(0)
    return response


@login_required
def task_file_download(request):
    task_id = request.GET.get('task_id')
    print(task_id)
    task_file_path = "%s/%s"%( conf.settings.FILE_DOWNLOADS,task_id)
    return send_zipfile(request,task_id,task_file_path)


@login_required
def multitask(request):
    lange_id = request.POST.get("lange_id")
    cmd = request.POST.get("cmd")
    random_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
    print(cmd)

    print(lange_id)
    task_obj = task_handler.Task(request)
    if task_obj.is_valid():
        task_obj = task_obj.run(random_str)
        print(task_obj)
        return HttpResponse(json.dumps({'task_id':task_obj.id,'timeout':task_obj.timeout}))
    return HttpResponse(json.dumps(task_obj.errors))


@login_required
def multitask_result(request):
    task_id = request.GET.get("task_id")
    task_obj = models.Task.objects.get(id=task_id)

    results = list(task_obj.tasklog_set.values("id","status",
                                "host_user_bind__host__hostname",
                                "host_user_bind__host__ip_addr",
                                "result"))
    return HttpResponse(json.dumps(results))


def vue_study(request):
    return render(request,"1.html")

@login_required
def upload_host(request):
    import os
    if request.method == 'POST':
        random_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
        file_obj = request.FILES.get('file')
        upload_to = os.path.join(conf.settings.FILE_UPLOADS, str(request.user.account.id), random_str)
        des_id = request.POST.get("des_id")
        upload_file = request.POST.get("upload_file")
        print(des_id,upload_file)
        if not os.path.isdir(upload_to):
            os.makedirs(upload_to, exist_ok=True)
        f = open(os.path.join(upload_to,file_obj.name), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        remote_user_bind_host = request.user.account.host_user_binds.get(id=des_id)
        hostname = remote_user_bind_host.host.ip_addr
        port = remote_user_bind_host.host.port
        username = remote_user_bind_host.host_user.username
        password = remote_user_bind_host.host_user.password
        import paramiko
        try:
            t = paramiko.Transport((hostname, port))
            t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(t)
            print(os.path.join(upload_to, file_obj.name))
            sftp.put(localpath=os.path.join(upload_to, file_obj.name), remotepath="%s/%s"%(upload_file,file_obj.name))
            t.close()
            print("okok")
        except Exception as e:
            print(e)

        return HttpResponse('OK')


from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

scheduler.start()


def time_task(task):
    print("I'm a test job!")

scheduler.add_job(time_task, "cron", id=task.name, hour=hour, minute=minute, second=0, misfire_grace_time=30,kwargs={"task": task})
