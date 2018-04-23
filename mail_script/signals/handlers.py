from django.contrib.auth.signals import user_logged_in
from mail_script.helpers import get_data


def get_directories(sender, user, request, **kwargs):
    """
    """
    # get_data()
    pass


user_logged_in.connect(get_directories)
