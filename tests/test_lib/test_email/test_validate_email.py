from unittest import TestCase
from unittest.mock import patch, mock_open

from ptmd.lib.email.core import send_confirmation_mail
from ptmd.const import SITE_URL


@patch("ptmd.lib.email.core.Credentials")
class TestValidateEmail(TestCase):

    @patch('ptmd.lib.email.core.build')
    def test_send_confirmation_mail(self, mock_build, mock_credentials):
        mock_credentials.from_authorized_user_file.return_value = {'save_credentials_file': 'test'}
        message = send_confirmation_mail(username='test', email="test@test.com", token="test")
        self.assertIn("<h1> Hello, test</h1>", message)
        self.assertIn(f"{SITE_URL}/api/enable/test", message)
