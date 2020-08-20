#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhonghaolin'
__mtime__ = '2020/8/19'
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
from scripts import base
from web import models

def run():
	models.PricePricy.objects.create(
		title='VIP',
		price=100,
		project_num=50,
		project_member=10,
		project_space=10,
		per_file_size=500,
		category=2
	)
	models.PricePricy.objects.create(
		title='SVIP',
		price=200,
		project_num=150,
		project_member=110,
		project_space=110,
		per_file_size=1024,
		category=2
	)
	models.PricePricy.objects.create(
		title='VVIP',
		price=500,
		project_num=550,
		project_member=510,
		project_space=510,
		per_file_size=2048,
		category=2
	)


if __name__ == '__main__':
	run()