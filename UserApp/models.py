from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.exceptions import ValidationError #email
from  django.core.validators import RegexValidator #nom prenom
# Create your models here.
def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()

def verify_email(email):
    domaine=["esprit.tn","sesame.com","tek.tn","centrale.tn"]
    email_domain=email.split("@")[1]
    if email_domain not in domaine:
        raise ValidationError("lemail est invalide et doit eappartenir a un domaine universitaire")

name_validator=RegexValidator(
    regex=r'^[a-zA-Z\s-]+$',
    message="ce champs ne doit cntenir que des lettres et des espaces"
)

class User(AbstractUser):
    user_id=models.CharField(max_length=8,primary_key=True,unique=True,editable=False)
    first_name=models.CharField(max_length=255,validators=[name_validator])
    last_name=models.CharField(max_length=255,validators=[name_validator])
    ROLE=[
        ("participant","participant"),
        ("commitee","organisateur ou membre du comité scientifique")
    ]
    role=models.CharField(max_length=255,choices=ROLE,default="participant")
    affiliation=models.CharField(max_length=255)
    email=models.EmailField(unique=True, validators=[verify_email])
    nationality=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
        if not self.user_id: #ferga nexiste pas
            newid=generate_user_id()
            while User.objects.filter(user_id=newid).exists():
                newid=generate_user_id()
            self.user_id=newid
        super().save(*args,**kwargs)



