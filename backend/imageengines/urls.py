from django.urls import path
from . import views

app_name = 'imageengines'

urlpatterns = [
    path('upload/', views.engine, name='image'),
    path('training/',views.training, name='training')
]
