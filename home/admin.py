from django.contrib import admin
from django.conf import settings
from home.utils import mp3_tag_edit
from .models import Art, Person, GroupPerson, Singer, Audio, PlayList
from .forms import PersonForm, AudioForm, GroupPersonForm, PlayListForm

 


class AudioAdmin(admin.ModelAdmin):
    form = AudioForm

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        request.POST = request.POST.copy()
        if request.FILES.get('file'): # Edit tags 
            if request.POST.get('singer'):
                singer = Singer.objects.get(pk=request.POST.get('singer'))
            if request.FILES.get('img'):
                img = request.FILES.get('img').temporary_file_path()
            else:
                img = settings.DEFAULT_COVER_IMAGE
            file = request.FILES.get('file')
            title = request.POST.get('name')
            request.POST['size'] = file.size
            request.POST['min'] = mp3_tag_edit(file=file, img=img, title=title,singer=singer)
            
            
        return form

 

class PersonAdmin(admin.ModelAdmin):
    form = PersonForm

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    

    
class GroupPersonAdmin(admin.ModelAdmin):
    form = GroupPersonForm
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class SingerAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class PlaylistAdmin(admin.ModelAdmin):
    form = PlayListForm

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(Art)
admin.site.register(Person, PersonAdmin)
admin.site.register(GroupPerson, GroupPersonAdmin)
admin.site.register(Singer, SingerAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(PlayList, PlaylistAdmin)
