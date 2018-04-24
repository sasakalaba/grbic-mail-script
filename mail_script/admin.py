import os
from django.contrib import admin
from .models import Directory
from .client import Client
from .parse_email import Writer
from django.http import HttpResponse, Http404


def get_results(modeladmin, request, queryset):
    """
    Calls the parser and stores data.
    """

    writer = Writer()

    # Destroy old temp directories.
    writer.destroy_dirs()
    writer.make_base_dirs()

    client = Client()

    for directory in queryset:
        paths = client.get_csv(directory)
        writer.process(directory, **paths)

    # Generate zip file and return a download link:
    zip_path = writer.compress()

    # Generate download.
    if os.path.exists(zip_path):
        with open(zip_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(zip_path)
            return response
    raise Http404


get_results.short_description = 'Get results'


class DirectoryAdmin(admin.ModelAdmin):
    model = Directory
    list_display = ('title', )
    actions = [get_results]


admin.site.register(Directory, DirectoryAdmin)
