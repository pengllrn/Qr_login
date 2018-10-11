# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import script_qr as sq
from django.http import HttpResponse
from django.http import JsonResponse
import random
import models
import datetime
import time
import json
# Create your views here.

def initial(request):
    return render(request,"index.html")

def generate_qr(request):
    ##QR's token
    lgToken=genrate_lgToken()
    ##过期时间
    expiredTime=datetime.datetime.now()+datetime.timedelta(minutes=2)
    models.lgToken.objects.create(lgToken=lgToken,expiredTime=expiredTime).save()
    qr_url="http://192.168.0.10:8000/ident/"
    qr_image=sq.make_easy_code(qr_url+lgToken)
    qr_image.save("scan_qr_login/static/qr.jpg")
    return JsonResponse({'qr_image':"fine",'qr_token':lgToken})


def genrate_lgToken(randomlength=50):
    """
    生成一个指定长度的随机字符串
    """
    lgToken=""
    base_str="abcdefghijklmnoprstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    length = len(base_str) - 1
    for i in range(randomlength):
        lgToken += base_str[random.randint(0,length)]
    return lgToken

@csrf_exempt
def ident(request,token):
    user=request.POST.get("user")
    #判断user合法性,简单做个测试
    if user=="pengllrn":
        token=models.lgToken.objects.filter(lgToken=token)
        if len(token)>0:
            token=token[0]
            if(token.status==0):
                token.status=1
                token.user=user
                token.save()
                return HttpResponse(json.dumps({"code":"10006"}))
    return HttpResponse(json.dumps({"code":"10002"}))

def polling(request,token):
    tokens = models.lgToken.objects.filter(lgToken=token)
    for i in range(6):
        tokens.update()
        if len(tokens) > 0:
            token = tokens[0]
            if token.status == 2:
                return JsonResponse({"code":10002,"message":"qr is invalid!"})
            elif token.expiredTime < datetime.datetime.now():
                token.status = 2
                token.save()
                return JsonResponse({"code":10003,"message":"qr is expired!"})
            elif token.status == 1:
                return JsonResponse({"code":10006,"message":token.user})
            else:#token=0
                time.sleep(0.5)
    return JsonResponse({"code":10001,"message":"qr waits to scan..."})

