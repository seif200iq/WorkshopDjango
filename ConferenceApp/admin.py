from django.contrib import admin
from .models import Conference, Submission,OrganizingCommittee
# Register your models here.
admin.site.site_title="Gestion Conference 25/26"
admin.site.site_header="Gestion Conférences"
admin.site.index_title="django app conférence"
# admin.site.register(Conference)
# admin.site.register(Submission)
# admin.site.register(OrganizingCommittee)

# Inline Tabular
class SubmissionTabularInline(admin.TabularInline):
    model = Submission
    extra = 1
    fields = ('submission_id', 'title', 'status', 'payed', 'submission_date', 'user')
    readonly_fields = ('submission_id', 'submission_date')


# Inline Stacked
class SubmissionStackedInline(admin.StackedInline):
    model = Submission
    extra = 1
    fields = ('submission_id', 'title', 'abstract', 'keywords', 'status', 
              'payed', 'paper', 'submission_date', 'user')
    readonly_fields = ('submission_id', 'submission_date')
    classes = ['collapse']

    
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


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submission_id', 'title', 'conference', 'get_user_info', 
                    'status', 'payed', 'submission_date')
    list_filter = ('status', 'payed', 'submission_date', 'conference')
    search_fields = ('title', 'abstract', 'keywords', 'submission_id', 
                     'user__username', 'user__email')
    readonly_fields = ('submission_id', 'submission_date', 'created_at', 'updated_at')
    ordering = ('-submission_date',)
    date_hierarchy = 'submission_date'
    
    fieldsets = (
        ('Informations de soumission', {
            'fields': ('submission_id', 'conference', 'user', 'submission_date')
        }),
        ('Contenu', {
            'fields': ('title', 'abstract', 'keywords', 'paper')
        }),
        ('Statut', {
            'fields': ('status', 'payed')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    @admin.display(description='Utilisateur', ordering='user__username')
    def get_user_info(self, obj):
        if obj.user:
            if hasattr(obj.user, 'first_name') and obj.user.first_name:
                return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
            return obj.user.username
        return "Non assigné"
    
    actions = ['mark_as_accepted', 'mark_as_rejected', 'mark_as_payed']
    
    @admin.action(description='✓ Marquer comme accepté')
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f"{updated} soumission(s) acceptée(s).")
    
    @admin.action(description='✗ Marquer comme rejeté')
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} soumission(s) rejetée(s).")
    
    @admin.action(description='€ Marquer comme payé')
    def mark_as_payed(self, request, queryset):
        updated = queryset.update(payed=True)
        self.message_user(request, f"{updated} paiement(s) enregistré(s).")

