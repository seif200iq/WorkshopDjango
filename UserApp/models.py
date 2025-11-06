from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# Create your models here.
def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()

def verify_email(email):
    domaine =["esprit.tn","seasame.com","tek.tn","gmail.com","outlook.com"]
    email_domaine = email.split("@")[1]
    if email_domaine not in domaine:
        return ValidationError("invalid email n'appartient pas au domaine")
    
name_validator = RegexValidator(regex ='^[a-zA-Z\s-]+$', message = "champ ne doit contenir que des lettres et des espaces")


class USER(AbstractUser):
    user_id = models.CharField(max_length=8,primary_key=True,editable=False,unique=True)
    first_name = models.CharField(max_length=255,validators=[name_validator])
    last_name = models.CharField(max_length=255,validators=[name_validator])
    affiliation = models.CharField(max_length=255)
    ROLE = [
        ("participant", "participant"),
        ("comitee","organizing comitee member")
    ]
    role = models.CharField(max_length=255,choices= ROLE,default="participant")
    email = models.EmailField(unique=True,validators=[verify_email])
    nationality = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.user_id:
            newid = generate_user_id()
            while USER.objects.filter(user_id=newid).exists():
                newid = generate_user_id()
            self.user_id = newid
        super().save(*args, **kwargs)
    
   


class ORGANIZINGCOMITEE(models.Model):
    chair = [
        ('chair','chair'),
        ('co-chair','co-chair'),
        ('member','member')
    ]
    commitee_role = models.CharField(max_length=255,choices=chair)
    join_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("UserApp.User",on_delete=models.CASCADE,related_name='committees')
    conference = models.ForeignKey('ConferenceApp.CONFERENCE',on_delete=models.CASCADE,related_name='committees')
    

