import pytest

from hermes.lib.HermesMail import HermesMailBuilder
from hermes.lib.exceptions import MissingFieldError, NoRecipientError


class TestMissingFields:
    """
    Assertions that check if various mandatory fields are missing
    """
    def test_no_display_name(self):
        with pytest.raises(MissingFieldError, match=r"Display Name"):
            mail = (HermesMailBuilder()
                    .set_sender("test_sender@test.com")
                    .add_recipient("test_recipient@test.com")
                    .set_subject("Test Mail")
                    .set_html_body("Test Body")
                    .build())

    def test_no_from_email(self):
        with pytest.raises(MissingFieldError, match=r"From Email"):
            mail = (HermesMailBuilder()
                    .set_display_name("Test Sender")
                    .add_recipient("test_recipient@test.com")
                    .set_subject("Test Mail")
                    .set_html_body("Test Body")
                    .build())

    def test_no_subject(self):
        with pytest.raises(MissingFieldError, match=r"Subject"):
            mail = (HermesMailBuilder()
                    .set_sender("test_sender@test.com")
                    .set_display_name("Test Sender")
                    .add_recipient("test_recipient@test.com")
                    .set_html_body("Test Body")
                    .build())

    def test_no_recipients(self):
        with pytest.raises(NoRecipientError, match=r"recipient"):
            mail = (HermesMailBuilder()
                    .set_sender("test_sender@test.com")
                    .set_display_name("Test Sender")
                    .set_subject("Test Mail")
                    .set_html_body("Test Body")
                    .build())


class Test_Normal_Mail_No_Error:
    def test_different_recipients(self):
        mail = (HermesMailBuilder()
                .set_sender("test_sender@test.com")
                .set_display_name("Test Sender")
                .add_recipient("test_recipient@test.com")
                .set_subject("Test Mail")
                .set_html_body("Test Body")
                .build())

        mail = (HermesMailBuilder()
                .set_sender("test_sender@test.com")
                .set_display_name("Test Sender")
                .add_cc_recipient("test_recipient@test.com")
                .set_subject("Test Mail")
                .set_html_body("Test Body")
                .build())

        mail = (HermesMailBuilder()
                .set_sender("test_sender@test.com")
                .set_display_name("Test Sender")
                .add_bcc_recipient("test_recipient@test.com")
                .set_subject("Test Mail")
                .set_html_body("Test Body")
                .build())
