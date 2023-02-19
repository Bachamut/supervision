from django.db import models
from django.utils import timezone

from account.models import Company, Customer, CustomUser


class JobTemplate(models.Model):

    job_template_name = models.CharField('job template name', max_length=30, unique=False)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='creator', null=True)

    class Meta:

        verbose_name = 'template'
        verbose_name_plural = 'templates'

    def __str__(self):
        return self.job_template_name


class Status(models.Model):

    job_template = models.ForeignKey(JobTemplate, on_delete=models.CASCADE, verbose_name='job type')
    status_id = models.CharField('status id', max_length=30)
    status_name = models.CharField('status name', max_length=80)
    body = models.TextField('description', max_length=120, blank=True, null=True)

    class Meta:

        ordering = ('status_id',)
        verbose_name = 'status'
        verbose_name_plural = 'statuses'

    def __str__(self):
        return self.status_name

    @staticmethod
    def get_status_choices(jobtype):
        job = JobTemplate.objects.get(id=jobtype)
        related_status = job.status_set.all()
        status_choices = tuple(related_status.values_list('status_id', 'status_name'))
        return status_choices


class Job(models.Model):

    STATUS_CHOICES = [
        ('status_1', 'pending'),
    ]

    investor = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='investor')
    contractor = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='contactor', null=True)
    job_type = models.ForeignKey(JobTemplate, on_delete=models.PROTECT, verbose_name='job type')
    plot_number = models.CharField('plot number', max_length=12)
    work_id = models.CharField(max_length=10, null=True)
    body = models.TextField('description', max_length=80, null=True)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES)
    created = models.DateTimeField('creation date', default=timezone.now)
    updated = models.DateTimeField('update date', auto_now=True)
    last_accessed = models.DateTimeField('last open', auto_now=True)

    class Meta:

        ordering = ('-created',)
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return self.job_type.job_template_name


class Task(models.Model):

    name = models.CharField('task name', max_length=60)
    parent_job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='job')
    body = models.TextField('description', max_length=120, null=True)
    created = models.DateTimeField('creation date', default=timezone.now)
    updated = models.DateTimeField('update date', auto_now=True)

    class Meta:

        verbose_name = 'task'
        verbose_name_plural = 'tasks'

    def __str__(self):
        return self.name
