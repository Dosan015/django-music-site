from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.db import IntegrityError



from .utils import get_file_upload_path, get_cover_upload_path
from .manager import SearchManager
from slugify import slugify


class Art(models.Model):
    name = models.CharField(_('Name'),max_length=30)

    class Meta:
        verbose_name = 'Art'
        verbose_name_plural = 'Art'
        ordering = ['name']


    def __str__(self):
          return self.name

class Person(models.Model):
    first_name = models.CharField(_('Firstname'),max_length=100)
    first_name_slug = models.SlugField(null=True, editable=False)
    last_name = models.CharField(_('Lastname'),max_length=100)
    last_name_slug = models.SlugField(null=True, editable=False)
    name = models.CharField(null=True, editable=False, max_length=200)
    name_slug = models.SlugField(null=True,editable=False, unique=True,)
    art = models.ManyToManyField('Art', verbose_name='Art')
    img = models.ImageField(_('Image'),upload_to=get_cover_upload_path, 
                            default=settings.DEFAULT_ARTIST_IMAGE)

    objects = SearchManager()

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'
        ordering = ['name']


    def get_absolute_url(self):
        poet = [val for val in self.art.all() if val.name == 'Poet']
        composer = [val for val in self.art.all() if val.name == 'Composer']
        if poet:
            return reverse('poet',kwargs={'first_name_slug': self.first_name_slug,'last_name_slug':self.last_name_slug })
        elif composer:
            return reverse('composer',kwargs={'first_name_slug': self.first_name_slug,'last_name_slug':self.last_name_slug })
        return reverse('singer',kwargs={'name_slug': self.name_slug })

    def save(self, *args, **kwargs):
        self.first_name_slug = slugify(self.first_name,replacements=[['ә','a'],['Ә', 'A']] ) # slug for kazakh language
        self.last_name_slug = slugify(self.last_name,replacements=[['ә','a'],['Ә', 'A']] )
        self.name = self.first_name +' '+ self.last_name
        self.name_slug= self.first_name_slug + '-'+ self.last_name_slug
        super(Person, self).save(*args, **kwargs)


    def __str__(self):
          return "%s %s" % (self.first_name, self.last_name)



class GroupPerson(models.Model):
    name = models.CharField(_('Name'),max_length=50)
    name_slug = models.SlugField(null=True, editable=False, unique=True)
    group_person = models.ManyToManyField('Person',_('Members'), blank=True)
    img = models.ImageField(_('Image'),upload_to=get_cover_upload_path, 
                            default=settings.DEFAULT_ARTIST_IMAGE)

    objects = SearchManager()

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('singer',kwargs={'name_slug': self.name_slug })

    def save(self, *args, **kwargs):
          self.name_slug = slugify(self.name,replacements=[['ә','a'],['Ә', 'A']] )
          super(GroupPerson, self).save(*args, **kwargs)


    def __str__(self):
          return self.name


class Singer(models.Model):
    group = models.OneToOneField('GroupPerson', null=True, blank=True, on_delete=models.CASCADE)
    person = models.OneToOneField('Person', null=True, blank=True, on_delete=models.CASCADE, 
                                            limit_choices_to={'art__name': 'Singer'})

    class Meta:
        verbose_name = 'Singer'
        verbose_name_plural = 'Singers'
        ordering = ('group__name','person__first_name')

    def group_or_person(self):
        if self.group is not None:
            return self.group
        return self.person

    def get_absolute_url(self):
        if self.group is not None:
            return self.group.get_absolute_url()
        return self.person.get_absolute_url()

    def __str__(self):
        if self.group:
            return self.group.__str__()
        return self.person.__str__()


class Audio(models.Model):
    file = models.FileField(_('mp3 file'), upload_to=get_file_upload_path, blank=True, 
                                           validators=[FileExtensionValidator(allowed_extensions=['mp3',''])])
    name = models.CharField(_('Name'),max_length=100)
    name_slug = models.SlugField(null=True, editable=False)
    singer = models.ForeignKey('Singer', verbose_name=_('Singer'),on_delete=models.CASCADE, related_name='singer')
    composer = models.ForeignKey('Person',verbose_name=_('Composer'), on_delete=models.CASCADE,blank=True,null=True, related_name='composer',
                                           limit_choices_to={'art__name': 'Composer'})
    poet = models.ForeignKey('Person', verbose_name=_('Poet'),on_delete=models.CASCADE, blank=True,null=True, related_name='poet',
                                       limit_choices_to={'art__name': 'Poet'} )
    img = models.ImageField(_('Image'),upload_to=get_cover_upload_path, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    min = models.CharField(_('Minute'),max_length=5, null=True, blank=True)
    count = models.PositiveIntegerField(default=0, editable=False )# download count
    size = models.IntegerField(default=0, null=True, blank=True)
    full_name_slug = models.SlugField(null=True,editable=False, unique=True)

    objects = SearchManager()

    class Meta:
         verbose_name = 'Song'
         verbose_name_plural = 'Songs'
         ordering = ['-id']
    
    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name,replacements=[['ә','a'],['Ә', 'A']] )
        self.full_name_slug = slugify(self.singer.__str__(), self.name, replacements=[['ә','a'],['Ә', 'A']] ) +'_' + self.name_slug
        super(Audio, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('song',kwargs={'name_slug': self.full_name_slug })


    def __str__(self):
        if self.singer.person:
            return "%s - %s" % (self.singer.person.__str__(), self.name)
        return "%s - %s" % (self.singer.group.__str__(), self.name)


class PlayList(models.Model):
    name = models.CharField(_('Name'),max_length=50)
    name_slug = models.SlugField(null=True, editable=False,unique=True)
    img = models.ImageField(_('Image'),upload_to=get_cover_upload_path, 
                            default=settings.DEFAULT_ARTIST_IMAGE)
    audios = models.ManyToManyField(Audio, verbose_name=_('Songs'),related_name='audio')

    objects = SearchManager()

    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('playlist',kwargs={'name_slug': self.name_slug })

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name,replacements=[['ә','a'],['Ә', 'A']] )
        super(PlayList, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


