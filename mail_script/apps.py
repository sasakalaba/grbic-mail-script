from django.apps import AppConfig


class MailScriptConfig(AppConfig):
    name = 'mail_script'

    def ready(self):
        import mail_script.signals.handlers
