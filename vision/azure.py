from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.storage.blob import BlobServiceClient
import os, uuid, sys, json, cv2
import validators, requests, shutil

key = "2429f3cb34784725accd94084cdc775f"
endpoint = "https://test222pet2020.cognitiveservices.azure.com/"
client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

def azudetperson(imagepath, imgname):
    print(imagepath+'imgpath in azu n name '+imgname)
    img = cv2.imread(imagepath)
    height, width, channels = img.shape
    print(str(height)+' h and w '+str(width))
    # os.system('rm /home/pt/s3-bucket/MLWB/images/azuperf/*')
    # os.system('cp '+imagepath+' /home/pt/s3-bucket/MLWB/images/azuperf/')
    image_url='https://mlwb-bucket.s3.amazonaws.com/MLWB/images/azuperf/'+imgname
    print(image_url+' img url')
    response = client.detect_objects(image_url)
    print(response)
    azresponse = []
    for object in response.objects:
        print("{} detected at location {}, {}, {}, {}".format( \
        object.object_property, object.rectangle.x, object.rectangle.x + object.rectangle.w, \
        object.rectangle.y, object.rectangle.y + object.rectangle.h))

    for object in response.objects:
        if object.object_property == 'person':
            pers = {}
            # x, y, w, h = boxes[i]
            pers['Width'] = object.rectangle.w / width
            pers['Height'] = object.rectangle.h / height
            pers['Left'] = object.rectangle.x / width
            pers['Top'] = object.rectangle.y / height                
            personBB = {'BoundingBox': pers, 'Confidence': object.confidence*100}
            azresponse.append(personBB)
# response = client.detect_objects(image_url)
    print(azresponse)
    return azresponse