from django.contrib import admin
from .models import Conference, Submission,OrganizingCommittee
# Register your models here.
admin.site.site_title="Gestion Conference 25/26"
admin.site.site_header="Gestion Conférences"
admin.site.index_title="django app conférence"
# admin.site.register(Conference)
# admin.site.register(Submission)
# admin.site.register(OrganizingCommittee)

class SubmissionInline(admin.TabularInline):
    model = Submission
    extra=1
    readonly_fields=("submission_date",)


@admin.register(Conference)
class AdminConferenceModel(admin.ModelAdmin):
    list_display=("name","theme","start_date","end_date")
    ordering=("start_date","end_date")
    list_filter=("theme",)
    search_fields=("name","description",)
    date_hierarchy="start_date"
    fieldsets=(
        ("Information general", {
         "fields":("conference_id","name","theme","description")
         }),
         ("logistic info", {
             "fields":("location","start_date","end_date")
         })
    )
    readonly_fields = ("conference_id",) 
    

    def a(self,objet):
        if objet.start_date and objet.end_date :
            return(objet.end_date-objet.start_date).days
        return "rien a signaler"
    a.short_description="Description (days)"
    inlines=[SubmissionInline]