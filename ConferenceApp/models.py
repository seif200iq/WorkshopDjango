from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.crypto import get_random_string
from django.utils import timezone

def validate_keywords(value):
    mots = [mot.strip() for mot in value.split(',')]
    if len(mots) > 10:
        raise ValidationError("Vous ne pouvez pas avoir plus de 10 mots-clés.")
# Create your models here.
class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(validators=[
        MaxLengthValidator(30,"La description doit contenir au moins 30 caractères.")
    ]
    # description = models.TextField(validators=[
    #     MaxLengthValidator(30,"La description doit contenir au moins 30 caractères.")
    # ]


    )
    THEME =[
        ('CSAI', 'Computer Science & Artificial Intelligence'),
        ('SE', 'Science & Engineering'),
        ('SSE', 'Social Sciences & Education'),
        ('IT', 'Interdisciplinary Themes'),
    ]
    theme = models.CharField(max_length=225,choices=THEME)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"La conférenence a comme titre {self.name}"
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("la date de debut de la Conference doit etre anterieur a la date de fin")



class Submission(models.Model):
    submission_id = models.CharField(max_length=255,primary_key=True,unique=True)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    # keywords = models.TextField()
    keywords = models.TextField(validators=[validate_keywords])
    # papers = models.FileField(upload_to='paper/')
    paper = models.FileField(upload_to='paper/', validators=[FileExtensionValidator(['pdf'], "Le fichier doit être un .pdf")], blank=True, default='')
    STATUS =[
        ('submitted','submitted'),
        ('under review', 'under review'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected')
    ]
    status = models.CharField(max_length=50,choices=STATUS)
    payed = models.BooleanField(default=False)
    submission_date= models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('UserApp.USER',on_delete=models.CASCADE,related_name='submissions')
    conference = models.ForeignKey(Conference,on_delete=models.CASCADE,related_name='submissions')  
    def save(self, *args, **kwargs):
        if not self.submission_id:
            self.submission_id = "SUB" + get_random_string(8).upper()
        super().save(*args, **kwargs)

    def clean(self):
        #Vérifier que la soumission est faite avant le début de la conférence
        today = timezone.now().date()
        if self.conference.start_date:
          today = timezone.now().date()
          if self.conference.start_date <= today:
             raise ValidationError("La soumission ne peut être faite que pour des conférences à venir.")
        #Limiter à 3 soumissions par jour par utilisateur
        same_day_submissions = Submission.objects.filter(
            user=self.user,
            submission_date=today
        ).exclude(pk=self.pk).count()
        if same_day_submissions >= 3:
            raise ValidationError("Vous ne pouvez pas soumettre à plus de 3 conférences par jour.")
        


class OrganizingCommittee(models.Model):
    chair = [
        ('chair','chair'),
        ('co-chair','co-chair'),
        ('member','member')
    ]
    commitee_role = models.CharField(max_length=255, choices=chair)
    join_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name='committees')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='committees')
