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
from django.conf.urls import url, include
from web.views import account, home, project

urlpatterns=[
	url(r'^register/$', account.register, name="register"),
	url(r'^login/$', account.login, name="login"),
	url(r'^login/sms/$', account.login_sms, name="login_sms"),
	url(r'^send/sms/$', account.send_sms, name="send_sms"),
	url(r'^image/code/$', account.image_code, name="image_code"),
	url(r'^index/$', home.index, name="index"),
	url(r'^logout/$', account.logout, name="logout"),

	# 项目列表
	url(r'^project/list/$', project.project_list, name="project_list"),
]