from __future__ import annotations

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


class HermesMail:
    def __init__(self, mail: MIMEMultipart, recipients: list[str]):
        self.mail = mail
        self.recipients = recipients


class HermesMailBuilder:
    def __init__(self):
        self.message = MIMEMultipart()

        self.sender = None
        self.display_name = None
        self.recipients: list[str] = []
        self.cc_recipients: list[str] = []
        self.bcc_recipients: list[str] = []

    def set_sender(self, sender: str) -> HermesMailBuilder:
        self.sender = sender
        return self

    def set_display_name(self, display_name: str) -> HermesMailBuilder:
        self.display_name = display_name
        return self

    def add_recipient(self, recipient: str) -> HermesMailBuilder:
        self.recipients.append(recipient)
        return self

    def add_cc_recipient(self, cc_recipient: str) -> HermesMailBuilder:
        self.cc_recipients.append(cc_recipient)
        return self

    def add_bcc_recipient(self, bcc_recipient: str) -> HermesMailBuilder:
        self.bcc_recipients.append(bcc_recipient)
        return self

    def set_subject(self, subject: str) -> HermesMailBuilder:
        self.message["Subject"] = subject
        return self

    def set_html_body(self, html_body: str) -> HermesMailBuilder:
        self.message.attach(MIMEText(html_body, "html"))
        return self

    def add_attachment(self, filename: str, file_data: bytes) -> HermesMailBuilder:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(file_data)
        encoders.encode_base64(attachment)
        attachment["Content-Disposition"] = f"attachment; filename={filename}"
        self.message.attach(attachment)
        return self

    def build(self) -> HermesMail:
        self.message["From"] = formataddr((self.display_name, self.sender))

        # Merge recipients into csv
        self.message["To"] = ",".join(self.recipients)
        self.message["Cc"] = ",".join(self.cc_recipients)
        self.message["Bcc"] = ",".join(self.bcc_recipients)

        return HermesMail(self.message, self.recipients + self.cc_recipients + self.bcc_recipients)
