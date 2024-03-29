# Generated by Django 3.2.3 on 2022-08-08 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot_number', models.CharField(max_length=12, verbose_name='numer działki')),
                ('work_id', models.CharField(max_length=10, null=True)),
                ('body', models.TextField(max_length=80, null=True, verbose_name='opis')),
                ('status', models.CharField(choices=[('status_1', 'pending')], max_length=20, verbose_name='status')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='utworzono')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='ostatnia aktualizacja')),
                ('last_accessed', models.DateTimeField(auto_now=True, verbose_name='ostatnio otwarto')),
                ('contractor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.company', verbose_name='wykonawca')),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.customer', verbose_name='klient')),
            ],
            options={
                'verbose_name': 'Robotę',
                'verbose_name_plural': 'Roboty',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='JobTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_template_name', models.CharField(max_length=30, verbose_name='rodzaj pracy')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='twórca')),
            ],
            options={
                'verbose_name': 'Szablon',
                'verbose_name_plural': 'Szablony',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='nazwa zadania')),
                ('body', models.TextField(max_length=120, null=True, verbose_name='opis')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='utworzono')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='ostatnia aktualizacja')),
                ('parent_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobprogress.job', verbose_name='Robota')),
            ],
            options={
                'verbose_name': 'Zadanie',
                'verbose_name_plural': 'Zadania',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_id', models.CharField(max_length=30, verbose_name='ID statusu')),
                ('status_name', models.CharField(max_length=80, verbose_name='nazwa statusu')),
                ('body', models.TextField(blank=True, max_length=120, null=True, verbose_name='opis')),
                ('job_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobprogress.jobtemplate', verbose_name='Rodzaj Pracy')),
            ],
            options={
                'verbose_name': 'Etap',
                'verbose_name_plural': 'Etapy',
                'ordering': ('status_id',),
            },
        ),
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jobprogress.jobtemplate', verbose_name='typ pracy'),
        ),
    ]
