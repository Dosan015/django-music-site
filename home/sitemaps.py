from django.contrib.sitemaps import Sitemap
from .models import Audio, Singer, Person


class AudioSitemap(Sitemap):
    def items(self):
        return Audio.objects.all()

class SingerSitemap(Sitemap):
    def items(self):
        return Singer.objects.all()

class PoetSitemap(Sitemap):
    def items(self):
        return Person.objects.filter(art__name='Poet')


class ComposerSitemap(Sitemap):
    def items(self):
        return Person.objects.filter(art__name='Composer')
