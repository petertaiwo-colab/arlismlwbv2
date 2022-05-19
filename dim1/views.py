from django.http.response import HttpResponse
from django.shortcuts import render, redirect
# from .utils import geturl, sgmk
from datasearch.models import Usersessn
import time, pyperclip
from mlengine import aws, lceng

# Create your views here.

def dim1home(request):
    user=request.user.username       
    obj = Usersessn.objects.get(user=user)  
    page = 'dim1pgs/dim1home.html'
    dtsloc = obj.metadata['dtsloc']
    numitems = obj.metadata['numitems']
    if 'csvimg' in dtsloc:
        dtsloc = 'No csv type dataset in active storage'
        numitems = 'none'
    context = {"sgmkinsturl":obj.sgmk['insturl'], "sgmkvmtype":obj.sgmk['vmtype'], 
    "lclinsturl":obj.lclnb['insturl'], "lclvmtype":obj.lclnb['vmtype'], "sgmksetuptime":obj.sgmk['setuptime'], 
    "lclsetuptime":obj.lclnb['setuptime'], 'numitems':numitems, 'dtsloc':dtsloc}
    # print(Dtsrchdb.objects.get(sess_id=sess_id).dtssmrypg)
    return render(request, page, context)

def trainmdl(request):
    user=request.user.username 
    obj = Usersessn.objects.get(user=user) 
    if request.POST['pltfm'] == 'local':
        if obj.lclnb['insturl'] == 0:
            lceng.lclnb(user, 'ml.t2.medium')
        obj = Usersessn.objects.get(user=user)
        page = obj.lclnb['insturl'] 
        print("this is view page"+page) 
        return redirect(page)
        # print('local')
        # return redirect('dim1home')
    if obj.sgmk['insturl'] != 0:
        if time.time() - obj.sgmk['urltime'] > 300:
            auth_url = aws.geturl(obj.sgmk['instname'])
            obj.sgmk['insturl'] = auth_url
            obj.save()
    if obj.sgmk['insturl'] == 0:
        aws.sgmk(user, 'ml.t2.medium')
    # if time.time() < obj
    # print(time.time()-300)
    # sgmk(user, 'ml.t2.medium') 
    page = obj.sgmk['insturl']  
    print(page)
    return redirect(page)

def copyurl(request, whcnb):
    user=request.user.username
    obj = Usersessn.objects.get(user=user) 
    if whcnb == 'lclnb':
        pyperclip.copy(obj.lclnb['insturl'])
    if whcnb == 'sgmk':
        pyperclip.copy(obj.sgmk['insturl'])
    pyperclip.paste()
    return redirect('dim1home')

# def index(request):
#     if not request.session.session_key:
#         request.session.save()
#         sess_id = request.session.session_key
#         obj = Dtsrchdb(sess_id=sess_id)
#         obj.save()
#     metadata = 'metadata.json'
#     sritems = 'sritems.txt'
#     csvdts = '/home/pt/s3-bucket/MLWB/csvdts.zip'
#     csvimg = 'csvimg.csv'
#     imagehtml = 'MLWB/templates/imgprv.html'
#     if os.path.isfile(imagehtml):
#         print('got a html image')
#         page = 'homeWtImPr.html'
#         return render(request, page)
#     if os.path.isfile(csvimg):
#         print('got a csv image')
#         page = 'homeWtImDt.html'
#         return render(request, page)
#     if os.path.isfile(csvdts):
#         print('got a zip')
#         page = 'homeWtCsDt.html'
#         return render(request, page)
#     if os.path.isfile(sritems):
#         page = 'homeWtSr.html'
#         return render(request, page)
#     if os.path.isfile(metadata):
#         with open(metadata) as f:
#             data = json.load(f)
#         with open('currimage.json') as fp:
#             data2 = json.load(fp)
#             data = data.update(data2)
#             print(data)
#         page = 'homeWtDt.html'
#     else:
#         data = {
#             'a':'b'
#         }
#         page = 'home.html'
#     return render(request, page, data)
