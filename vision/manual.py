import pandas as pd
import cv2

def mandetperson(imgpath):
    img = cv2.imread(imgpath)
    imgfilename = imgpath.split('/')[-1]
    response = []
    df = pd.read_csv("/home/pt/ARLIS/ARLISDJ/MLWB/vision/perstestimgs/csv/manual.csv")
    height, width, channels = img.shape

    # print (df.iterrows)
    # for index, row in df.iterrows():
    #     print (row['personid'])

    for index, row in df.iterrows():
        if row['imagefile'] == imgfilename:

            print(row['imagefile'])
            print(row['personid'])
            pers = {}
            # width = 500
            # height = 500
            x, y, w, h = row['left'], row['top'], row['width'], row['height']
            pers['Width'] = w
            pers['Height'] = h
            pers['Left'] = x
            pers['Top'] = y                
            personBB = {'BoundingBox': pers, 'Confidence': row['confidence']}
            response.append(personBB)
    return response

# response = mandetperson('/home/pt/ARLIS/ARLISDJ/MLWB/vision/perstestimgs/images/2732711ba470008722b054.jpg')
# print(response)