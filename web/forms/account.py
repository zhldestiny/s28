#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhonghaolin'
__mtime__ = '2020/6/24'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class RegisterModelFrom(forms.ModelForm):
	phone = forms.CharField(label="phone", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])    # validators正则
	password = forms.CharField(label="password", widget=forms.PasswordInput())    # 隐藏显示密码      attrs={"class": "form-control", "placeholder": "confirm password"}
	confirm_password = forms.CharField(label="confirm_password", widget=forms.PasswordInput())    # attrs={"class": "form-control", "placeholder": "confirm password"}
	code = forms.CharField(label="验证码", widget=forms.TextInput())    # attrs={"class": "form-control", "placeholder": "请输入验证码"}
	class Meta:
		model = models.Login_info
		# fields = "__all__"    # 默认顺序展示
		fields = ["username", "email", "phone", "code", "password", "confirm_password"]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for name, field in self.fields.items():
			field.widget.attrs["class"] = "form-control"
			field.widget.attrs["placeholder"] = "plz input " + name    # '请输入%s' % (field.label,)