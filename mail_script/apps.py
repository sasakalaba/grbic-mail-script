from django.apps import AppConfig


class MailScriptConfig(AppConfig):
    name = 'mail_script'
    verbose_name = 'Google Drive Share Folder'

    def ready(self):
        import mail_script.signals.handlers
