# from django.test import TestCase

# Create your tests here.
# from yolo import yoldetperson

# yoldetperson("/home/pt/ARLIS/ARLISDJ/MLWB/s3-bucket/MLWB/petai1test/images/2732711b86f000bc5b77bf.jpg")




# import csv

# with open('/home/pt/awskey.csv','r')as input:    
#     reader = csv.reader(input)
#     key = [x[0].split('=')[1] for x in reader]    
#     access_key_id = key[0]
#     secret_access_key = key[1]
# import os
# # os.system('cd /home/pt/darknet && ./darknet detect cfg/yolov4.cfg yolov4.weights data/person.jpg')
# s1 = os.popen('cd /home/pt/darknet && ./darknet detect cfg/yolov4.cfg yolov4.weights data/person.jpg  -ext_output').read()

# print(s1)
# import cv2
# import numpy as np

# Load Yolo
# net = cv2.dnn.readNet("/home/pt/OpenCVYolo/yolov3.weights", "/home/pt/OpenCVYolo/yolov3.cfg")
# # classes = ["person", "bicycle"]
# classes = []
# with open("/home/pt/OpenCVYolo/coco.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]
# print(classes)
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
# colors = np.random.uniform(0, 255, size=(len(classes), 3))

# # Loading image
# img = cv2.imread("/home/pt/OpenCVYolo/person.jpg")
# img = cv2.resize(img, None, fx=2, fy=2)

# height, width, channels = img.shape

# # Detecting object
# blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

# for b in blob:
#     for n, img_blob in enumerate(b):
#         cv2.imshow(str(n), img_blob)

# net.setInput(blob)
# outs = net.forward(output_layers)

# print(outs)

# # Showing the information on the screen
# class_ids = []
# confidences = []
# boxes = []
# for out in outs:
#     for detection in out:
#         scores = detection[5:]
#         class_id = np.argmax(scores)
#         confidence = scores[class_id]
#         if confidence > 0.5:
#             # object detected
#             center_x = int(detection[0] * width)
#             center_y = int(detection[1] * height)
#             w = int(detection[2] * width)
#             h = int(detection[3] * height) 
#             cv2.circle(img, (center_x, center_y), 10, (0, 255, 0), 2)

#             # Rectangle coordinates
#             x = int(center_x - w / 2)
#             y = int(center_y -h / 2)

#             boxes.append([x, y, w, h])
#             confidences.append(float(confidence))
#             class_ids.append(class_id)

#             # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# print(len(boxes))
# number_obj_detected = len(boxes)

# indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
# print(indexes)

# font = cv2.FONT_HERSHEY_PLAIN
# for i in range(len(boxes)):
#     if i in indexes:
#         x, y, w, h = boxes[i]
#         label = str(classes[class_ids[i]])
#         color = colors[i]
#         cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
#         cv2.putText(img, label, (x, y + 30), font, 2, color, 3)
# cv2.imshow("Image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


import cv2
import numpy as np

 #image_path
img_path="/home/pt/ARLIS/ARLISDJ/MLWB/s3-bucket/MLWB/petai1test/images/2732711a0d6000b9e1f5b7.jpg"

#read image
img_raw = cv2.imread(img_path)

#select ROIs function
ROIs = cv2.selectROIs("Select Rois",img_raw)

#print rectangle points of selected roi
print(ROIs)

#Crop selected roi ffrom raw image

#counter to save image with different name
crop_number=0 

#loop over every bounding box save in array "ROIs"
for rect in ROIs:
    x1=rect[0]
    y1=rect[1]
    x2=rect[2]
    y2=rect[3]

    img_crop=img_raw[y1:y1+y2,x1:x1+x2]

    cv2.imshow("crop"+str(crop_number),img_crop)

    cv2.imwrite("crop"+str(crop_number)+".jpeg",img_crop)
    crop_number+=1

#hold window
cv2.waitKey(0)