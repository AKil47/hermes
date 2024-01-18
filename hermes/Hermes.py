import smtplib
import sys

from hermes.HermesMail import HermesMailBuilder, HermesMail


class Hermes:
    """
    Interface to create and send emails
    """
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, display_name: str, password: str):
        """
        :param smtp_server: The smtp server. (smtp.gmail.com)
        :param smtp_port: The smtp port. Make sure this port supports TLS
        :param sender_email: The email that is used to authenticate
        :param display_name: The name that should be sent with the email
        :param password: The SMTP PASSWORD. Depending on the service, this *might not* be the same as email password.
        """
        self.sender = sender_email
        self.display_name = display_name

        self.mails: list[HermesMail] = []

        # Initialize Connection
        try:
            self.server = smtplib.SMTP(host=smtp_server, port=smtp_port, timeout=60)
            self.server.connect(host=smtp_server, port=smtp_port)
            self.server.ehlo()
            self.server.starttls()  # this is needed to get past spam filters
            self.server.ehlo()
            self.server.login(sender_email, password)
        except (smtplib.SMTPConnectError, TimeoutError) as error:
            raise ConnectionError("Couldn't connect to SMTP Server. Check that server settings are correct") from error
        except (smtplib.SMTPNotSupportedError, smtplib.SMTPHeloError) as error:
            raise ConnectionError("Server isn't communicating properly. Is it actually an SMTP Server?")
        except smtplib.SMTPAuthenticationError as error:
            raise ConnectionError("Couldn't login properly. Check that the username and password is correct. Note "
                                  "that SMTP password might be different than normal email password") from error

    def mail_builder(self) -> HermesMailBuilder:
        """
        :return: A HermesMailBuilder that can be used to construct the message
        """
        return (HermesMailBuilder()
                .set_sender(self.sender)
                .set_display_name(self.display_name))

    def add_email(self, mail: HermesMail):
        """
        Adds email to a queue of messages to be sent at once. In preferred to send all the messages at once to avoid
        connection overhead
        """
        self.mails.append(mail)

    def send_mails(self):
        """
        Sends emails that were added with add_email and clears queue.
        """
        for mail in self.mails:
            self.server.sendmail(self.sender, mail.recipients, mail.mail.as_string())
        self.mails.clear()
