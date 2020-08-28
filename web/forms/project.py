#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhonghaolin'
__mtime__ = '2020/8/20'
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
from web.forms.bootstrap import BootStrapForm
from web import models
from django.core.exceptions import ValidationError
from web.forms.widgets import ColorRadioSelect

class ProjectModelForm(BootStrapForm, forms.ModelForm):
	# desc = forms.CharField(widget=forms.Textarea)
	bootstrap_class_exclude = ['color']

	class Meta:
		model = models.Project
		fields = ['name', 'color', 'desc']
		# 修改相应field的插件及样式
		widgets = {
			'desc': forms.Textarea,
			'color': ColorRadioSelect(attrs={'class': 'color-radio'}),
		}

	def __init__(self, request, *args, **kwargs):
		# 继承父类 重写构造函数
		super().__init__(*args, **kwargs)
		self.request = request

	def clean_name(self):
		# 1.当前用户是否创建过同名项目
		name = self.cleaned_data['name']
		exists = models.Project.objects.filter(creator=self.request.tracer.user, name=name)
		if exists:
			raise ValidationError("项目已存在")
		# 2.当前用户是否有额度
		# 最多创建项目
		# self.request.tracer.price_policy.project_num

		# 现在已创建项目
		count = models.Project.objects.filter(creator=self.request.tracer.user).count()
		if count >= self.request.tracer.price_policy.project_num:
			raise ValidationError("项目个数超限， 请购买套餐")
		return name

