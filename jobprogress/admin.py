from django.contrib import admin

from jobprogress.models import Job, Task, JobTemplate, Status
from account.models import Company


@admin.action(description='Oznacz wybrane jako "zakończone"')
def make_finished(modeladmin, request, queryset):
    queryset.update(status='finished')


@admin.action(description='Oznacz wybrane jako "w trakcie"')
def make_inprogress(modeladmin, request, queryset):
    queryset.update(status='in_progress')


class TaskInLine(admin.TabularInline):

    extra = 0
    model = Task


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = ('job_type', 'plot_number', 'investor', 'work_id', 'created', 'status', 'updated', 'last_accessed')
    list_filter = ('job_type', 'status', 'investor', 'created', 'updated')
    search_fields = ('job_type', 'plot_number', 'work_id', 'investor__last_name')
    # raw_id_fields = ('investor',)
    date_hierarchy = 'created'
    ordering = ('status', 'updated')
    actions = [make_finished, make_inprogress]
    inlines = [TaskInLine]


# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('name', 'body', 'parent_job')


class StatusInLine(admin.TabularInline):
    extra = 0
    model = Status


@admin.register(JobTemplate)
class JobTemplateAdmin(admin.ModelAdmin):
    list_display = ['job_template_name', 'creator']
    inlines = [StatusInLine]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['status_name']