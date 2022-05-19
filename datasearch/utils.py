from .models import Usersessn
import pandas as pd
import os
import json
import zipfile
import csv
import base64
import io
from PIL import Image

bucket='/home/pt/s3-bucket/MLWB/'
templtdir='/home/pt/ARLIS/ARLISDJ/MLWB/datasearch/templates/'
os.environ['KAGGLE_USERNAME'] = "petertaiwo"
os.environ['KAGGLE_KEY'] = "463e53d7143fadf6c40abbab2d8f0135"

def wrhtml(head, body, filename):
	html_content = f"<html> <head> {head} </head> <body> {body} </body> </html>"
	with open(filename, "w") as html_file:
		html_file.write(html_content)
		print("html file created!")

def tblhtml(data, filename):
	B="<tr><th></th>"
	for col in data.columns:
		B += "<th>"+col+"</th>"
	B += "</tr>"
	C = ""
	if 'imdtsprv' in filename:
		for i in range(len(data.index)):
			A="<tr><th>"+str(i)+"</th>"
			for j in range(len(data.columns)):
				if j==0:
					refl=str(data._get_value(i,data.columns[j]))
					A += "<td><a href='{% url 'clckvw' dspwht='"+str(i)+"' %}'>"+refl+"</a></td>"
				else:
				   A += "<td>"+str(data._get_value(i,data.columns[j]))+"</td>" 
			A += "</tr>"
			C += A
		# pass<td><a href="#">Blah Blah</a></td>
	elif 'srtbl' in filename:        
		for i in range(len(data.index)):
			A="<tr><th>"+str(i+1)+"</th>"
			for j in range(len(data.columns)):
				A += "<td>"+str(data._get_value(i,data.columns[j]))+"</td>"
			A += "</tr>"
			C += A
	else:        
		for i in range(len(data.index)):
			A="<tr><th>"+str(i)+"</th>"
			for j in range(len(data.columns)):
				A += "<td>"+str(data._get_value(i,data.columns[j]))+"</td>"
			A += "</tr>"
			C += A
	html_content = f"<table> <thead> {B} </thead> <tbody> {C} </tbody> </table>"
	with open(filename, "w") as html_file:
		html_file.write(html_content)
		print("table html file created!")
 
def createdtcsv(zfilist, dtpath, user):
	k = 0
	labels={}
	# dictst = {'currvw': 0}
	sptFmt = ['jpg', 'png']
	with open(dtpath, 'a') as f:
		writer = csv.writer(f)
		writer.writerow(['item', 'filetype', 'label'])
		for item in zfilist:
			fields = []
			_, f_type = os.path.splitext(item)
			path = os.path.normpath(item)
			label1 = path.split(os.sep)[-2]
			if f_type[1:] in sptFmt:
				k += 1
				fields.append(item)
				fields.append(f_type[1:])
				fields.append(label1)
				writer.writerow(fields)
				if label1 in labels:
					labels[label1] +=1
				else:
					labels[label1] = 1
	obj = Usersessn.objects.get(user=user)
	obj.metadata ['numitems']= k
	obj.metadata ['labels']= labels
	obj.metadata['currvw']= 0
	obj.metadata['dtsloc'] = dtpath
	obj.save()
	


def searchkaggle(keywords, user):
	os.system('rm /home/pt/s3-bucket/MLWB/'+user+'/csvdts.zip')   	  
	s1 = os.popen('kaggle datasets list -s '+keywords).read().splitlines()
	print('test')
	print(s1[0])
	header1 = s1[0].split()
	print(header1)
	df = pd.DataFrame(columns=header1)
	for x in range(len(s1[2:])):
		data1 = s1[x+2].split('  ')
		data1 = [k.strip() for k in data1]
		data1 = list(filter(None, data1))
		df.loc[len(df)] = data1 
	   
	itemlist = df['ref'].tolist()
	tblpath=templtdir+user+'/srtbl.html'
	tblhtml(df,tblpath)
	obj = Usersessn.objects.get(user=user)
	obj.sritems = itemlist
	obj.save()
	# print(obj.sritems)


def dldkaggle(dtref, user):    
	os.system('rm '+bucket+user+'/processdt/*.*')
	os.system('cd '+bucket+user+'/processdt && kaggle datasets download -d '+dtref)
	dtfile = os.popen(
		'ls '+bucket+user+'/processdt').read().splitlines()
	dtpath = os.path.join(
		bucket+user+'/processdt', str(dtfile[0]))
	with zipfile.ZipFile(dtpath, 'r') as f:
		zfilist = f.namelist()
	if len(zfilist) == 1:
		os.system('mv '+bucket+user+'/processdt/*.*'+' '+bucket+user+'/csvdts.zip')
		dtpath = bucket+user+'/csvdts.zip'
		tblpath=templtdir+user+'/dtprv.html'
		df = pd.read_csv(dtpath)
		obj = Usersessn.objects.get(user=user)
		obj.metadata['currvw']=0
		obj.metadata['numitems']=len(df.index)
		obj.metadata['labels'] = df.nunique(axis=0).to_dict()
		obj.metadata['dtsloc'] = dtpath
		obj.save()		
	else:
		f_pnm, _ = os.path.splitext(str(dtfile[0]))
		dtpath = bucket+user+'/csvimg.csv'
		createdtcsv(zfilist, dtpath, user)
		tblpath=templtdir+user+'/imdtsprv.html'
	df = pd.read_csv(dtpath, nrows=50)
	# tblpath=templtdir+user+'/dtprv.html'
	tblhtml(df,tblpath)

def imgprv(scroll, user):
	obj = Usersessn.objects.get(user=user)
	if scroll == 'down':
		obj.metadata['currvw'] += 1
	if scroll == 'up':
		obj.metadata['currvw'] -= 1
	obj.save()
	dtpath = bucket+user+'/csvimg.csv'
	# print('start delay)')
	df = pd.read_csv(dtpath)
	
	idx = df['item'].iloc[obj.metadata['currvw']]
	label = df['label'].iloc[obj.metadata['currvw']]
	# print('end delay)')
	dtfile = os.popen(
		'ls '+bucket+user+'/processdt').read().splitlines()
	zipath = os.path.join(
		bucket+user+'/processdt', str(dtfile[0]))
	
	with zipfile.ZipFile(zipath, 'r') as f:
		ifile = f.open(idx)
		img = Image.open(ifile)
	imgdict = {}
	imgdict['label'] = label
	imgdict['imagepath'] = idx
	imgdict['width'], imgdict['height'] = img.size
	obj.currimage = imgdict
	obj.save()    
	output = io.BytesIO()
	img.save(output, format="PNG")
	output.seek(0)
	str_equivalent_image = base64.b64encode(output.getvalue()).decode()

	img_tag = "<img src='data:image/png;base64," + \
		str_equivalent_image + "' width='960' height='720'/>"
	imgpath1 = templtdir+user+'/imgprv.html'
	wrhtml("preview", img_tag, imgpath1)


def tblprv(scroll, user, dtpath, tblpath):
	obj = Usersessn.objects.get(user=user)
	print(50*obj.metadata['currpg'])
	if scroll == 'down':
		obj.metadata['currpg'] += 1
		obj.save()
	if scroll == 'up':
		if obj.metadata['currpg'] > 0:
			obj.metadata['currpg'] -= 1                     
			obj.save()

	# dtpath = bucket+user+'/csvdts.zip'
	df = pd.read_csv(dtpath, skiprows=range(1, 50*obj.metadata['currpg']), nrows=50)
	tblhtml(df,tblpath)
