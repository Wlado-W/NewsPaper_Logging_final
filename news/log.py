import logging
from django.utils.log import AdminEmailHandler

class CustomAdminEmailHandler(AdminEmailHandler):
    def emit(self, record):
        """
        Customize the email message to exclude the traceback.
        """
        message = self.format(record)
        subject = self.format_subject(record)
        self.send_mail(subject, message, fail_silently=True)

        if record.exc_info:
            # Ensure exc_info is deleted to prevent it from being attached to the email
            # Remove the traceback information
            record.exc_info = None
