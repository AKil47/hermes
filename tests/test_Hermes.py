import smtplib
from unittest.mock import MagicMock, patch
import pytest

from hermes.Hermes import Hermes


@pytest.fixture
def mock_smtp(mocker) -> MagicMock:
    mock = mocker.MagicMock()
    mock.connect.return_value = None
    mock.ehlo.return_value = None
    mock.starttls.return_value = None
    mock.login.return_value = None

    return mock


def test_connect_timeout(mock_smtp):
    with pytest.raises(ConnectionError):
        with patch.object(smtplib, "SMTP", return_value=mock_smtp):
            mock_smtp.login.side_effect = TimeoutError("")

            hermes = Hermes("test_server", 1, "test_sender@test.com", "Test Sender", "test_passwd")


def test_login_issue(mock_smtp):
    with pytest.raises(ConnectionError):
        with patch.object(smtplib, "SMTP", return_value=mock_smtp):
            mock_smtp.login.side_effect = smtplib.SMTPAuthenticationError(1, "issue")

            hermes = Hermes("test_server", 1, "test_sender@test.com", "Test Sender", "test_passwd")
