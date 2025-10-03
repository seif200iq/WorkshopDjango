from django.db import models
from django.core.validators import MaxLengthValidator
# Create your models here.
from django.core.exceptions import ValidationError

class Conferance(models.Model):
    Conferance_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    THEME=[
        ("IA","Computer science & ia"),
        ("SE","Science & engineering"),
        ("SC","Social sciences"),
    ]
    
    theme=models.CharField(max_length=255,choices=THEME)
    location=models.CharField(max_length=50)
    description=models.TextField(validators=[
        MaxLengthValidator(30,"La description doit contenir au moins 30 caractéres.")
        ]
    )
    start_date=models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("La date de début de la conference doit etre antérieur a la date fin")

class Submission(models.Model):
    submission_id = models.CharField(max_length=255,primary_key=True,unique=True)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.TextField()
    papers = models.FileField(upload_to="papers/")

    STATUS=[
        ("submitted","submitted"),
        ("under review","under review"),
        ("accepted","accepted"),
        ("rejected","rejected"),
    ]
    status=models.CharField(max_length=50,choices=STATUS)
    payed=models.BooleanField(default=False)
    submission_date=models.DateField(auto_now=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    user=models.ForeignKey("UserApp.USER",on_delete=models.CASCADE,related_name="submission")
    conference=models.ForeignKey(Conferance,on_delete=models.CASCADE,related_name="submission")