
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map/<str:city>/<str:rest_name>', views.map, name="map"),
    path('model/', views.model, name='model')
]
