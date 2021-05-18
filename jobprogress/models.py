from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Job(models.Model):
    JOB_TYPE = (
        ('type_1', 'mdcp'),
        ('type_2', 'podział'),
        ('type_3', 'wznowienie granic'),
        ('type_4', 'obsługa inwestycji'),
    )

    STATUS_CHOICES = (
        ('not_started', 'nie rozpoczęta'),
        ('in_progress', 'w trakcie'),
        ('finished', 'zakończone'),
    )

    job_type = models.CharField('typ roboty', max_length=30, choices=JOB_TYPE)
    plot_number = models.CharField('numer działki', max_length=12)
    investor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='inwestor', related_name='job_kerg')
    kerg = models.CharField(max_length=10)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    body = models.TextField(max_length=80)
    created = models.DateTimeField('utworzono', default=timezone.now)
    updated = models.DateTimeField('ostatnia aktualizacja', auto_now=True)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default='not started')

    job_type.short_description = 'robota'


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.kerg