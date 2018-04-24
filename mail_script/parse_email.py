import csv
import os
import shutil
import zipfile
from collections import OrderedDict
from urllib.parse import urlparse
from django.conf import settings


class Parser(object):
    """
    Main class for processing email data.
    """

    PREFIXES = ('www', 'ww2')

    def get_urls(self, path):
        """
        Parse urls from csv file.
        Return dict with urls mapped to their domains.
        """

        urls = {}
        with open(path, 'rt') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                parsed_uri = urlparse(row[0])

                # Get domain name
                domain = '{uri.netloc}'.format(uri=parsed_uri)
                if any(domain.startswith(prefix) for prefix in self.PREFIXES):
                    domain = domain.split('.', 1)[1]

                # Map them to ulrs
                if domain in urls:
                    urls[domain]['urls'].append(row[0])
                else:
                    urls[domain] = {'email': '', 'urls': [row[0], ]}

        return urls

    def get_emails(self, path):
        """
        Parse emails from csv file.
        Return dict with emails mapped to their domain.
        """

        emails = {}
        with open(path, 'rt') as csvfile:
            reader = csv.reader(csvfile)

            # Skip header row
            next(reader)

            for row in reader:
                # Get only email and confidence score.
                email = {row[0]: row[3]}

                if row[1] in emails:
                    emails[row[1]].update(email)
                else:
                    emails[row[1]] = email

        return emails

    def clean_emails(self, emails):
        """
        Detect domains with multiple emails, end select only the one with the
        highest confidence score.
        """

        for domain in emails:
            mail_dict = emails[domain]

            if len(mail_dict) > 1:
                max_key = max(mail_dict, key=mail_dict.get)
                emails[domain] = {max_key: mail_dict[max_key]}

        return emails

    def write_data(self, urls, emails, result_path, empty_emails_path):
        """
        Append email data to urls.
        """
        empty_emails = {}

        # We're gonna use urls dict as the main container, so take all the data out
        # of emails dict and merge them into urls.
        for domain in emails:
            email = {'email': '', 'confidence_number': ''}
            (email['email'], email['confidence_number']), = emails[domain].items()
            urls[domain].update(email)

        # Convert urls to OrderedDict.
        urls = OrderedDict(sorted(urls.items()))

        # Get final data (emails mapped to their URLs)
        with open(result_path, 'w') as csvfile:
            fieldnames = ['Email', 'URL', ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for domain in urls:
                row = urls[domain]

                # Only get the first url and ignore the rest.
                row_url = row.get('urls', ['', ])[0]
                email = row.get('email')

                # Map empty emails to another dict and skip writing that row.
                if not email:
                    empty_emails[domain] = row_url
                    continue

                writer.writerow({
                    'Email': email,
                    'URL': row_url,
                })

        # Output empty emails into a separate csv
        with open(empty_emails_path, 'w') as csvfile:
            fieldnames = ['Domain', 'URL', ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for domain in empty_emails:
                writer.writerow({
                    'Domain': domain,
                    'URL': empty_emails[domain],
                })

        return {
            'result': result_path,
            'empty_emails': empty_emails_path
        }


class Writer(object):
    """
    Main class for writing and destroying cleaned data.
    """

    def __init__(self, *args, **kwargs):
        self.parser = Parser()

        # Create temporary directories for data storage and download.
        self.temp_path = os.path.join(settings.MEDIA_ROOT, 'temp')
        self.result_path = os.path.join(settings.MEDIA_ROOT, 'results')

    def make_base_dirs(self):
        """
        Create results directory.
        """
        for dir_path in (self.temp_path, self.result_path):
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    def destroy_dirs(self):
        """
        Destroys results directory.
        """
        shutil.rmtree(self.temp_path)
        shutil.rmtree(self.result_path)

    def compress(self):
        """
        Compresses results.
        """
        filepath = os.path.join(settings.MEDIA_ROOT, 'results.zip')
        zipf = zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED)

        for root, dirs, files in os.walk(self.result_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(self.result_path, '..')))
        zipf.close()

        return filepath

    def process(self, directory, urls_path, emails_path):
        """
        Process data.
        """
        urls = self.parser.get_urls(urls_path)
        emails = self.parser.get_emails(emails_path)
        results = self.parser.clean_emails(emails)

        # Create directories
        subdir = os.path.join(self.result_path, '%s_result' % directory.title)
        if not os.path.exists(subdir):
            os.makedirs(subdir)
        urls_result_path = os.path.join(subdir, 'urls.csv')
        empty_emails_path = os.path.join(subdir, 'emails.csv')

        self.parser.write_data(
            urls, results, urls_result_path, empty_emails_path)
