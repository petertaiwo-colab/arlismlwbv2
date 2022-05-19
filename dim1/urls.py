from django.urls import path, include
from . import views
# path('dtdload/', views.dtdload, name='dtdload'),

urlpatterns = [
    path('dim1/', views.dim1home, name='dim1home'),
    path('trainmdl/', views.trainmdl, name='trainmdl'),
    path('copyurl/<str:whcnb>/', views.copyurl, name='copyurl'),

]