#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-8-1 13:16
# @Author  : Jerry Wang
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django import forms
from audit.models import Environ,PublishCmd,App


class environ_form(forms.ModelForm):

    def clean(self):
        cleaned_data = super(environ_form, self).clean()
        print(cleaned_data)
        value = cleaned_data.get("name")
        try:
            Environ.objects.get(name=value)
            self.add_errors["name"] = self.error_class(["%s的信息已经存在" % value])
        except Environ.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = Environ
        exclude = ("id",)
        from django.forms import widgets as wid
        # widgets = {
        #     "url":wid.Textarea(attrs={"class":"c1"})
        # }


class cmd_form(forms.ModelForm):

    def clean(self):
        cleaned_data = super(cmd_form, self).clean()
        print(cleaned_data)
        value = cleaned_data.get("name")
        try:
            PublishCmd.objects.get(name=value)
            self.add_errors["name"] = self.error_class(["%s的信息已经存在" % value])
        except PublishCmd.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = PublishCmd
        exclude = ("id",)