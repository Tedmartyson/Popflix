from django import forms

class UploadRateForm(forms.Form):
    rate = forms.FloatField()