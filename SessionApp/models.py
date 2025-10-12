from django.db import models
from ConferenceApp.models import Conference
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
# Create your models here.
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    session_day=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    room = models.CharField(
    max_length=50,  # Max 50, pas 255
    validators=[
        RegexValidator(
            regex=r'^[A-Za-z0-9]+$',
            message="Le nom de la salle ne doit contenir que des lettres et des chiffres.",
            code='invalid_room_name'
        )
    ]
)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    conference = models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="sessions")
    # À ajouter dans votre classe Session
    def clean(self):
        if self.conference:
            if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
                raise ValidationError(
                    "La date de la session doit être comprise entre la date de début et la date de fin de la conférence."
                )
        if self.end_time <= self.start_time:
            raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")


