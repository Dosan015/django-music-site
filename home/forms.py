from django import forms

from slugify import slugify
from .models import Person, Audio, GroupPerson, PlayList



class PersonForm(forms.ModelForm):
    def clean(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        value = first_name +' '+ last_name
        first_name_slug = slugify(first_name,replacements=[['ә','a'],['Ә', 'A']] )
        last_name_slug = slugify(last_name,replacements=[['ә','a'],['Ә', 'A']] )
        name_slug= first_name_slug + '-'+ last_name_slug
        if Person.objects.filter(name_slug=name_slug).exists():
            raise forms.ValidationError('%(value)s already exists. ', params={'value': value},)


class AudioForm(forms.ModelForm):
    def clean(self):
        singer = self.cleaned_data['singer']
        name = self.cleaned_data['name']
        value = singer.__str__() +' '+ name
        singer_slug = slugify(singer.__str__(),replacements=[['ә','a'],['Ә', 'A']] )
        name_slug = slugify(name,replacements=[['ә','a'],['Ә', 'A']] )
        name_slug= singer_slug + '_'+ name_slug
        if Audio.objects.filter(full_name_slug=name_slug).exists():
            raise forms.ValidationError('%(value)s already exists. ', params={'value': value},)


class GroupPersonForm(forms.ModelForm):
    def clean(self):
        name = self.cleaned_data['name']
        name_slug = slugify(name,replacements=[['ә','a'],['Ә', 'A']] )
        
        if GroupPerson.objects.filter(name_slug=name_slug).exists():
            raise forms.ValidationError('%(value)s already exists. ', params={'value': name},)


class PlayListForm(forms.ModelForm):
    def clean(self):
        name = self.cleaned_data['name']
        name_slug = slugify(name,replacements=[['ә','a'],['Ә', 'A']] )

        if PlayList.objects.filter(name_slug=name_slug).exists():
            raise forms.ValidationError('%(value)s already exists. ', params={'value': name},)


