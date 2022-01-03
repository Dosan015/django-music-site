from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from django.contrib.sitemaps.views import sitemap
from rest_framework.authtoken import views as drf_views
from home import urls as home_urls
from home.api import urls as api_urls
from home.sitemaps import AudioSitemap, SingerSitemap, PoetSitemap, ComposerSitemap


sitemaps = {
        'audio':AudioSitemap,
        'singer':SingerSitemap,
        'poet': PoetSitemap,
        'composer': ComposerSitemap,
        }

urlpatterns = [
    path('', include(home_urls)),
    path('api/', include(api_urls)),
    path('api/auth/', drf_views.obtain_auth_token),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

