from django.contrib import admin

from jobprogress.models import Job

@admin.action(description='Oznacz wybrane jako "zakończone"')
def make_finished(modeladmin, request, queryset):
    queryset.update(status='finished')

@admin.action(description='Oznacz wybrane jako "w trakcie"')
def make_inprogress(modeladmin, request, queryset):
    queryset.update(status='in_progress')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_type', 'plot_number', 'investor', 'kerg', 'created', 'updated', 'status')
    list_filter = ('status', 'created', 'investor', 'job_type', 'updated')
    search_fields = ('job_type', 'plot_number', 'kerg', 'investor__last_name')
    prepopulated_fields = {'slug': ('plot_number',)}
    # raw_id_fields = ('investor',)
    date_hierarchy = 'created'
    ordering = ('status', 'updated')
    actions = [make_finished, make_inprogress]

