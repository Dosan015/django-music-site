from django.db import models
from django.db.models import Q
 
class SearchManager(models.Manager):
    use_for_related_fields = True
 
    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(name__icontains=query.capitalize()) | Q(name_slug__icontains=query.capitalize()) 
                        | Q(name__icontains=query.lower()) | Q(name_slug__icontains=query.lower()))
            qs = qs.filter(or_lookup).order_by('name')
 
        return qs