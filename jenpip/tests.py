from django.test import TestCase

# Create your tests here.
# 灰度设置
    index
        环境      网址

    添加环境

        A 环境     网址      环境参数a
        B 环境     网址      环境参数b
        C 环境     网址      环境参数c

    切换环境


    测试当前环境

    url     w环境      n环境    切换
        外：环境   内：环境   方法    生成网址     切换

    当前环境




from django.db import models

class Environ(models):
    name = models.CharField(max_length=64,verbose_name="环境名称")
    group_name = models.CharField(max_length=64,verbose_name="环境组")
    ex = models.CharField(max_length=32,verbose_name="环境参数")
    url = models.URLField(max_length=64,verbose_name="环境网址")
    def __str__(self):
        return "%s-%s" % (self.group_name,self.name)


class App(models):
    name = models.CharField(max_length=64,verbose_name="app名称")
    host_user_binds = models.ForeignKey("HostUserBind")
    environ = models.ForeignKey(Environ,related_name="app_environ",verbose_name="环境")
    app_url = models.URLField(max_length=64,verbose_name="app网址")
    publish_cmd = models.ForeignKey(PublishCmd,verbose_name="脚本")
    tar_name = models.CharField(max_length=64,verbose_name="程序包名称")
    tar_file = models.CharField(max_length=64,verbose_name="程序包路径")
    backup_file = models.CharField(max_length=64,verbose_name="备份路径")
    def __str__(self):
        return "%s-%s" % (self.environ,self.name)


class PublishCmd(models):
    log_type_choices = (
        ("0", "SHELL"),
        ("1", "PYTHON"),
    )
    name = models.CharField(max_length=64,verbose_name="脚本名称")
    cmd_text = models.CharField(max_length=64,choices=log_type_choices,verbose_name="脚本内容")
    cmd_ars = models.CharField(max_length=64,verbose_name="脚本参数")

    def __str__(self):
        return "%s-%s" % (self.name, self.cmd_type)



环境一对多app
    添加app
        app主机
        环境选择
        app网址
        发布命令
        程序包名称
    app主机
    环境选择
    app网址
    发布命令
    程序包名称
    测试app网址是否正常
    发布
    回滚

    添加发布命令

