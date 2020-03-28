from django import forms

class InputForm(forms.Form):
    title = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class' : 'custom-form-txtinp form-control'}))
    content = forms.CharField(max_length=25000, widget=forms.Textarea(attrs={'class' : 'custom-form-txtarea form-control'}))

class WebScrapeForm(forms.Form):
    url = forms.CharField(max_length=1500, widget=forms.TextInput(attrs={'class' : 'custom-form-txtinp form-control'}))