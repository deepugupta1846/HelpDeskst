from django import forms
from .models import *

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class UserForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)

    class Meta:
        model = UserModel
        fields = ['first_name', 'mid_name', 'last_name', 'gender', 'user_type']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':'First Name', 'class': 'form-control mb-2'}),
            'mid_name': forms.TextInput(attrs={'placeholder': 'Mid Name', 'class': 'form-control mb-2', }),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control mb-2'}),
            'user_type': forms.Select(attrs={'class':'form-control mb-2'}),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = TicketModel
        fields = [ 'categrories', 'ticket_type', 'question', 'description']
        widgets = {
            'categrories': forms.Select(attrs={ 'class': 'form-control mb-2'}),
            'ticket_type': forms.Select(attrs={'class': 'form-control mb-2'}),
            'question': forms.TextInput(attrs={'class':'form-control mb-2'}),
            'description': forms.Textarea(attrs={'class':'form-control mb-2'})
        }