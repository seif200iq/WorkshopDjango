from django import forms
from .models import CONFERENCE
class conferenceForm(forms.ModelForm):
    class Meta:
        model = CONFERENCE
        fields = ['name','Theme','location','description','start_date','end_date']
        lables = {
            'name':"titre de la conference",
            'Theme':"Theme de la conference",
        }
        widgets = {
            'name':forms.TextInput(
                attrs={
                    'placeholder' : 'Entre titre de conference'
                }
            ),
            'start_date':forms.DateInput(
                attrs={
                    'type':'date'
                }
            ),
            'end_date':forms.DateInput(
                attrs={
                    'type':'date'
                }
            )
        }