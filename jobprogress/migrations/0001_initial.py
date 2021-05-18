# Generated by Django 3.2.3 on 2021-05-13 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(choices=[('type_1', 'mdcp'), ('type_2', 'podział'), ('type_3', 'wznowienie granic'), ('type_4', 'obsługa inwestycji')], max_length=30)),
                ('plot_number', models.CharField(max_length=12)),
                ('kerg', models.CharField(max_length=10)),
                ('slug', models.SlugField(max_length=250, unique_for_date='created')),
                ('body', models.TextField(max_length=80)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('finished', 'Finished')], default='not started', max_length=20)),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_type', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
