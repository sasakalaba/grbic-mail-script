import csv
import os
from collections import OrderedDict
from urllib.parse import urlparse


PREFIXES = ('www', 'ww2')


def make_results_dir():
    """
    Create results directory.
    """
    if not os.path.isdir('results'):
        os.makedirs('results')


def get_urls(path):
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
            if any(domain.startswith(prefix) for prefix in PREFIXES):
                domain = domain.split('.', 1)[1]

            # Map them to ulrs
            if domain in urls:
                urls[domain]['urls'].append(row[0])
            else:
                urls[domain] = {'email': '', 'urls': [row[0], ]}

    return urls


def get_emails(path):
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


def clean_emails(emails):
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


def write_data(urls, emails):
    """
    Append email data to urls.
    """
    empty_emails = {}

    # Create results directory.
    make_results_dir()

    # Set path values.
    result_path = os.path.join(settings.MEDIA_ROOT, 'results/result.csv')
    empty_emails_path = os.path.join(settings.MEDIA_ROOT, 'results/no_email_urls.csv')

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

    return {'result': result_path, 'empty_emails': empty_emails_path}
