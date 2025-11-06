from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(SESSION)
class SESSIONAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'title', 'tpic', 'session_day', 'start_time', 'end_time', 'room', 'created_at', 'updated_at')
    search_fields = ('title', 'tpic', 'room')
    list_filter = ('session_day', 'conference')
    date_hierarchy = 'session_day'
    readonly_fields = ('created_at', 'updated_at')

 