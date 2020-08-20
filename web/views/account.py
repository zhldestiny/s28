#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhonghaolin'
__mtime__ = '2020/6/23'
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
import uuid
import datetime
from io import BytesIO
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from web import models
from web.forms.account import RegisterModelFrom, SendSmsForm, LoginSMSForm, LoginForm
from django.conf import settings
from utils.image_code import check_code


def register(request):
	if request.method == 'GET':
		form = RegisterModelFrom()
		return render(request, "web/register.html", {"form": form})
	form = RegisterModelFrom(data=request.POST)
	if form.is_valid():
		# 验证通过，写入数据库（密码要是密文）
		# instance = form.save，在数据库中新增一条数据，并将新增的这条数据赋值给instance

		# 用户表中新建一条数据（注册）
		instance = form.save()
		# 创建交易记录
		# 方式一
		policy_object = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
		models.Transaction.objects.create(status=2, order=str(uuid.uuid4()), user=instance, price_policy=policy_object,
			count=0, price=0, start_datetime=datetime.datetime.now())

		# 方式二

		return JsonResponse({'status': True, 'data': '/login/'})

	return JsonResponse({'status': False, 'error': form.errors})


def login(request):
	if request.method == 'GET':
		form = LoginForm(request)
		return render(request, 'web/login.html', {"form": form})
	form = LoginForm(request, data=request.POST)
	print(form)
	if form.is_valid():
		username = form.cleaned_data["username"]
		print(username)
		password = form.cleaned_data["password"]

		user_object = models.UserInfo.objects.filter(Q(email=username) | Q(phone=username)).filter(
			password=password).first()
		if user_object:
			request.session['user_id'] = user_object.id
			request.session.set_expiry(60 * 60 * 24 * 14)
			return redirect('index')
		form.add_error('username', '用户名或密码错误')
	return render(request, "web/login.html", {"form": form})


def logout(request):
	request.session.flush()
	return redirect('index')

def login_sms(request):
	if request.method == 'GET':
		form = LoginSMSForm()
		return render(request, 'web/login_sms.html', {"form": form})
	form = LoginSMSForm(request.POST)
	if form.is_valid():
		phone = form.cleaned_data["phone"]

		# 把用户名写入seesion中
		user_object = models.UserInfo.objects.filter(phone=phone).first()
		request.session['user_id'] = user_object.id
		request.session.set_expiry(60 * 60 * 24 * 14)    # session 默认有效时间为两周
		return JsonResponse({"status": True, 'data': "/index/"})

	return JsonResponse({"status": False, 'error': form.errors})


def send_sms(request):
	"""发送短信"""
	form = SendSmsForm(request, data=request.GET)
	# 校验手机号不能为空 格式是否正确
	if form.is_valid():
		# 发短信 & 在钩子函数中做
		# redis & 在钩子函数中做
		return JsonResponse({"status": True})

	return JsonResponse({'status': False, 'error': form.errors})


def image_code(request):
	"""生成图片验证码"""
	image_object, code = check_code(char_length=4)
	request.session["image_code"] = code
	request.session.set_expiry(60)    # 主动修改session的过期时间60s

	stream = BytesIO()
	image_object.save(stream, 'png')
	print("图片验证码：", code)
	return HttpResponse(stream.getvalue())
