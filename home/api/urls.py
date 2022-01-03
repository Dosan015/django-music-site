from django.urls import include, path
from . import views


urlpatterns = [
    path('audio-list/', views.AudioList.as_view(), name='audio-list'),
    path('audio-detail/<pk>', views.audioDetail, name='audio-detail'),
]
