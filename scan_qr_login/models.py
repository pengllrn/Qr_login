# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class lgToken(models.Model):
    lgToken=models.CharField(db_column="lg_token",max_length=120,null=False,blank=False) #序列号
    status=models.IntegerField(db_column="status",default=0)  #0 未扫码，1已登录，2二维码无效
    user=models.CharField(db_column="user",max_length=100,null=True,blank=True)
    expiredTime=models.DateTimeField(db_column="expierd_time")  #过期时间

    class Meta:
        db_table="lgToken"