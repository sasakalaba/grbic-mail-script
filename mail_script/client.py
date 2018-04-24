import os
import io
from apiclient.discovery import build
from apiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
from django.conf import settings


class Client(object):
    """
    Main wrapper for handling requests and responses to the Google Drive API.
    """

    SCOPES = 'https://www.googleapis.com/auth/drive.file'

    def __init__(self, *args, **kwargs):
        """
        Initialize the API.
        """
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('drive', 'v3', http=creds.authorize(Http()))



        self.temp_path = os.path.join(settings.MEDIA_ROOT, 'temp')

    def get_data(self):
        """
        Fetches data from Google Drive and registers it in the database.
        """
        query = (
            "parents='%s' and mimeType='application/vnd.google-apps.folder'"
            % settings.GD_ROOT_DIR_ID
        )
        results = self.service.files().list(q=query).execute()

        return results.get('files', [])

    def download_csv(self, file_id, dir_path, filename):
        """
        Download file by id.
        """
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'wb') as output:
            output.write(fh.getvalue())

        return filepath

    def get_csv(self, directory):
        """
        Downloads files by id from Google Drive.
        """

        paths = {}

        # Create the download directory.
        download_dir = os.path.join(self.temp_path, directory.title)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Download files.
        paths['urls_path'] = self.download_csv(
            directory.urls_id, download_dir, 'urls.csv')
        paths['emails_path'] = self.download_csv(
            directory.emails_id, download_dir, 'emails.csv')

        return paths
