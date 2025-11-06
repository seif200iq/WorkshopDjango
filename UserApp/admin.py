from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(ORGANIZINGCOMITEE)
class ORGANIZINGCOMITEEAdmin(admin.ModelAdmin):
    list_display = ('user', 'commitee_role', 'join_date', 'created_at', 'updated_at')
    search_fields = ('user', 'commitee_role')
    list_filter = ('commitee_role', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
@admin.register(USER)
class USERAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'affiliation', 'role', 'email', 'created_at', 'updated_at')
    search_fields = ('user_id', 'first_name', 'last_name', 'affiliation', 'role', 'email')
    list_filter = ('role', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')