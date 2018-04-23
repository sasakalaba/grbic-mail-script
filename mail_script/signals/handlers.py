from django.contrib.auth.signals import user_logged_in
from mail_script.helpers import get_data
from mail_script.models import Directory


def get_directories(sender, user, request, **kwargs):
    """
    Creates all directory objects on login.
    """
    items = get_data()
    if items:
        for item in items:
            Directory.objects.get_or_create(
                title=item['title'], dir_id=item['id'], url=item['alternateLink'])


user_logged_in.connect(get_directories)
