from django.urls import path
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('singer/<name_slug>', views.singer, name='singer'),
    path('poet/<first_name_slug>_<last_name_slug>', views.poet, name='poet'),
    path('composer/<first_name_slug>_<last_name_slug>', views.composer, name='composer'),
    path('song/<name_slug>', views.song, name='song'),
    path('playlist/<name_slug>', views.playlist, name='playlist'),
    path('playlists/', views.AllPlaylist.as_view(), name='playlists'),
    path('search/', views.search, name='search'),
    path('singers/', views.AllSinger.as_view(), name='singers'),
    path('poets/', views.AllPoet.as_view(), name='poets'),
    path('composers/', views.AllComposer.as_view(), name='composers'),
    path('download/<name_slug>', views.download, name='download'),
]
