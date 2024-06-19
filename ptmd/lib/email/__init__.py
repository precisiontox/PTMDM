""" This module contains all functions related to sending emails. Email are sent when:
    - A user creates an account: send_confirmation_mail
    - A user enabled is account (clicked the link in the email) and admin needs to validate it send_validation_mail
    - An admin validated the account: send_validated_account_mail

    - TODO: A user forgot his password: send_forgot_password_mail
"""
from .core import (
    send_confirmation_mail,
    send_validated_account_mail,
    send_validation_mail,
    send_reset_pwd_email,
    send_file_shipped_email
)
