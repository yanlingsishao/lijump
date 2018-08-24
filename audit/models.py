from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class IDC(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Host(models.Model):
    """
    存储所有主机信息
    """
    hostname = models.CharField(max_length=64,unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=22)
    idc = models.ForeignKey("IDC")
    enabled = models.BooleanField(default=True)
    #host_users = models.ManyToManyField("HostUser")

    def __str__(self):
        return "%s-%s" %(self.hostname,self.ip_addr)


class HostGroup(models.Model):
    """
    主机组
    """
    name = models.CharField(max_length=64,unique=True)
    host_user_binds = models.ManyToManyField("HostUserBind")

    def __str__(self):
        return self.name


class HostUser(models.Model):
    """
    存储远程主机的用户信息
    """
    auth_type_choices = ((0,"ssh-password"),(1,"ssh-key"))
    auth_type = models.SmallIntegerField(choices=auth_type_choices)
    username = models.CharField(max_length=32)
    password = models.CharField(blank=True,null=True,max_length=128)

    def __str__(self):
        return "%s-%s-%s" %(self.get_auth_type_display(),self.username,self.password)

    class Meta:
        unique_together = ("username","password")


class Token(models.Model):
    host_user_bind = models.ForeignKey("HostUserBind")
    val = models.CharField(max_length=128)
    account = models.ForeignKey("Account")
    expire = models.IntegerField("超时时间(s)",default=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s-%s" %(self.host_user_bind,self.val)

    class Meta:
        unique_together = ("host_user_bind","val")


class HostUserBind(models.Model):
    host = models.ForeignKey("Host")
    host_user = models.ForeignKey("HostUser")

    def __str__(self):
        return "%s-%s" % (self.host, self.host_user)

    class Meta:
        unique_together = ("host","host_user")


class SessionLog(models.Model):
    account = models.ForeignKey("Account")
    host_user_binds = models.ForeignKey("HostUserBind")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return "%s-%s" %(self.account, self.host_user_binds)


class AuditLog(models.Model):
    """审计日志"""
    session = models.ForeignKey("SessionLog")
    cmd = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s-%s" %(self.session,self.cmd)


class Account(models.Model):
    """
    堡垒机账户
    """
    user = models.OneToOneField(User)
    name = models.CharField(max_length=64)
    host_user_binds = models.ManyToManyField("HostUserBind", blank=True)
    host_groups = models.ManyToManyField("HostGroup", blank=True)
    slb = models.ManyToManyField("Slb",blank=True)


class Slb(models.Model):
    group_name = models.CharField(max_length=64)
    url = models.URLField(max_length=2048)
    method = models.CharField(max_length=32)
    W = models.CharField(max_length=64,blank=True)
    n = models.CharField(max_length=64,blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return "%s-%s" %(self.group_name,self.url)


class AccessLog(models.Model):
    log_type_choices = (
        ("0", "DEBUG"),
        ("1", "INFO"),
        ("2", "WARNING"),
        ("3", "ERROR"),
        ("4", "CRITICAL"),
    )
    user = models.ForeignKey(User,blank=True,null=True,verbose_name="产生日志的用户",on_delete=models.SET_NULL)
    log_type = models.CharField(max_length=32,choices=log_type_choices,default=1,verbose_name="日志类型")
    content = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True,verbose_name="记录时间")

    def __str__(self):
        return "%s  记录时间 <%s>" %(self.user.username,self.c_time)

    class Meta:
        verbose_name = "堡垒机用户行为日志"
        verbose_name_plural = "堡垒机用户行为日志"
        ordering = ["-c_time"]


class Task(models.Model):
    """存储任务信息"""
    def __str__(self):
        return "%s-%s-%s" %(self.id,self.get_task_type_display(),self.content)
    task_type_choices = ((0,"cmd"),(1,"file_transfer"))
    cmd_type_choices = ((0,"sh"),(1,"python"))
    task_type = models.SmallIntegerField(choices=task_type_choices)
    cmd_type = models.SmallIntegerField(choices=cmd_type_choices)
    # host_user_binds = models.ManyToManyField("HostUserBind")
    content = models.TextField("任务内容")
    timeout = models.IntegerField("任务超时",default=300)
    account = models.ForeignKey("Account")
    date = models.DateTimeField(auto_now_add=True)




class TaskLog(models.Model):
    task = models.ForeignKey("Task")
    host_user_bind = models.ForeignKey("HostUserBind")
    result = models.TextField(default="init...")
    date = models.DateTimeField(auto_now_add=True)
    status_choices = ((0,"成功"),(1,"失败"),(2,"超时"),(3,"初始化"))
    status = models.SmallIntegerField(choices=status_choices)

    class Meta:
        unique_together = ("task","host_user_bind")


class EnvironUrl(models.Model):
    url = models.URLField(max_length=64, verbose_name="环境网址")

    def __str__(self):
        return self.url


class Environ(models.Model):
    """环境
    name,group_name,ex,url
    """
    name = models.CharField(max_length=64,verbose_name="环境名称")
    group_name = models.CharField(max_length=64,verbose_name="环境组")
    ex = models.CharField(max_length=32,verbose_name="环境参数")
    url = models.ManyToManyField("EnvironUrl",verbose_name="网址")

    def __str__(self):
        return "%s-%s" % (self.group_name,self.name)


class PublishCmd(models.Model):
    """脚本"""
    log_type_choices = (
        ("0", "SHELL"),
        ("1", "PYTHON"),
    )
    name = models.CharField(max_length=64,verbose_name="脚本名称")
    cmd_text = models.CharField(max_length=64,choices=log_type_choices,verbose_name="脚本内容")
    cmd_ars = models.CharField(max_length=64,verbose_name="脚本参数")

    def __str__(self):
        return "%s-%s" % (self.name, self.cmd_type)


class App(models.Model):
    """app"""
    name = models.CharField(max_length=64,verbose_name="app名称")
    host_user_binds = models.ForeignKey("HostUserBind",verbose_name="主机")
    environ = models.ForeignKey(Environ,related_name="app_environ",verbose_name="环境")
    app_url = models.URLField(max_length=64,verbose_name="app网址")
    publish_cmd = models.ForeignKey("PublishCmd",verbose_name="脚本")
    tar_name = models.CharField(max_length=64,verbose_name="程序包名称")
    tar_file = models.CharField(max_length=64,verbose_name="程序包路径")
    backup_file = models.CharField(max_length=64,verbose_name="备份路径")

    def __str__(self):
        return "%s-%s" % (self.environ,self.name)











