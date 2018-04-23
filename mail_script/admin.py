from django.contrib import admin
from .models import Directory


def get_results(modeladmin, request, queryset):
    """
    """
    # https://docs.djangoproject.com/en/2.0/ref/contrib/admin/actions/
    pass
get_results.short_description = 'Get results'


class DirectoryAdmin(admin.ModelAdmin):
    model = Directory
    list_display = ('title', )
    actions = [get_results]


admin.site.register(Directory, DirectoryAdmin)
