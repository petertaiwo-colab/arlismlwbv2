import csv, random, time
from .models import Testdata
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import cv2, urllib.request, os
import numpy as np

def data_gen():
    Testdata.objects.all().delete()
    x_value = 0
    total_1 = 1000
    total_2 = 200

    # fieldnames = ["x_value", "total_1", "total_2"]


    while True:
        with open('data.csv', 'a') as csv_file:
            obj = Testdata(item=x_value, costprice=total_1, sellprice=total_2)
            obj.save()
            # print(x_value, total_1, total_2)
            x_value += 1
            total_1 = total_1 + random.randint(-6, 8)
            total_2 = total_2 + random.randint(-5, 6)
        time.sleep(1)

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y1,y2):
    # os.system('rm /home/pt/ARLIS/ARLISDJ/MLWB/plot1.png')
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('live perf chart')
    plt.plot(x,y1, 'b-', label='x_c')
    plt.plot(x,y2, 'r-', label='x_p')
    plt.xticks(rotation=45)
    plt.xlabel('idx')
    plt.ylabel('val')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig('/home/pt/ARLIS/ARLISDJ/MLWB/performance/dynimgs/plot1.png')
    # filename = get_and_replace_filename('plot1')
    # print(filename)
    # plt.savefig(filename)
    graph = get_graph()
    return graph

#     line1, = plt.plot(t, np.sin(t * 2 * np.pi), 'b-', label='$sin(t)$')
# line2, = plt.plot(t, np.cos(t * 2 * np.pi/2), 'r--', label='$sin(t)$')
# line3, = plt.plot(t, (np.sin(t * 2 * np.pi))**2, 'k.-', label='$sin(t)$')

# plt.legend(loc='upper right')

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

class IPWebCam(object):
    def __init__(self):
        self.url = "http://192.168.1.205:8080/shot.jpg"

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        imgResp = urllib.request.urlopen(self.url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, 1)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

class Graph1(object):
    def __init__(self):
        self.plot1 = "/home/pt/ARLIS/ARLISDJ/MLWB/performance/dynimgs/plot1.png"

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        with open(self.plot1, "rb") as image:
            f = image.read()
        # print(len(f))
        imgNp = np.array(bytearray(f), dtype=np.uint8)
        img = cv2.imdecode(imgNp, 1)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

        # with open("img.png", "rb") as image:
        # f = image.read()
        # b = bytearray(f)
        # print b[0]
# def get_and_replace_filename(prefix):
#     dyndir='/home/pt/ARLIS/ARLISDJ/MLWB/performance/dynimgs/'
#     new_graph_name = prefix + str(time.time()) + '.png'
#     for filename in os.listdir(dyndir):
#         if filename.startswith(prefix):  # not to remove other images
#             os.remove(dyndir + filename)

#     return (dyndir + new_graph_name)