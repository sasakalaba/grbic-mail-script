from django.contrib import admin
from .models import Directory
from .parse_email import Parser


def get_results(modeladmin, request, queryset):
    """
    Calls the parser and stores data.
    """
    parser = Parser()

get_results.short_description = 'Get results'


class DirectoryAdmin(admin.ModelAdmin):
    model = Directory
    list_display = ('title', )
    actions = [get_results]


admin.site.register(Directory, DirectoryAdmin)
