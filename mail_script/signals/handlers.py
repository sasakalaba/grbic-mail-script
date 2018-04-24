from django.contrib.auth.signals import user_logged_in
from mail_script.client import Client
from mail_script.models import Directory


def clean_email_title(title):
    """
    Validates emails.csv title.
    """
    if not title:
        return False

    trails = title.split('-')[-1].split('.')

    if len(trails) != 2:
        return False

    if trails[1] == 'csv' and len(trails[0]) == 6 and trails[0].isdigit():
        return True
    return False


def clean_directories(file_data):
    """
    Validates directory data (needs to have emails and urls csv.)
    """
    data = {'urls': None, 'emails': None}

    if file_data:
        for file in file_data:
            filename = file.get('name', '')
            if filename and filename.startswith('Outreach'):
                data['urls'] = file['id']
            elif clean_email_title(filename):
                data['emails'] = file['id']

    return data


def get_directories(sender, user, request, **kwargs):
    """
    Creates all directory objects on login.
    """
    Directory.objects.all().delete()
    client = Client()
    items = client.get_data()
    if items:
        for item in items:
            query = "parents='%s'" % item['id']
            data = client.service.files().list(q=query).execute()
            children = clean_directories(data.get('files', []))

            params = {
                'title': item['name'],
                'dir_id': item['id'],
                'urls_id': children['urls'],
                'emails_id': children['emails']
            }
            Directory.objects.create(**params)


user_logged_in.connect(get_directories)
