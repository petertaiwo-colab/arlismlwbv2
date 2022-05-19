import cv2, csv
import numpy as np

def annot(imagepath):
    # #image_path
    # img_path="/home/pt/ARLIS/ARLISDJ/MLWB/s3-bucket/MLWB/petai1test/images/2732711a0d6000b9e1f5b7.jpg"

    #read image
    img_raw = cv2.imread(imagepath)

    #select ROIs function
    ROIs = cv2.selectROIs("Select Rois",img_raw)
    with open(imagepath[:-3]+'csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['width', 'height', 'left', 'top'])
        # df = pd.read_csv(imgdir[:-7]+'visionimages.csv')
                
        for item in ROIs:            
            print (item)
            writer.writerow([item[0], item[1], item[2], item[3]])
					
annot("/home/pt/ARLIS/ARLISDJ/MLWB/s3-bucket/MLWB/petai1test/images/2732711ba470008722b054.jpg")

# #print rectangle points of selected roi
# print(ROIs)