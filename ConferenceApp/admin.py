from django.contrib import admin
from .models import Conferance, Submission
# Register your models here.
admin.site.site_title="Gestion Conference 25/26"
admin.site.site_header="Gestion Conference"
admin.site.index_title="django app conférence"
admin.site.register(Conferance)
admin.site.register(Submission)
