from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class JobTemplate(models.Model):
    job_template_name = models.CharField('rodzaj pracy', max_length=30, unique=True)

    class Meta:
        verbose_name = 'Szablon'
        verbose_name_plural = 'Szablony'

    def __str__(self):
        return self.job_template_name


class Status(models.Model):
    job_template = models.ForeignKey(JobTemplate, on_delete=models.CASCADE, verbose_name='Rodzaj Pracy')
    status_id = models.CharField('ID statusu', max_length=30)
    status_name = models.CharField('nazwa statusu', max_length=80)
    body = models.TextField('opis', max_length=120, blank=True, null=True)

    class Meta:
        ordering = ('status_id',)
        verbose_name = 'Etap'
        verbose_name_plural = 'Etapy'

    def __str__(self):
        return self.status_name

    @staticmethod
    def get_status_choices(jobtype):
        job = JobTemplate.objects.get(id=jobtype)
        related_status = job.status_set.all()
        status_choices = tuple(related_status.values_list('status_id', 'status_name'))
        return status_choices


class Job(models.Model):

    # JOB_TYPE = [
    #     ('type_1', 't1'),
    # ]
    #
    STATUS_CHOICES = [
        ('status_1', 's1'),
    ]

    investor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='klient', related_name='job_kerg')
    # job_type = models.CharField('rodzaj pracy', max_length=30, choices=JOB_TYPE)
    job_type = models.ForeignKey(JobTemplate, on_delete=models.PROTECT, verbose_name='typ pracy')
    plot_number = models.CharField('numer działki', max_length=12)
    work_id = models.CharField(max_length=10, null=True)
    body = models.TextField('opis', max_length=80, null=True)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES)
    # status = models.CharField('aktualny etap', max_length=20, choices=Status.get_status_choices(1))
    created = models.DateTimeField('utworzono', default=timezone.now)
    updated = models.DateTimeField('ostatnia aktualizacja', auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Robotę'
        verbose_name_plural = 'Roboty'

    def __str__(self):
        return self.job_type.job_template_name


class Task(models.Model):
    name = models.CharField('nazwa zadania', max_length=60)
    parent_job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='Robota')
    body = models.TextField('opis', max_length=120, null=True)
    created = models.DateTimeField('utworzono', default=timezone.now)
    updated = models.DateTimeField('ostatnia aktualizacja', auto_now=True)

    class Meta:
        verbose_name = 'Zadanie'
        verbose_name_plural = 'Zadania'

    def __str__(self):
        return self.name
