from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Usersessn
import os
# from .models import Dtsrchdb, Usersessn
# from .utils import searchkaggle, dldkaggle, imgprv, tblprv
# import json, pyperclip
# import zipfile
# import io, os
# import pandas as pd

# Create your views here.
bucket='/home/pt/s3-bucket/MLWB/'
templtdir='/home/pt/ARLIS/ARLISDJ/MLWB/datasearch/templates/'


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=request.user.username
    try:
        obj = Usersessn.objects.get(user=user)
    except:
        obj = Usersessn(user=user)
        obj.userbucket='/home/pt/s3-bucket/MLWB/'+user
        os.system('mkdir '+obj.userbucket)
        os.system('mkdir '+obj.userbucket+'/processdt')
        obj.usertemplates=templtdir+user
        os.system('mkdir '+obj.usertemplates)
        obj.save()
    context = {
        'a':'b'
    }
    page = 'home.html'
    print('This is the home page on Home ')
    return render(request, page, context)
