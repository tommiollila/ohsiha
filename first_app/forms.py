from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EmailForm(forms.Form):
    your_email = forms.CharField (label ='E-mail', max_length=100)

class RegisterationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
    def save(self, commit=True):
        user = super(RegisterationForm, self).save(commit=False)
        user.first_name = cleaned_data['first_name']
        user.last_name = cleaned_data['last_name']
        user.email = cleaned_data['email']

        if commit:
            user.save()

        return user
