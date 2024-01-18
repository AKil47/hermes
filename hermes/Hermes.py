import smtplib

from hermes.HermesMail import HermesMailBuilder, HermesMail


class Hermes:
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, display_name: str, password: str):
        self.sender = sender_email
        self.display_name = display_name

        self.mails: list[HermesMail] = []

        # Initialize Connection
        self.server = smtplib.SMTP(host=smtp_server, port=smtp_port)
        self.server.connect(host=smtp_server, port=smtp_port)
        self.server.ehlo()
        self.server.starttls()  # this is needed to get past spam filters
        self.server.ehlo()
        self.server.login(sender_email, password)

    def mail_builder(self) -> HermesMailBuilder:
        return (HermesMailBuilder()
                .set_sender(self.sender)
                .set_display_name(self.display_name))

    def add_email(self, mail: HermesMail):
        self.mails.append(mail)

    def send_mails(self):
        for mail in self.mails:
            self.server.sendmail(self.sender, mail.recipients, mail.mail.as_string())
