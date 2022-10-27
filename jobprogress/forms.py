from django import forms
from django.forms import ModelForm

from account.models import Company
from jobprogress.models import JobTemplate, Job


class EmailStatusForm(forms.Form):

    user = forms.CharField(max_length=35)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class AddJobTemplate(ModelForm):
    class Meta:
        model = JobTemplate
        fields = ['job_template_name']

    # def __init__(self, *args, **kwargs):
    #     if kwargs:
    #         owner_user = kwargs.pop('owner_user')
    #         super(AddJobTemplate, self).__init__(*args, **kwargs)
    #         self.creator = owner_user


class AddOrder(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        owner_user = kwargs.pop('owner_user')
        super(AddOrder, self).__init__(*args, **kwargs)
        self.fields['contractor'].queryset = Company.objects.filter(owner=owner_user)
        self.fields['job_type'].queryset = JobTemplate.objects.filter(creator=owner_user)
