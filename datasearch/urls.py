from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from vision import views as uploader_views
# path('dtdload/', views.dtdload, name='dtdload'),

# app_name = "datasearch"

urlpatterns = [    
    # path('', views.index, name='index'),
    path('vision/', views.dtsethome, name='dtsethome'),
    path('index1/', views.index1, name='index1'),
    # path('dtwindow/', views.dtwindow, name='dtwindow'),
    path('dtsearchrs/', views.dtsearchrs, name='dtsearchrs'),
    path('dtdload/', views.dtdload, name='dtdload'),
    path('dtsprv1/', views.dtsprv1, name='dtsprv1'),
    path('srchprv1/', views.srchprv1, name='srchprv1'),
    path('dspfrm/<str:dspwht>/', views.dspfrm, name='dspfrm'),
    path('clckvw/<str:dspwht>/', views.clckvw, name='clckvw'),
]