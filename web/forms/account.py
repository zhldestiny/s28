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
import random
from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection
from utils import encrypt
from web.forms.bootstrap import BootStrapForm


class RegisterModelFrom(forms.ModelForm):
	phone = forms.CharField(label="phone", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])    # validators正则
	password = forms.CharField(
		label="password",
		min_length=6,
		max_length=20,
		error_messages={
			'min_length': '密码长度不能小于6个字符',
			'max_length': '密码长度不能大于20个字符'
		},
		widget=forms.PasswordInput()
	)    # 隐藏显示密码      attrs={"class": "form-control", "placeholder": "confirm password"}
	confirm_password = forms.CharField(
		label="confirm_password",
		min_length=6,
		max_length=20,
		error_messages={
			'min_length': '重复密码长度不能小于6个字符',
			'max_length': '重复密码长度不能大于20个字符'
		},
		widget=forms.PasswordInput()
	)    # attrs={"class": "form-control", "placeholder": "confirm password"}
	code = forms.CharField(label="验证码", widget=forms.TextInput())    # attrs={"class": "form-control", "placeholder": "请输入验证码"}
	class Meta:
		model = models.UserInfo
		# fields = "__all__"    # 默认顺序展示
		fields = ["username", "email", "phone", "code", "password", "confirm_password"]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# 修改fileds样式
		for name, field in self.fields.items():
			field.widget.attrs["class"] = "form-control"
			field.widget.attrs["placeholder"] = "plz input " + name    # '请输入%s' % (field.label,)

	def clean_username(self):
		username = self.cleaned_data['username']
		exists = models.UserInfo.objects.filter(username=username).exists()
		if exists:
			raise ValidationError('用户名已存在')
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		exists = models.UserInfo.objects.filter(email=email).exists()
		if exists:
			raise ValidationError('邮箱已存在')
		return email

	def clean_password(self):
		pwd = self.cleaned_data['password']
		# 加密&返回
		return encrypt.md5(pwd)


	def clean_confirm_password(self):
		pwd = self.cleaned_data.get('password')
		confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])
		if pwd != confirm_pwd:
			raise ValidationError('两次密码不一致')
		return confirm_pwd

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		exists = models.UserInfo.objects.filter(phone=phone).exists()
		if exists:
			raise ValidationError('手机号已注册')
		return phone

	def clean_code(self):
		code = self.cleaned_data['code']
		phone = self.cleaned_data.get('phone')
		if not phone:
			return code
		conn = get_redis_connection()
		redis_code = conn.get(phone)
		if not redis_code:
			raise ValidationError('验证码失效或未发送，请重新获取')
		redis_str_code = redis_code.decode('utf-8')    # redis里的byte类型 转化为 字符
		if code.strip() != redis_str_code:
			raise ValidationError('验证码错误，请重新输入')
		return code



class SendSmsForm(forms.Form):
	phone = forms.CharField(label="phone", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

	def __init__(self, request, *args, **kwargs):
		# 继承父类 重写构造函数
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
		if tpl == "login":
			# 登录时：数据库中存在已注册手机
			if not exists:
				raise ValidationError("手机号不存在")
		else:
			# 注册时：数据库中不存在手机号
			if exists:
				raise ValidationError("手机号已存在")
		# 发短信
		code = random.randrange(1000, 9999)
		print("验证码为：", code)
		# sms = send_sms_single(phone, template_id, [code, ])
		# if sms["result"] != 0:
		# 	raise ValidationError("短信发送失败：{}".format(sms["errmsg"]))

		# 验证码写入redis(djano-redis)    暂停服务：连接不上本地redis
		conn = get_redis_connection("default")
		conn.set(phone, code, ex=60)    # 写入redis 短信：验证码，存在时间60s有效；
		# 手动完成redis 存储功能

		return phone


class LoginSMSForm(BootStrapForm, forms.Form):
	phone = forms.CharField(label="phone", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
	code = forms.CharField(label="code", widget=forms.TextInput())
	# 钩子函数校验
	def clean_phone(self):
		phone = self.cleaned_data["phone"]
		exists = models.UserInfo.objects.filter(phone=phone).exists()
		# user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
		if not exists:
			raise ValidationError("手机号不存在")
		return phone

	def clean_code(self):
		code = self.cleaned_data["code"]
		phone = self.cleaned_data.get("phone")
		# 手机号不存在，则验证码无需再校验
		if not phone:
			return code

		conn = get_redis_connection()
		redis_code = conn.get(phone)
		if not redis_code:
			raise ValidationError('验证码失效或未发送，请重新发送')

		redis_str_code = redis_code.decode("utf-8")
		if code.strip() != redis_str_code:
			raise ValidationError('验证码错误，请重新输入')
		return code


class LoginForm(BootStrapForm, forms.Form):
	username = forms.CharField(label='邮箱或手机号')
	password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True))
	code = forms.CharField(label='图片验证码')

	def __init__(self, request, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.request = request

	def clean_password(self):
		pwd = self.cleaned_data['password']
		# 加密 & 返回
		return encrypt.md5(pwd)

	def clean_code(self):
		""" 钩子 图片验证码是否正确？ """
		# 读取用户输入的yanzhengm
		code = self.cleaned_data['code']

		# 去session获取自己的验证码
		session_code = self.request.session.get('image_code')
		if not session_code:
			raise ValidationError('验证码已过期，请重新获取')

		if code.strip().upper() != session_code.strip().upper():
			raise ValidationError('验证码输入错误')

		return code
