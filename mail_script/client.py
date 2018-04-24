import httplib2
import os
import io
from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from django.conf import settings
from .parse_email import get_urls, get_emails, clean_emails, write_data


class Client(object):
    """
    Main wrapper for handling requests and responses to the Google Drive API.
    """

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/drive-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Drive API Python Quickstart'

    def __init__(self, *args, **kwargs):
        """
        Initialize the API.
        """
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('drive', 'v2', http=http)

    def _get_credentials(self):
        """
        Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'drive-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def get_data(self):
        """
        Fetches data from Google Drive and registers it in the database.
        """
        query = (
            "parents='%s' and mimeType='application/vnd.google-apps.folder'"
            % settings.GD_ROOT_DIR_ID
        )
        results = self.service.files().list(q=query).execute()

        return results.get('items', [])


"""
def get_files(file_id):
    # Retrieves specific files from dir list.

    service = init_service()

    #
    query = "parents='%s'" % '1yncWniN1kcQClqLZ_tRlSbQVTTXDWVI3'
    results = service.files().list(q=query).execute()

    items = results.get('items', [])
    #

    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
"""
