from .models import Visionuser
import pandas as pd
import os, cv2
import json
import zipfile
import csv
import base64
import io
from PIL import Image
from .rekognition import rekdetperson
from .azure import azudetperson
from .yolo import yoldetperson
from .manual import mandetperson
from .perf import f1score
import matplotlib.pyplot as plt
from io import BytesIO

def perfmetrics(imgdir, gtruth, yolo, azure, rekognition):
	Yolscore, TPimg = f1score(imgdir, gtruth, yolo)
	Rekscore, TPimg = f1score(imgdir, gtruth, rekognition)
	Azuscore, TPimg = f1score(imgdir, gtruth, azure)
	print(Yolscore)
	print(Rekscore)
	print(str(Azuscore)+'azuscore')
	return Yolscore, Azuscore, Rekscore, TPimg
	#next plot the scores


def wrhtml(head, body, filename):
	html_content = f"<html> <head><div> {head} </div></head> <body> {body} </body> </html>"
	with open(filename, "w") as html_file:
		html_file.write(html_content)
		print("html file created!")

def tblhtml(data, filename):
    B="<tr><th></th>"
    for col in data.columns:
        B += "<th>"+col+"</th>"
    B += "</tr>"
    C = ""
    # if 'imdtsprv' in filename:
    for i in range(len(data.index)):
        A="<tr><th>"+str(i)+"</th>"
        for j in range(len(data.columns)):
            if j==0:
                refl=str(data._get_value(i,data.columns[j]))
                A += "<td><a href='{% url 'imgvw' dspwht='"+str(i)+"' %}'>"+refl+"</a></td>"
            else:
                    A += "<td>"+str(data._get_value(i,data.columns[j]))+"</td>" 
        A += "</tr>"
        C += A
    html_content = f"<table class='table table-striped table-hover table-dark'> <thead> {B} </thead> <tbody> {C} </tbody> </table>"
    with open(filename, "w") as html_file:
        html_file.write(html_content)
        print("table html file created!")
    return html_content

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
			label1 = 'none'
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
	obj = Visionuser.objects.get(user=user)
	obj.metadata ['numitems']= k
	obj.metadata ['labels']= labels
	obj.metadata['currvw']= 0
	obj.metadata['dtsloc'] = dtpath
	obj.save()

def createcurrimagehtml(htmlpath, imagepath, BB, srcname):
	opencv_img = cv2.imread(imagepath)
	cv2.putText(opencv_img, srcname, (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
	imgheight, imgwidth = opencv_img.shape[:2]
    # Perform Annotations
	if len(BB) !=0:
		for person in BB['personid']:			
			BBrow = BB.loc[BB['personid']==person]
			# print('draw with '+BBrow)
			print('Person'+str(person)+'  confd'+str(int(BBrow['confidence'])))
			bxheight, bxwidth = imgheight*BBrow['height'], imgwidth*BBrow['width']
			cv2.rectangle(opencv_img, (int(imgwidth*BBrow['left']),int(imgheight*BBrow['top'])),
                (int(imgwidth*BBrow['left']+bxwidth),int(imgheight*BBrow['top']+bxheight)),(0, 255, 0), 2)
			cv2.putText(opencv_img, 'ps-'+str(person)+' .'+str(int(BBrow['confidence'])), (int(imgwidth*BBrow['left']),int(imgheight*BBrow['top'])), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (127,0,255), 1)
	color_converted = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2RGB)
	img = Image.fromarray(color_converted)
	print("CV2 to PIL done")
	    
	output = io.BytesIO()
	img.save(output, format="PNG")
	output.seek(0)
	str_equivalent_image = base64.b64encode(output.getvalue()).decode()

	img_tag = "<img src='data:image/png;base64," + \
		str_equivalent_image + "' width='960' height='720'/>"
	header ="<a href="+'"'+"{% url 'imagelist' %}"+'"'+">Back to Image list</a>"
	wrhtml(header, img_tag, htmlpath)
	
def persons(pltfm, imgdir, respath):
	# if pltfm == 'rekognition':
	# respath = resdir+pltfm+'detpers.csv'	
	print('csv of '+ pltfm+' result is in '+respath)
	if not os.path.isfile(respath):
		print('no results csv found : start detect persons')
		with open(respath, 'a') as f:
			writer = csv.writer(f)
			writer.writerow(['imagefile', 'personid', 'confidence', 'width', 'height', 'left', 'top'])
			df = pd.read_csv(imgdir[:-7]+'visionimages.csv')
					
			for item in df['item'].tolist():            
				print (item)
				if pltfm == 'rekognition':
					print(imgdir+item)
					response = rekdetperson(imgdir+item)

				elif pltfm == 'azure':
					response = azudetperson(imgdir+item, item)					
					
				elif pltfm == 'yolo':
					response = yoldetperson(imgdir+item)

				elif pltfm == 'groundtruth':
					response = mandetperson(imgdir+item)

				i=0
				for person in response:
					BB=person['BoundingBox']
					writer.writerow([item, i+1, person['Confidence'], BB['Width'], 
						BB['Height'], BB['Left'], BB['Top']])
					i+=1
					# print(json.dumps(response, indent=4))
					# print('..............................................')

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y1,y2,y3,pltpath,title,xlabel,ylabel,pltfm1,pltfm2,pltfm3):
    # os.system('rm /home/pt/ARLIS/ARLISDJ/MLWB/plot1.png')
    print(str(y2)+' y2')
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title(title)
    plt.plot(x,y1, 'b-', label=pltfm1)
    plt.plot(x,y2, 'r-', label=pltfm2)
    plt.plot(x,y3, 'g-', label=pltfm3)
    plt.xticks(rotation=45)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(pltpath)
    # filename = get_and_replace_filename('plot1')
    # print(filename)
    # plt.savefig(filename)
    graph = get_graph()
    return graph

def get_plot2(x,y1,y2,y3,y4,pltpath,title,xlabel,ylabel,pltfm1,pltfm2,pltfm3,pltfm4):
    # os.system('rm /home/pt/ARLIS/ARLISDJ/MLWB/plot1.png')
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title(title)	
    plt.plot(x,y1, 'b-', label=pltfm1)
    plt.plot(x,y2, 'r-', label=pltfm2)
    plt.plot(x,y3, 'g-', label=pltfm3)
    plt.plot(x,y4, 'k-', label=pltfm4)
    plt.xticks(rotation=45)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(pltpath)
    # filename = get_and_replace_filename('plot1')
    # print(filename)
    # plt.savefig(filename)
    graph = get_graph()
    return graph
