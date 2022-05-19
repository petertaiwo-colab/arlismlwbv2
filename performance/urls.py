from django.urls import path, include
from . import views
# path('dtdload/', views.dtdload, name='dtdload'),

urlpatterns = [
    path('perf/', views.perfhome, name='perfhome'),
    path('plot/', views.plot, name='plot'),
    path('liveindex/', views.liveindex, name='liveindex'),
    path('liveplot/', views.liveplot, name='liveplot'),
    path('webcam/', views.webcam, name='webcam'),
    path('livegraph1/', views.livegraph1, name='livegraph1'),
    # path('trainmdl/', views.trainmdl, name='trainmdl'),
    # path('copyurl/<str:whcnb>/', views.copyurl, name='copyurl'),

]