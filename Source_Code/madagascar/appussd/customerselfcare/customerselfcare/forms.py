from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

class FrmIndex(forms.Form):
    username = forms.CharField(error_messages = {
               'required': 'Please enter your username.', 
               'invalid': 'Please enter a valid username.'})
    password = forms.CharField(
               widget=forms.PasswordInput, 
                      error_messages = {'required': 'Please enter your password.', 
                                        'invalid': 'Please enter a valid password.'})
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError("Please enter your username.")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError("Please enter your password.")
        return password

class FrmThreeG(forms.Form):
    SERVICE_CHOICES = (
        ("1", "Internet Bundles"),
    )
    RENEW_CHOICES = (
        ("False", "No"),
        ("True", "Yes")
    )

    service = forms.ChoiceField(choices=SERVICE_CHOICES)

    autorenew = forms.ChoiceField(choices=RENEW_CHOICES)
    
    BUNDLES_CHOICES = ()
    bundles = forms.ChoiceField(choices=BUNDLES_CHOICES)

class FrmUploadUsers(forms.Form):
    file = forms.FileField(error_messages = {
           'required': 'Please select a file to upload.', 
           'invalid': 'Please select a valid file to upload.'})

class msisdnForm(forms.Form):
    file = forms.FileField(error_messages = {
           'required': 'Please select a file to upload.', 
           'invalid': 'Please select a valid file to upload.'})

