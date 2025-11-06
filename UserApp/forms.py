from django import forms
from .models import USER
from django.contrib.auth.forms import UserCreationForm
class registerUserForm(UserCreationForm):
    class Meta:
        model = USER
        fields = ['username','first_name','last_name','email','affiliation','nationality','password1','password2']
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Email universitaire'
                }
            ),
            'password1': forms.PasswordInput(
                attrs={
                    'placeholder': 'Mot de passe'
                }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'placeholder': 'Confirmer mot de passe'
                }
            )
        }

def save(self,commit = True):
    user = super().save(commit=False)
    user.role = "participant"
    if commit:
        user.save()
    return user
