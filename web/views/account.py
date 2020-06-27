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
from django.shortcuts import render, HttpResponse
from web import models
from web.forms.account import RegisterModelFrom, SendSmsForm
from django.conf import settings


def register(request):
	form = RegisterModelFrom()
	return render(request, "web/register.html", {"form": form})

def send_sms(request):
	"""发送短信"""
	form = SendSmsForm(request, data=request.GET)
	# 校验手机号不能为空 格式是否正确
	if form.is_valid():
		pass

	return HttpResponse("成功")