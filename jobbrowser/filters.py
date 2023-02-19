import django_filters

from jobprogress.models import Job


class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['investor',
                  'contractor',
                  'job_type',
                  'status']
