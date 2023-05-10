from unittest import TestCase
from unittest.mock import patch

from ptmd.lib.email.validate_account import send_confirmation_mail
from ptmd.const import SITE_URL


class TestValidateEmail(TestCase):

    @patch('ptmd.lib.email.validate_account.build')
    def test_send_confirmation_mail(self, mock_build):
        message = send_confirmation_mail(username='test', email="test@test.com", token="test")
        self.assertIn("<h1> Hello, test</h1>", message)
        self.assertIn(f"{SITE_URL}/activate/test", message)
