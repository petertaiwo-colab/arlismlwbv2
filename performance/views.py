from django.http.response import StreamingHttpResponse
from django.shortcuts import render
from .utils import data_gen, get_plot, VideoCamera, IPWebCam, Graph1
from .matgraph import plotgraph
from .models import Testdata
import cv2, base64, codecs, time
import numpy as np

# Create your views here.

def perfhome(request):
    data_gen()
    return render(request, 'perf/perfhome.html')

def plot(request):
    qs = Testdata.objects.all()
    x = [x.item for x in qs]
    y1 = [y1.costprice for y1 in qs]
    y2 = [y2.sellprice for y2 in qs]
    chart = get_plot(x, y1, y2)
    return render(request, 'perf/perfhome.html', {'chart': chart})

def liveindex(request):
    return render(request, 'perf/streamgraph.html')

# really camera or mimicking a camera !
def gen(camera):
    while True: 
        qs = Testdata.objects.all()
        x = [x.item for x in qs]
        y1 = [y1.costprice for y1 in qs]
        y2 = [y2.sellprice for y2 in qs]
        get_plot(x, y1, y2)
        frame = camera.get_frame()
        # print(len(frame))
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'r\n\r\n')

def liveplot(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type = 'multipart/x-mixed-replace; boundary=frame')

def webcam(request):
    return StreamingHttpResponse(gen(IPWebCam()),
                    content_type = 'multipart/x-mixed-replace; boundary=frame')

def livegraph1(request):
    return StreamingHttpResponse(gen(Graph1()),
                    content_type = 'multipart/x-mixed-replace; boundary=frame')

