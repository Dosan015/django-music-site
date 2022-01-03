from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.list import ListView
from django.http import StreamingHttpResponse
from django.conf import settings
# from django.views.decorators.cache import cache_page

import urllib, mimetypes
from itertools import chain
import requests

from .models import Audio, GroupPerson, Person, PlayList, Singer



class Index(ListView):
   paginate_by = 30
   model = Audio
   template_name = 'home/index.html'

   def get_queryset(self):
       queryset = Audio.objects.select_related('singer','singer__person','singer__group','poet', 'composer').all()
       return queryset


   def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['page_title']= 'Қазақша әндер'
        context['active'] = 'home'
        return context
#@cache_page(60*180)
def song(request,name_slug):
   try:
      song = Audio.objects.get(full_name_slug=name_slug)
      page_title = song.__str__()
      singer = song.singer.group_or_person()
      audios = Audio.objects.filter(singer=song.singer).exclude(pk=song.pk)
   except Audio.DoesNotExist:
      raise Http404

   context = {
      'page_title': page_title,
      'singer':singer,
      'audio':song,
      'active': 'song'
      }
   current_page = Paginator(audios, 21)
   context['paginator'] = current_page
   page = request.GET.get('page')
   try:
      context['objects'] = current_page.page(page)
   except PageNotAnInteger:
      context['objects'] = current_page.page(1)
   except EmptyPage:
      context['objects'] = current_page.page(current_page.num_pages)

   return render(request, 'home/song.html', context)


def singer(request, name_slug):
   try:
      singer = Person.objects.filter(art__name='Singer').get(name_slug=name_slug)
      page_title = singer.__str__()
      audios = Audio.objects.filter(singer__person=singer)
   except Person.DoesNotExist:
       try:
           group =GroupPerson.objects.get(name_slug=name_slug)
           page_title = group.__str__()
           singer = group
           audios = Audio.objects.filter(singer__group=singer)
       except GroupPerson.DoesNotExist:
           raise Http404
   context = {
      'page_title': page_title,
      'singer': singer,
      'singer': singer
   }
   
   current_page = Paginator(audios, 21)
   context['paginator'] = current_page
   page = request.GET.get('page')
   try:
      context['objects'] = current_page.page(page)
   except PageNotAnInteger:
      context['objects'] = current_page.page(1)
   except EmptyPage:
      context['objects'] = current_page.page(current_page.num_pages)

   return render(request, 'home/singer.html', context)


def poet(request, first_name_slug,last_name_slug):
   try:
      poet = Person.objects.get(first_name_slug=first_name_slug, 
                                                            last_name_slug=last_name_slug)
      page_title = poet.__str__()
      audios = Audio.objects.filter(poet__id=poet.id) 
   except Person.DoesNotExist:
      raise Http404
   context = {
      'page_title': page_title,
      'poet': poet, 
      'active': 'poet'
      }
   
   current_page = Paginator(audios, 21)
   context['paginator'] = current_page
   page = request.GET.get('page')
   try:
      context['objects'] = current_page.page(page)
   except PageNotAnInteger:
      context['objects'] = current_page.page(1)
   except EmptyPage:
      context['objects'] = current_page.page(current_page.num_pages)

   return render(request, 'home/poet.html', context)


def composer(request, first_name_slug,last_name_slug):
   try:
      composer = Person.objects.get(first_name_slug=first_name_slug, 
                                                                     last_name_slug=last_name_slug)
      page_title = composer.__str__()
      audios = Audio.objects.filter(composer=composer)
   except Person.DoesNotExist:
      raise Http404

   context = {
      'page_title': page_title,
      'composer': composer, 
      'active': 'composer'
      }

   current_page = Paginator(audios, 21)
   context['paginator'] = current_page
   page = request.GET.get('page')
   try:
      context['objects'] = current_page.page(page)
   except PageNotAnInteger:
      context['objects'] = current_page.page(1)
   except EmptyPage:
      context['objects'] = current_page.page(current_page.num_pages)
   
   return render(request, 'home/composer.html', context)



class AllSinger(ListView):
   paginate_by = 30
   model = Singer
   template_name = 'home/all_singer.html'
   allow_empty = False

   def get_context_data(self, **kwargs):
        context = super(AllSinger, self).get_context_data(**kwargs)
        context['page_title']= 'Әншілер'
        context['active'] = 'singer'
        return context

class AllComposer(ListView):
   paginate_by = 30
   model = Person
   template_name = 'home/all_composer.html'
   allow_empty = False

   def get_queryset(self):
       queryset = Person.objects.filter(art__name='Composer')
       return queryset

   def get_context_data(self, **kwargs):
        context = super(AllComposer, self).get_context_data(**kwargs)
        context['page_title'] = 'Композиторлар'
        context['active'] = 'composer'
        return context

class AllPoet(ListView):
   paginate_by = 30
   model = Person
   template_name = 'home/all_poet.html'
   allow_empty = False

   def get_queryset(self):
       queryset = Person.objects.filter(art__name='Poet')
       return queryset

   def get_context_data(self, **kwargs):
        context = super(AllPoet, self).get_context_data(**kwargs)
        context['page_title'] = 'Ақындар'
        context['active'] = 'poet'
        return context

class AllPlaylist(ListView):
   paginate_by = 21
   model = PlayList
   template_name = 'home/all_playlist.html'
   allow_empty = False

   def get_context_data(self, **kwargs):
        context = super(AllPlaylist, self).get_context_data(**kwargs)
        context['page_title'] = 'Плейлисттер'
        context['active'] = 'playlist'
        return context


def playlist(request, name_slug):
   try:
      list = PlayList.objects.get(name_slug=name_slug)
      page_title = list.__str__()
      audios = list.audios.all()
   except PlayList.DoesNotExist:
      Http404
   contex = {
      'page_title': page_title,
      'list': list,
      'audios': audios,
      'activ': 'playlist'
      }
   return render(request, 'home/playlist.html', contex)


def search(request):
   context = {
           'active':'search'
           }

   if request.method == 'POST':
      q = request.POST['q']
      query_sets = []
      query_sets.append(Audio.objects.search(query=q))
      query_sets.append(GroupPerson.objects.search(query=q))
      query_sets.append(Person.objects.search(query=q))
      query_sets.append(PlayList.objects.search(query=q))
 
      final_set = list(chain(*query_sets))
      final_set.sort(key=lambda x: x.name, reverse=True)
 
      context['last_question'] = '%s' %q
 
      current_page = Paginator(final_set, 30)
      context['paginator'] = current_page
 
      page = request.GET.get('page')
      try:
         context['object_list'] = current_page.page(page)
      except PageNotAnInteger:
         context['object_list'] = current_page.page(1)
      except EmptyPage:
         context['object_list'] = current_page.page(current_page.num_pages)
      return render(request, 'home/search_results.html', context)

   q = request.GET.get('q')
   if q:
      query_sets = []
      query_sets.append(Audio.objects.search(query=q))
      query_sets.append(GroupPerson.objects.search(query=q))
      query_sets.append(Person.objects.search(query=q))
      query_sets.append(PlayList.objects.search(query=q))
 
      final_set = list(chain(*query_sets))
      final_set.sort(key=lambda x: x.name, reverse=True)
 
      context['last_question'] = '%s' %q
 
      current_page = Paginator(final_set, 30)
 
      page = request.GET.get('page')
      try:
         context['object_list'] = current_page.page(page)
      except PageNotAnInteger:
         context['object_list'] = current_page.page(1)
      except EmptyPage:
         context['object_list'] = current_page.page(current_page.num_pages)

   return render(request, 'home/search_results.html', context)



def download(request, name_slug):
   try:
      song = Audio.objects.get(full_name_slug=name_slug)
      # https://selectel.ru/ cloud
      if settings.IS_SELECTEL_STORAGES:
         r = requests.get(song.file.url, stream=True)
         response = StreamingHttpResponse(streaming_content=r.raw)
      else:
         fp = open(str(settings.BASE_DIR) + song.file.url, 'rb') 
         response = HttpResponse(fp.read()) 
         fp.close() 
         #file_path = str(settings.BASE_DIR) + song.file.url
      original_filename = song.__str__() +'.mp3'
      type, encoding = mimetypes.guess_type(original_filename)
      if type is None:
         type = 'application/octet-stream'
      response['Content-Type'] = type
      response['Content-Length'] = song.size
      if encoding is not None:
         response['Content-Encoding'] = encoding # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/ 
      if u'WebKit' in request.META['HTTP_USER_AGENT']:
         # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly. 
         filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(original_filename.encode('utf-8').decode('utf-8'))
      elif u'MSIE' in request.META['HTTP_USER_AGENT']:
         # IE does not support internationalized filename at all. 
         # It can only recognize internationalized URL, so we do the trick via routing rules. 
         filename_header = ''
      else:
         # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers). 
         filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(original_filename.encode('utf-8').decode('utf-8'))
      response['Content-Disposition'] = 'attachment; ' + filename_header

      Audio.objects.filter(pk=song.id).update(count=F('count')+1)
      return response
   except Audio.DoesNotExist:
      raise Http404
