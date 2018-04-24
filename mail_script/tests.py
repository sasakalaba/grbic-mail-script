from django.test import TestCase
from .client import Client


class GoogleDriveGetDataTest(TestCase):
    """
    Unit tests for import data helper function.
    """

    def test_get_data(self):
        """
        """
        client = Client()
        client.get_data()
        # get_files('1yncWniN1kcQClqLZ_tRlSbQVTTXDWVI3')
