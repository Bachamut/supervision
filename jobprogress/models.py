from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class JobTemplate(models.Model):
    job_template_name = models.CharField('rodzaj pracy', max_length=30, unique=True)
    job_template_id = models.CharField('ID szablonu', max_length=4, unique=True)

    class Meta:
        ordering = ('job_template_id',)
        verbose_name = 'Szablon'
        verbose_name_plural = 'Szablony'

    def __str__(self):
        return self.job_template_name


class Status(models.Model):
    job_template = models.ManyToManyField(JobTemplate, verbose_name='Rodzaj Pracy')
    status_id = models.CharField('ID statusu', max_length=30, unique=True)
    status_name = models.CharField('nazwa statusu', max_length=80, unique=True)
    body = models.TextField('opis', max_length=120, blank=True, null=True)

    class Meta:
        ordering = ('status_id',)
        verbose_name = 'Etap'
        verbose_name_plural = 'Etapy'

    def __str__(self):
        return self.status_name


class Job(models.Model):

    # JOB_TYPE = [
    #     ('type_1', 'mdcp'),
    #     ('type_2', 'podział'),
    #     ('type_3', 'wznowienie granic'),
    #     ('type_4', 'obsługa inwestycji'),
    # ]
    #
    #
    # STATUS_CHOICES = [
    #     ('not_started', 'nie rozpoczęta'),
    #     ('in_progress', 'w trakcie'),
    #     ('finished', 'zakończone'),
    # ]

    investor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='inwestor', related_name='job_kerg')
    job_type = models.CharField('rodzaj pracy', max_length=30, choices=tuple(JobTemplate.objects.values_list('job_template_id', 'job_template_name')))
    # job_type = models.CharField('rodzaj pracy', max_length=30, choices=JOB_TYPE)
    plot_number = models.CharField('numer działki', max_length=12)
    kerg = models.CharField(max_length=10)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    body = models.TextField(max_length=80)
    created = models.DateTimeField('utworzono', default=timezone.now)
    updated = models.DateTimeField('ostatnia aktualizacja', auto_now=True)
    status = models.CharField('status', max_length=20, choices=tuple(Status.objects.values_list('status_id', 'status_name')), default=[0])
    # status = models.CharField('status', max_length=20, choices=STATUS_CHOICES)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Robotę'
        verbose_name_plural = 'Roboty'

    def __str__(self):
        return self.kerg


class Task(models.Model):
    name = models.CharField('nazwa zadania', max_length=60)
    parent_job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='Robota', related_name='tasks')
    body = models.TextField('opis', max_length=120)
    created = models.DateTimeField('utworzono', default=timezone.now)
    updated = models.DateTimeField('ostatnia aktualizacja', auto_now=True)

    class Meta:
        verbose_name = 'Zadanie'
        verbose_name_plural = 'Zadania'

    def __str__(self):
        return self.name
