from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Dtsrchdb, Usersessn
from .utils import searchkaggle, dldkaggle, imgprv, tblprv
import json, pyperclip
import zipfile
import io, os
import pandas as pd

# Create your views here.
bucket='/home/pt/s3-bucket/MLWB/'
templtdir='/home/pt/ARLIS/ARLISDJ/MLWB/datasearch/templates/'


def dtsethome(request):
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
    metadata = obj.metadata
    sritems = obj.sritems
    # print(obj.sritems)
    csvdts = obj.userbucket+'/csvdts.zip'
    csvimg = obj.userbucket+'/csvimg.csv'
    imagehtml = obj.usertemplates+'/imgprv.html'
    srtable = obj.usertemplates+'/srtbl.html'
    csdtprv = obj.usertemplates+'/dtprv.html'
    csimdtprv = obj.usertemplates+'/imdtsprv.html'
    if os.path.isfile(imagehtml):
        print('got a html image')
        page = 'homeWtImPr.html'
        context = {'imagehtml':imagehtml, 'labels':obj.metadata['labels'], 'numitems':obj.metadata['numitems'],
        'currvw':obj.metadata['currvw'], 'label':obj.currimage['label'], 'imagepath':obj.currimage['imagepath'],
        'width':obj.currimage['width'], 'height':obj.currimage['height']}
        return render(request, page, context)
    if os.path.isfile(csimdtprv):
        print('got a csv image')
        page = 'homeWtImDt.html'
        context = {'csimdtprv':csimdtprv, 'labels':obj.metadata['labels'], 'numitems':obj.metadata['numitems'],
        'currpg':obj.metadata['currpg'], 'dtsloc':obj.metadata['dtsloc']}
        return render(request, page, context)
    if os.path.isfile(csdtprv):
        print('got a csv dataset')
        page = 'homeWtCsDt.html'
        context = {'csdtprv':csdtprv, 'labels':obj.metadata['labels'], 'numitems':obj.metadata['numitems'],
        'currpg':obj.metadata['currpg'], 'dtsloc':obj.metadata['dtsloc']}
        return render(request, page, context)
  
    if os.path.isfile(srtable):
        page = 'homeWtSr.html'
        context = {'srtable':srtable, 'dtsite':obj.dtsite, 'searchkey':obj.searchkey,
		'lensritems':len(obj.sritems)}
        print('data search results hit')
        return render(request, page, context)
    context = {
        'a':'b'
    }
    page = 'home.html'
    print('datasearch default hit ')
    return render(request, page, context)


def index1(request):
    if not request.session.session_key:
        request.session.save()
        sess_id = request.session.session_key
        obj = Dtsrchdb(sess_id=sess_id)
        obj.save()
        return redirect('http://time.is')
    else:
        sess_id = request.session.session_key
        ins = Dtsrchdb.objects.get(sess_id=sess_id)
        keywords = "fraud", "detection"
        res = searchkaggle(keywords)
        context = {
            'object': ins,
            'result': res
        }

        return render(request, 'get_image.html', context)


def dtsearchrs(request):
    sess_id = request.session.session_key
    user=request.user.username
    ins = Usersessn.objects.get(user=user)
    try:
        os.remove(templtdir+user+"/dtprv.html")
    except:
        print("no dtprv.html file to remove")
    try:
        os.remove(templtdir+user+"/imdtsprv.html")
    except:
        print("no imdtsprv.html file to remove")
    if request.method == 'POST':
        ins.dtsite = request.POST['dtsite']
        ins.searchkey = request.POST['searchkey']
        if ins.searchkey=="":
            return redirect('index')
        ins.save()
        searchkaggle(request.POST['searchkey'], request.user.username) 
        return redirect('index')


def dtdload(request):
    dtsnum = request.POST['dtsnum']
    if dtsnum=="Select-Dataset":
            return redirect('index')
    # with open("sritems.txt", "r") as fp:
    #     dtref = json.load(fp)
    obj = Usersessn.objects.get(user=request.user.username)
    # print(obj.sritems)
    context = {
        'dtsnum': dtsnum,
        'dtsitem': obj.sritems[int(dtsnum)-1],
        # 'dtsitem': dtref[int(dtsnum)]
    }
    dldkaggle(context['dtsitem'], request.user.username)
    return redirect('index')


def dtsprv(request):
    with open('metadata.json') as f:
        data = json.load(f)
        if request.POST['scroll'] == 'down':
            data['currvw'] += 1
    with open('metadata.json', 'w') as f:
        json.dump(data, f)
    dtpath = r'C:\Users\PTatMSU\ARLIS\ARLISDJ\mlwb\csvdts\dogs-cats-images.csv'
    df = pd.read_csv(dtpath)
    idx = df['dataset/test_set/cats/cat.4001.jpg'].iloc[data['currvw']]
    zipath = r'C:\Users\PTatMSU\ARLIS\ARLISDJ\mlwb\processdt\dogs-cats-images.zip'
    # print(df.to_string())
    with zipfile.ZipFile(zipath, 'r') as f:
        ifile = f.open(idx)
        img = Image.open(ifile)
        # display(img)
    # imgpath1 = r'C:\Users\PTatMSU\ARLIS\ARLISDJ\mlwb\static\images\prv\prv.png'
    # img.save(imgpath1,"PNG")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    yield HttpResponse(buffer.getvalue(), content_type='image/png')
    # return redirect('index')
    # content = {"response": response}
    # return render (request, 'get_image.html', content)


def dspfrm(request, dspwht):
    user=request.user.username
    print(dspwht)
    if dspwht == 'imgset':
        scroll = request.POST['scroll']
        imgprv(scroll, user)
    if dspwht == 'tblpg':
        scroll = request.POST['scroll']
        dtpath = bucket+user+'/csvdts.zip'
        tblpath=templtdir+user+'/dtprv.html'
        tblprv(scroll, user, dtpath, tblpath)
    if dspwht == 'tblpgim':
        scroll = request.POST['scroll']
        dtpath = bucket+user+'/csvimg.csv'
        tblpath=templtdir+user+'/imdtsprv.html'
        tblprv(scroll, user, dtpath, tblpath)
    # more data window views coming.....
    return redirect('index')

def clckvw(request, dspwht):
    user=request.user.username
    obj = Usersessn.objects.get(user=user)  
    idx = int(dspwht)+50*int(obj.metadata["currpg"]) 
    print(idx)
    obj.metadata["currvw"]=idx-1
    obj.save()
    imgprv("down", user)
    # if dspwht == 'tblpg':
    #     scroll = request.POST['scroll']
    #     imgprv(scroll)
    # # more data window views coming.....
    return redirect('index')

def dtsprv1(request):
    user=request.user.username
    os.remove(templtdir+user+"/imgprv.html")
    return redirect('index')

def srchprv1(request):
    user=request.user.username
    try:
        os.remove(templtdir+user+"/imdtsprv.html")
    except:
        print("image csv file not present, try delete dataset csv file")
    try:
        os.remove(templtdir+user+"/dtprv.html")
    except:
        print("dataset csv file not present")
    return redirect('index')








