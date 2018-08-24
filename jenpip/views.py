from audit.models import Environ,PublishCmd,App,EnvironUrl
from django.shortcuts import render,HttpResponse
from jenpip.forms import environ_form
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    all_env = Environ.objects.all()
    if request.method == "POST":
        n_form = environ_form(request.POST)
        print(n_form)
        if n_form.is_valid():
            n_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "environ/index.html", locals())
    else:
        display_control = "none"
        n_form = environ_form()
        print(n_form)
        return render(request, "environ/index.html", locals())


def add(request):
    if request.method == "POST":
        n_form = environ_form(request.POST)
        print(n_form)
        if n_form.is_valid():
            n_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "environ/add.html", locals())
    else:
        display_control = "none"
        n_form = environ_form()
        return render(request, "environ/add.html", locals())


def edit(request):
    if request.method == 'GET':
        item = request.GET.get("id")
        obj = Environ.objects.get(id=item)
        all_url = EnvironUrl.objects.all()

        url = obj.url.all()
        print(url)
    return render(request, "environ/edit.html", locals())


def update(request):
    if request.method == 'GET':
        status = 2
        env_url = "123"
        all_env = Environ.objects.all()
        for i in all_env:
            env_url = i.url.all()
        return render(request, "environ/update.html", locals())
    else:
        status = 1
        env_url = "123"
        all_env = Environ.objects.all()
        for i in all_env:
            env_url = i.url.all()
        url_list = []
        mu_url = request.POST.getlist('mu_url')
        for url_id in mu_url:
            url_list.append(EnvironUrl.objects.get(id=url_id).url)
        wai_id = request.POST.get("wai")
        nei_id = request.POST.get("nei")
        wai_item = Environ.objects.get(id=wai_id)
        wai_ex = wai_item.ex
        nei_item = Environ.objects.get(id=nei_id)
        nei_ex = nei_item.ex
        for url in url_list:
            url = url + "sets/set"
            print(url)
            ui_status = get_request(url,**{"w":wai_ex,"n":nei_ex})
            print(ui_status.text)
        return render(request, "environ/update.html", locals())


def get_request(url,**kwargs):
    import requests
    ui = requests.get(url,params=kwargs)
    return ui


def test_lb_status(request):
    if request.method == 'GET':
        env_url = "123"
        all_env = Environ.objects.all()
        for i in all_env:
            env_url = i.url.all()
        import requests,json

        url_dic = {}
        url_list = ["http://10.5.0.204/sets/get",
                    "http://10.5.0.205/sets/get"]
        for url in url_list:
            ui = get_request(url)
            url_dic[url] = ui.text

    return render(request,"environ/update.html",locals())


def save(request):
    if request.method == 'POST':
        ids = request.POST.get('id')
        name = request.POST.get('name')
        group_name = request.POST.get('group_name')
        url = request.POST.getlist('all_url')
        ex = request.POST.get("ex")
        env_item = Environ.objects.get(id=ids)
        env_item.name = name
        env_item.group_name = group_name
        env_item.url = url
        env_item.ex = ex
        env_item.save()
        status = 1
    else:
        status = 2
    all_env = Environ.objects.all()
    return render(request, "environ/edit.html", locals())


def get_object(model, **kwargs):
    """
    use this function for query
    使用改封装函数查询数据库
    """
    for value in kwargs.values():
        if not value:
            return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object


def env_del(request):

    if request.method == 'POST':
        print(1)
        data = request.POST
        print(data)
        env_items = request.POST.getlist('id_list[]')
        print(env_items)
        if env_items:
            for n in env_items:
                Environ.objects.filter(id=n).delete()
    all_env = Environ.objects.all()
    return render(request, "environ/index.html", locals())
