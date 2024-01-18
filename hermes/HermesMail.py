from __future__ import annotations

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from hermes.exceptions import MissingFieldError, NoRecipientError


class HermesMail:
    """
    Object that holds mail constructed MIMEMultipart Message and recipients. In general, this object should be built
    using a HermesMailBuilder that is generated from a Hermes instance.
    """
    def __init__(self, mail: MIMEMultipart, recipients: list[str]):
        self.mail = mail
        self.recipients = recipients


class HermesMailBuilder:
    def __init__(self):
        self.message = MIMEMultipart()

        self.sender = None
        self.display_name = None
        self.subject_added = False
        self.body_added = False
        self.recipients: list[str] = []
        self.cc_recipients: list[str] = []
        self.bcc_recipients: list[str] = []

    def set_sender(self, sender: str) -> HermesMailBuilder:
        """
        Sets the "from" header of the email. This should NOT be needed to be called directly
        """
        self.sender = sender
        return self

    def set_display_name(self, display_name: str) -> HermesMailBuilder:
        """
        Sets the "display name" header of the email (who it says the email is from). This method should only be called
        if the Display Name for this individual email should be different. Consider changing the display name of the
        overall Hermes object that constructs this.
        """
        self.display_name = display_name
        return self

    def add_recipient(self, recipient: str) -> HermesMailBuilder:
        """
        Adds a normal recipient (shows up in the "To" field of the email)
        """
        self.recipients.append(recipient)
        return self

    def add_cc_recipient(self, cc_recipient: str) -> HermesMailBuilder:
        """
        Adds a CC recipient (shows up in the "CC" field of the email)
        """
        self.cc_recipients.append(cc_recipient)
        return self

    def add_bcc_recipient(self, bcc_recipient: str) -> HermesMailBuilder:
        """
        Adds a BCC recipient (shows up in the "CC" field of the email). It's a good idea to use this for blast emails
        instead of sending multiple individual emails.
        """
        self.bcc_recipients.append(bcc_recipient)
        return self

    def set_subject(self, subject: str) -> HermesMailBuilder:
        """
        Sets the subject of the mail.
        """
        self.subject_added = True
        self.message["Subject"] = subject
        return self

    def set_html_body(self, html_body: str) -> HermesMailBuilder:
        """
        Sets the HTML body of the message. Note that not all HTML works with email so be sure to send a test email
        first. Sometimes, the emails could vary by client so test with some variety (Gmail, Yahoo, Outlook, Outlook Web)
        """
        self.body_added = True
        self.message.attach(MIMEText(html_body, "html"))
        return self

    def add_attachment(self, filename: str, file_data: bytes) -> HermesMailBuilder:
        """
        Adds an attachment to the email. This *should* work for most common file types, but be sure to send a test email.
        Some filetypes get caught by virus detectors and spam filters.

        :param filename: The name to send the filename as
        :param file_data: The byte stream of the data (open the file in binary mode)
        """
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(file_data)
        encoders.encode_base64(attachment)
        attachment["Content-Disposition"] = f"attachment; filename={filename}"
        self.message.attach(attachment)
        return self

    def build(self) -> HermesMail:
        """
        Creates the HermesMail object to be sent.
        """
        if self.display_name is None:
            raise MissingFieldError("Display Name")
        elif self.sender is None:
            raise MissingFieldError("From Email")
        self.message["From"] = formataddr((self.display_name, self.sender))

        # Merge recipients into csv
        all_recipients: list[str] = self.recipients + self.cc_recipients + self.bcc_recipients
        if len(all_recipients) == 0:
            raise NoRecipientError()
        self.message["To"] = ",".join(self.recipients)
        self.message["Cc"] = ",".join(self.cc_recipients)
        self.message["Bcc"] = ",".join(self.bcc_recipients)

        if not self.body_added:
            raise MissingFieldError("Message Body")
        if not self.subject_added:
            raise MissingFieldError("Subject")

        return HermesMail(self.message, all_recipients)
