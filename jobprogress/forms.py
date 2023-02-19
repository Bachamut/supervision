from django import forms
from django.forms import ModelForm
from django.core.mail import send_mail

from account.models import Company
from jobprogress.models import JobTemplate, Job


class EmailNotificationForm(forms.Form):

    user = forms.CharField(max_length=35)
    email_from = forms.EmailField()
    email_to = forms.EmailField(required=False)
    subject = forms.CharField(required=True, max_length=60)
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def get_info(self):
        cl_data = super().clean()
        user = cl_data.get('user')
        email_from = cl_data.get('email_from')
        email_to = cl_data.get('email_to')
        subject = cl_data.get('subject')

        msg = f'{user} with email {email_from} send a message:'
        msg += f'\n'
        msg += cl_data.get('comments')

        return subject, msg, email_from, email_to

    def send(self):
        subject, msg, email_from, email_to = self.get_info()

        send_mail(subject=subject,
                  message=msg,
                  from_email=email_from,
                  recipient_list=[email_to])


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
