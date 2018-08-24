from .models import navi
from django.shortcuts import render,HttpResponse
from navi.forms import navi_form
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    temp_name = "navi/navi-header.html"
    allnavi = navi.objects.all()
    return render(request, "navi/index.html", locals())


def add(request):
    temp_name = "navi/navi-header.html"
    if request.method == "POST":
        n_form = navi_form(request.POST)
        if n_form.is_valid():
            n_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "navi/add.html", locals())
    else:
        display_control = "none"
        n_form = navi_form()
        return render(request, "navi/add.html", locals())


def delete(request):
    env_id = request.GET.get("id", "")
    print(env_id)
    return HttpResponse(u'删除成功')