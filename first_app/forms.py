from django import forms

class EmailForm(forms.Form):
    your_email = forms.CharField (label ='E-mail', max_length=100)
