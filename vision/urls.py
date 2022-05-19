from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from vision import views as uploader_views
# path('dtdload/', views.dtdload, name='dtdload'),

# app_name = "vision"

urlpatterns = [
    path('vision/', views.visionhome, name='visionhome'),
    path('imageai/', views.imageai, name='imageai'),
    path('upldimg/', views.upldimg, name='upldimg'),
    path('imgvw/<str:dspwht>/', views.imgvw, name='imgvw'),    
    path('imagelist/', views.imagelist, name='imagelist'),
    path('imgscroll/', views.imgscroll, name='imgscroll'),
    path('visionjob/', views.visionjob, name='visionjob'),
    path('perfpltimg/', views.perfpltimg, name='perfpltimg'),
    path('perfpltimg2/', views.perfpltimg2, name='perfpltimg2'),
    path('stdperftestpers/', views.stdperftestpers, name='stdperftestpers'),
    # path('', views.UploadView.as_view(), name='fileupload'),
    # path('trainmdl/', views.trainmdl, name='trainmdl'),
    # path('copyurl/<str:whcnb>/', views.copyurl, name='copyurl'),
]