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
from django.conf import settings


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


class SendSmsForm(forms.Form):
	phone = forms.CharField(label="phone", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

	def __init__(self, request, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.request = request


	def clean_phone(self):
		"""手机号校验的钩子"""
		phone = self.cleaned_data["phone"]
		# 判断短信模版
		tpl = self.request.GET.get("tpl")
		template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
		if not template_id:
			raise ValidationError("短信模版错误")
		# 校验数据库中是否有手机号
		exists = models.UserInfo.objects.filter(phone=phone).exists()
		if exists:
			raise ValidationError("手机号已存在")

		return phone

