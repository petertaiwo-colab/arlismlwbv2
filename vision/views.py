from django.http.response import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .utils import createdtcsv, tblhtml, createcurrimagehtml, persons, get_plot, get_plot2, wrhtml, perfmetrics
from datasearch.models import Usersessn
from .models import Imagesessn, Visionuser
import time, pyperclip, os
from mlengine import aws, lceng
import pandas as pd

# Create your views here.
bucket='/home/pt/s3-bucket/MLWB/'
templtdir='/home/pt/ARLIS/ARLISDJ/MLWB/vision/templates/visionpgs/'

def stdperftestpers(request):
    user=request.user.username
    obj = Visionuser.objects.get(user=user)
    os.system('rm '+bucket+user+'/images/* '+bucket+user+'/visionimages.csv '+bucket+user+'/visionjobs/*detpers.csv '
        +templtdir+user+'/visionimageshtml.html '+templtdir+user+'/currimagehtml.html')
    os.system('cp /home/pt/ARLIS/ARLISDJ/MLWB/s3-bucket/MLWB/perstestimgs/csv/visionimages.csv '+bucket+user)
    os.system('cp /home/pt/ARLIS/ARLISDJ/MLWB/s3-bucket/MLWB/perstestimgs/images/* '+bucket+user+'/images')
    # use visingjobs function to complete, this is user independent, images and csv is on the workbench intfc
    # imgdir = '/home/pt/ARLIS/ARLISDJ/MLWB/vision/perstestimgs/'

    imgdir = '/home/pt/s3-bucket/MLWB/perstestimgs/images/'
    os.system('rm '+imgdir[:-7]+'csv/yolo.csv '+imgdir[:-7]+'csv/azure.csv '+imgdir[:-7]+'csv/rekognition.csv '+imgdir[:-7]+'csv/groundtruth.csv')
    # os.system('cp '+bucket+user+'/visionimages.csv '+imgdir)
    persons('rekognition', imgdir[:-7]+'images/', imgdir[:-7]+'csv/rekognition.csv')
    persons('azure', imgdir[:-7]+'images/', imgdir[:-7]+'csv/azure.csv')
    persons('yolo', imgdir[:-7]+'images/', imgdir[:-7]+'csv/yolo.csv')
    persons('groundtruth', imgdir[:-7]+'images/', imgdir[:-7]+'csv/groundtruth.csv')    
    obj.metadata["annotsrc"]=imgdir[:-7]+'csv/rekognition.csv'
    obj.save()
    perfmetrics(imgdir,imgdir[:-7]+'csv/groundtruth.csv',imgdir[:-7]+'csv/yolo.csv',imgdir[:-7]+'csv/azure.csv',imgdir[:-7]+'csv/rekognition.csv')
    return redirect('imageai')

def visionhome(request):
    user=request.user.username       
    obj = Usersessn.objects.get(user=user)  
    page = 'visionpgs/visionhome.html'
    dtsloc = obj.metadata['dtsloc']
    numitems = obj.metadata['numitems']
    if not 'csvimg' in dtsloc:
        dtsloc = 'No image dataset in active storage'
        numitems = 'none'
    context = {"sgmkinsturl":obj.sgmk['insturl'], "sgmkvmtype":obj.sgmk['vmtype'], 
    "lclinsturl":obj.lclnb['insturl'], "lclvmtype":obj.lclnb['vmtype'], "sgmksetuptime":obj.sgmk['setuptime'], 
    "lclsetuptime":obj.lclnb['setuptime'], 'numitems':numitems, 'dtsloc':dtsloc}
    # print(Dtsrchdb.objects.get(sess_id=sess_id).dtssmrypg)
    return render(request, page, context)

def imageai(request):
    user=request.user.username
    try:
        obj = Visionuser.objects.get(user=user)
    except:
        obj = Visionuser(user=user)
        os.system('mkdir '+bucket+user+'/images')
        os.system('mkdir '+bucket+user+'/visionjobs')
        os.system('mkdir '+templtdir+user)
        obj.save()
    # imgloc=obj.userbucket+'/image'
    # print(imgloc)
    # if request.POST['task'] == 'image':
    page = 'visionpgs/visionimg.html'
    context={}
    visionimagescsv = bucket+user+'/visionimages.csv'
    visionimageshtml = templtdir+user+'/visionimageshtml.html'
    currimagehtml = templtdir+user+'/currimagehtml.html'
    if os.path.isfile(visionimagescsv):
        print('got a visionimg csv')
        df = pd.read_csv(visionimagescsv)
        tblhtml(df, visionimageshtml)
        context['df']=visionimageshtml
        if os.path.isfile(currimagehtml):
            print('current image html exists')
            context['df']=currimagehtml
    else:
        wrhtml("head", "body", currimagehtml)
        context['df']=currimagehtml
        # idx = int(obj.metadata["currvw"])
        # df = pd.read_csv(visionimagescsv)#, skiprows=idx-1, nrows=idx)
        # df = df['item'].iloc[idx]
        # img_tag = "<img src='" +bucket+user+'/images/'+df + "' width='960' height='720'/>"
        # wrhtml("preview", img_tag, currimagehtml)
        # # df = df.loc[0,'items']
        # print(df)
        # context['df']=currimagehtml
        # return render(request, currimagehtml)
        
    return render(request, page, context)
    print(request.POST['task'])
    return redirect('visionhome')

def upldimg(request):
    user=request.user.username    
    os.system('rm '+bucket+user+'/images/* '+bucket+user+'/visionimages.csv '+bucket+user+'/visionjobs/*detpers.csv '
        +templtdir+user+'/visionimageshtml.html '+templtdir+user+'/currimagehtml.html')
    if request.method == "POST":
        name = request.POST.get("filename")
        myfile = request.FILES.getlist("uploadfiles")
        for f in myfile:
            Imagesessn(user=user, myfiles=f).save()
        filist = os.popen(
		'ls '+bucket+user+'/images').read().splitlines()
        print(filist)
        dtpath = bucket+user+'/visionimages.csv'
        createdtcsv(filist, dtpath, user)
        # return HttpResponse("Okay......")
        return redirect('imageai')
    # user=request.user.username       
    # obj = Usersessn.objects.get(user=user) 
    # # obj = Item()
    # obj.image = request.FILES['image']
    # print(len(obj.image))
    # obj.save()
    # page = 'visionpgs/visionimg.html'
    # context={}
    return redirect('imageai')


# def imgvw(request, dspwht):
#     print('attempt viewing am image')
#     user=request.user.username
#     obj = Visionuser.objects.get(user=user)  
#     idx = int(dspwht)+50*int(obj.metadata["currpg"]) 
#     # print(idx)
#     obj.metadata["currvw"]=idx
#     obj.save()
#     visionimagescsv = bucket+user+'/visionimages.csv'
#     df = pd.read_csv(visionimagescsv)#, skiprows=idx-1, nrows=idx)
#     imagefile = df['item'].iloc[idx]
#     htmlpath = templtdir+user+'/currimagehtml.html'
#     imagepath = bucket+user+'/images/'+imagefile
#     print(htmlpath)
#     print(imagepath)
#     createcurrimagehtml(htmlpath,imagepath)
#     # visionimagescsv = bucket+user+'/visionimages.csv'
#     # df = pd.read_csv(visionimagescsv, skiprows=idx-1, nrows=idx)
#     # imgprv("down", user)
#     # if dspwht == 'tblpg':
#     #     scroll = request.POST['scroll']
#     #     imgprv(scroll)
#     # # more data window views coming.....
#     return redirect('imageai')

def imgvw(request, dspwht):
    print('attempt viewing am image')
    user=request.user.username
    # rekdetpersoncsv = bucket+user+'/visionjobs/yolodetpers.csv'
    obj = Visionuser.objects.get(user=user)  
    detpersoncsv = obj.metadata["annotsrc"]
    print('whats annotation sourse?')
    print(detpersoncsv)
    idx = int(dspwht)+50*int(obj.metadata["currpg"]) 
    # print(idx)
    obj.metadata["currvw"]=idx
    obj.save()
    visionimagescsv = bucket+user+'/visionimages.csv'
    df = pd.read_csv(visionimagescsv)#, skiprows=idx-1, nrows=idx)
    imagefile = df['item'].iloc[idx]
    BB=[]
    if os.path.isfile(detpersoncsv):
        dfrek = pd.read_csv(detpersoncsv)
        BB = dfrek.loc[dfrek['imagefile'] == imagefile]
        print('check BB')
        print(imagefile)
        print(BB)
    htmlpath = templtdir+user+'/currimagehtml.html'
    imagepath = bucket+user+'/images/'+imagefile
    print(htmlpath)
    print(imagepath)
    srcname=detpersoncsv.split('/')[-1].split('.')[0]
    createcurrimagehtml(htmlpath,imagepath,BB,srcname)
    # visionimagescsv = bucket+user+'/visionimages.csv'
    # df = pd.read_csv(visionimagescsv, skiprows=idx-1, nrows=idx)
    # imgprv("down", user)
    # if dspwht == 'tblpg':
    #     scroll = request.POST['scroll']
    #     imgprv(scroll)
    # # more data window views coming.....
    return redirect('imageai')


def imagelist(request):
    user=request.user.username
    os.system('rm '+templtdir+user+'/currimagehtml.html')
    return redirect('imageai')

def imgscroll(request):
    user=request.user.username
    scroll = request.POST.get("scroll")
    obj = Visionuser.objects.get(user=user)
    max = obj.metadata["numitems"]    
    if scroll == 'up':
        if obj.metadata["currvw"]>0:
            obj.metadata["currvw"] -=1
    if scroll == 'down':
        if obj.metadata["currvw"]<max-1:
            obj.metadata["currvw"] +=1
    obj.save()    
    return redirect('imgvw', dspwht=str(obj.metadata["currvw"]))

def visionjob(request):
    os.system('rm /home/pt/s3-bucket/MLWB/perstestimgs/csv/yolo.csv ')
    user=request.user.username
    obj = Visionuser.objects.get(user=user)
    imgdir=bucket+user+'/images/'
    resdir=bucket+user+'/visionjobs/'
    if request.method == "POST":
        task = request.POST.get("task")
        pltfm = request.POST.get("pltfm")
        obj.metadata["annotsrc"]=resdir+pltfm+'detpers.csv'
        obj.save()
        print('task '+task+' to run on '+pltfm)
        if task == 'detpers':           
            persons(pltfm, imgdir, obj.metadata["annotsrc"])
            # return HttpResponse("Okay......")
            return redirect('imageai')
    return redirect('imageai')

def perfpltimg(request):
    user=request.user.username
    pltpath = bucket+user+'/visionjobs/perfpltimg.png'
    os.system('rm '+pltpath)
    if os.path.isfile('/home/pt/s3-bucket/MLWB/perstestimgs/csv/yolo.csv'):
        dfimgs = pd.read_csv('/home/pt/s3-bucket/MLWB/perstestimgs/visionimages.csv')
        dfyol = pd.read_csv('/home/pt/s3-bucket/MLWB/perstestimgs/csv/yolo.csv')
        dfrek = pd.read_csv('/home/pt/s3-bucket/MLWB/perstestimgs/csv/rekognition.csv')
        dfazu = pd.read_csv('/home/pt/s3-bucket/MLWB/perstestimgs/csv/azure.csv')
        dfman = pd.read_csv('/home/pt/s3-bucket/MLWB/perstestimgs/csv/groundtruth.csv')

        x = dfimgs['item'].tolist() 
        y_yol = [dfyol['imagefile'].tolist().count(y) for y in x]
        y_rek = [dfrek['imagefile'].tolist().count(y) for y in x]
        y_azu = [dfazu['imagefile'].tolist().count(y) for y in x]
        y_man = [dfman['imagefile'].tolist().count(y) for y in x]
        x_red = list(map(lambda n:n[-7:], x))
        get_plot2(x_red, y_yol, y_azu, y_rek, y_man, pltpath, 'Compare no of persons detected', 'image items', 'no of persons', 'yolo', 'azure', 'rekognition', 'groundtruth')
        response = FileResponse(open(pltpath, 'rb'))
        return response
    else:
        dfimgs = pd.read_csv(bucket+user+'/visionimages.csv')
        dfyol = pd.read_csv(bucket+user+'/visionjobs/yolodetpers.csv')
        dfrek = pd.read_csv(bucket+user+'/visionjobs/rekognitiondetpers.csv')
        dfazu = pd.read_csv(bucket+user+'/visionjobs/azuredetpers.csv')

        x = dfimgs['item'].tolist() 
        y_yol = [dfyol['imagefile'].tolist().count(y) for y in x]
        y_rek = [dfrek['imagefile'].tolist().count(y) for y in x]
        y_azu = [dfazu['imagefile'].tolist().count(y) for y in x]
        x_red = list(map(lambda n:n[-7:], x))
        get_plot(x_red, y_yol, y_azu, y_rek, pltpath, 'Compare no of persons detected', 'image items', 'no of persons', 'yolo', 'azure', 'rekognition')
        response = FileResponse(open(pltpath, 'rb'))
        return response
    # chart = get_plot(x, y1, y2)
    # use lambda function to plot object localization error
    # print(list(map(lambda x:x**2, n))) -- n is a list, lambda fn is on each item in n


def perfpltimg2(request):
    user=request.user.username
    pltpath = bucket+user+'/visionjobs/perfpltimg.png'
    os.system('rm '+pltpath)
    if os.path.isfile('/home/pt/s3-bucket/MLWB/perstestimgs/csv/yolo.csv'):
        dfimgs = pd.read_csv('/home/pt/s3-bucket/MLWB/perstestimgs/visionimages.csv')
        dfyol = pd.read_csv('/home/pt/s3-bucket/MLWB/perstestimgs/csv/yolo.csv')
        dfrek = pd.read_csv('/home/pt/s3-bucket/MLWB/perstestimgs/csv/rekognition.csv')
        dfman = pd.read_csv('/home/pt/s3-bucket/MLWB/perstestimgs/csv/groundtruth.csv')

        imgdir = '/home/pt/s3-bucket/MLWB/perstestimgs/images/'
        y_yol, y_azu, y_rek, x =perfmetrics(imgdir,imgdir[:-7]+'csv/groundtruth.csv',imgdir[:-7]+'csv/yolo.csv',imgdir[:-7]+'csv/azure.csv',imgdir[:-7]+'csv/rekognition.csv')
        
        x = dfimgs['item'].tolist() 
        # y_yol = [dfyol['imagefile'].tolist().count(y) for y in x]
        # y_rek = [dfrek['imagefile'].tolist().count(y) for y in x]
        y_man = [dfman['imagefile'].tolist().count(y) for y in x]
        x_red = list(map(lambda n:n[-7:], x))
        print("in view")
        print(x_red)
        print(y_yol)
        print(y_rek)
        
        get_plot(x_red, y_yol, y_azu, y_rek, pltpath, 'Compare F1 Score', 'image items', 'F1 score', 'yolo', 'azure', 'rekognition')
        response = FileResponse(open(pltpath, 'rb'))
        return response

