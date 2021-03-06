from django.contrib import admin
from audit import models
# Register your models here.


class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['session','cmd','date']
    list_filter = ['date','session']


class SessionLogAdmin(admin.ModelAdmin):
    list_display = ['id','account','host_user_bind','start_date','end_date']
    list_filter = ['start_date','account']


class TaskLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_id', 'host_user_bind_id', 'result', 'date']
    list_filter = ["result",]


admin.site.register(models.Host)
admin.site.register(models.HostUser)
admin.site.register(models.HostGroup)
admin.site.register(models.HostUserBind)
admin.site.register(models.Account)
admin.site.register(models.IDC)
admin.site.register(models.AuditLog)
admin.site.register(models.SessionLog)
admin.site.register(models.Slb)
admin.site.register(models.AccessLog)
admin.site.register(models.Task)
admin.site.register(models.TaskLog,TaskLogAdmin)
admin.site.register(models.EnvironUrl)
admin.site.register(models.Environ)