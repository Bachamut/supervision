from django import forms


class EmailStatusForm(forms.Form):
    user = forms.CharField(max_length=35)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)