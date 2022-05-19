import pandas as pd
import cv2

def f1score(imgdir, gtruth, yolo):
    print(imgdir+" for F1 score")
    dfimg = pd.read_csv(imgdir[:-7]+'visionimages.csv') 
    dftruth = pd.read_csv(gtruth) 
    dfyol = pd.read_csv(yolo)

    TParr = []
    TPimg =[]
    F1arr =[]
    for item in dfimg['item'].tolist():
        TP=0
        print(imgdir+item)
        img = cv2.imread(imgdir+item)
        height, width, channels = img.shape

        ElimList=[]
        for index, row in dftruth.iterrows():
            Aovlp=0
            if row['imagefile'] == item:
                # print(row['imagefile'])
                # print(row['height'])
                Atruth = row['height']*row['width']
                # print('Atruth= '+str(Atruth))               
                
                for yindex, yrow in dfyol.iterrows():
                    if yrow['imagefile'] == item and yindex not in ElimList:                        
                        # print(ElimList)                        
                        if yrow['top']>row['top'] and yrow['top']<row['top']+row['height']:
                            if yrow['left']>row['left'] and yrow['left']<row['left']+row['width']:
                                Aovlp=min(yrow['width'],(row['width']-(yrow['left']-row['left'])))*min(yrow['height'],(row['height']-(yrow['top']-row['top'])))
                            if row['left']>yrow['left'] and row['left']<yrow['left']+yrow['width']:
                                Aovlp=((yrow['width']-(row['left']-yrow['left'])))*((row['height']-(yrow['top']-row['top'])))
                        if row['top']>yrow['top'] and row['top']<yrow['top']+yrow['height']:
                            if yrow['left']>row['left'] and yrow['left']<row['left']+row['width']:
                                # Aovlp=min(yrow['width'],(row['width']-(yrow['left']-row['left'])))*min(yrow['height'],(row['height']-(yrow['top']-row['top'])))
                                Aovlp=((row['width']-(yrow['left']-row['left'])))*((yrow['height']-(row['top']-yrow['top'])))
                            if row['left']>yrow['left'] and row['left']<yrow['left']+yrow['width']:
                                # Aovlp=((yrow['width']-(row['left']-yrow['left'])))*((row['height']-(row['top']-yrow['top'])))
                                Aovlp=min(row['width'],(yrow['width']-(row['left']-yrow['left'])))*min(row['height'],(yrow['height']-(row['top']-yrow['top'])))

                                # print('Aovlp='+str(Aovlp))
                    if Aovlp > Atruth*0.8:
                        TP+=1                                   
                        # print(Atruth)
                        # print(Aovlp)
                        # print(yrow['imagefile']+' check yolo')
                        # print(yrow['height'])
                        ElimList.append(yindex)
                        break
        print(TP)
        TParr.append(TP)
        TPimg.append(item)
        FN = len(dftruth[(dftruth['imagefile']==item)])-TP
        FP = len(dfyol[(dfyol['imagefile']==item)])-TP
        print(FN)
        print(FP)
        F1 = TP / (TP + (FP + FN)/2)
        print(F1)

        F1arr.append(F1)
    # print(TParr)
       
    print(TParr)
    print(TPimg)
    print(F1arr)    
        
    return F1arr, TPimg

# def mandetperson(imgpath):
#     img = cv2.imread(imgpath)
#     imgfilename = imgpath.split('/')[-1]
#     response = []
#     df = pd.read_csv("/home/pt/ARLIS/ARLISDJ/MLWB/vision/perstestimgs/csv/manual.csv")
#     height, width, channels = img.shape

#     # print (df.iterrows)
#     # for index, row in df.iterrows():
#     #     print (row['personid'])

#     for index, row in df.iterrows():
#         if row['imagefile'] == imgfilename:

#             print(row['imagefile'])
#             print(row['personid'])
#             pers = {}
#             # width = 500
#             # height = 500
#             x, y, w, h = row['left'], row['top'], row['width'], row['height']
#             pers['Width'] = w
#             pers['Height'] = h
#             pers['Left'] = x
#             pers['Top'] = y                
#             personBB = {'BoundingBox': pers, 'Confidence': row['confidence']}
#             response.append(personBB)
#     return response