#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-7-31 19:25
# @Author  : Jerry Wang
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django import forms
from .models import navi


class navi_form(forms.ModelForm):

    def clean(self):
        cleaned_data = super(navi_form, self).clean()
        value = cleaned_data.get("name")
        try:
            navi.objects.get(name=value)
            self.add_errors["name"] = self.error_class(["%s的信息已经存在" % value])
        except navi.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = navi
        exclude = ("id",)