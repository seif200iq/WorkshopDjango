from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import string
import random
from django.utils import timezone

# Create your models here.
def generate_submission_id():
    letters = ''.join(random.choices(string.ascii_uppercase, k=8))
    return f"SUB{letters}"
def validate_keywords(value):
    # Sépare les mots par virgules et supprime les espaces inutiles
    keywords = [k.strip() for k in value.split(',') if k.strip()]
    if len(keywords) > 10:
        raise ValidationError("You can specify a maximum of 10 keywords separated by commas.")
def validate_keywords(value):
    # Sépare les mots par virgules et supprime les espaces inutiles
        keywords = [k.strip() for k in value.split(',') if k.strip()]
        if len(keywords) > 10:
            raise ValidationError("You can specify a maximum of 10 keywords separated by commas.")    
class CONFERENCE(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(validators=[MaxLengthValidator(30, "Description must be at most 30 characters long.")])
    Theme_list = [
        ('CSAI', 'Computer Science & Artificial Intelligence'),
        ('SE', 'Science & Engineering'),
        ('SSE', 'Social Sciences & Education'),
        ('IT', 'Interdisciplinary Themes'),
    ]
    Theme = models.CharField(max_length=225,choices=Theme_list)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("Start date must be before end date.")  
    
        
    


class SUBMISSION(models.Model):
    submission_id = models.CharField(max_length=255,primary_key=True,unique=True,editable=False,default=generate_submission_id)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.TextField(validators=[validate_keywords])
    papers = models.FileField(upload_to='paper/',validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    STATUS =[
        ('submitted','submitted'),
        ('under review', 'under review'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected')
    ]
    status = models.CharField(max_length=50,choices=STATUS)
    payed = models.BooleanField(default=False)
    submission_date= models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('UserApp.USER',on_delete=models.CASCADE,related_name='submissions')
    conference = models.ForeignKey(CONFERENCE,on_delete=models.CASCADE,related_name='submissions')  
    def clean(self):
        if self.submission_date:
            if self.conference.start_date < timezone.now().date() and self:
                raise ValidationError("The conference has already started.")
    
