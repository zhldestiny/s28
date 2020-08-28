#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhonghaolin'
__mtime__ = '2020/8/28'
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
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings
from qcloud_cos.cos_exception import CosServiceError


def create_bucket(bucket, region="ap-nanjing"):
	"""
	    创建桶
	    :param bucket: 桶名称
	    :param region: 区域
	    :return:
	"""
	config = CosConfig(Region=region, Secret_id=settings.TENCENT_COS_ID, Secret_key=settings.TENCENT_COS_KEY)
	client = CosS3Client(config)
	client.create_bucket(
		Bucket=bucket,
		ACL="public-read"
	)
	cors_config = {
		'CORSRule': [
			{
				'AllowedOrigin': '*',
				'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
				'AllowedHeader': "*",
				'ExposeHeader': "*",
				'MaxAgeSeconds': 500
			}
		]
	}
	client.put_bucket_cors(
		Bucket=bucket,
		CORSConfiguration=cors_config
	)


def upload_file(bucket, region, file_object, key):
	config = CosConfig(Region=region, SecretId=settings.TENCENT_COS_ID, SecretKey=settings.TENCENT_COS_KEY)
	client = CosS3Client(config)

	response = client.upload_file_from_buffer(
		Bucket=bucket,
		Body=file_object,  # 文件对象
		Key=key  # 上传到桶之后的文件名
	)

	# https://wangyang-1251317460.cos.ap-chengdu.myqcloud.com/p1.png

	return "https://{}.cos.{}.myqcloud.com/{}".format(bucket, region, key)
