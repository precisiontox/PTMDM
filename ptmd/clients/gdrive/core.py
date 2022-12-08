""" This module provides the core functions necessary to connect to a google drive, create the necessary directorie
and upload the files to the drive.

@author: D. Batista (Terazus)
"""
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from ptmd.const import ALLOWED_PARTNERS
from ptmd.logger import LOGGER
from .const import ROOT_FOLDER_METADATA, CREDENTIALS_FILE_PATH
from .utils import content_exist


class GoogleDriveConnector:
    """ This is the class that handle connection and interaction with the Google Drive. """
    instance_ = None
    google_drive = None

    def __new__(cls, credential_file: str = CREDENTIALS_FILE_PATH):
        """ Method to create a new instance of the GoogleDriveConnector class.

        :param credential_file: The path to the credential file.
        """
        if not cls.instance_:
            cls.instance_ = super(GoogleDriveConnector, cls).__new__(cls)
            cls.__credential_file = credential_file
            cls.__google_auth: GoogleAuth = GoogleAuth()
            cls.google_drive: GoogleDrive or None = None
            cls.instance_.connect()
            LOGGER.info('Connected to Google Drive')
        else:
            cls.instance_.refresh_connection()
            LOGGER.info('Refreshing token to Google Drive')
        return cls.instance_

    def __init__(self):
        """ Constructor for the GoogleDriveConnector class. """
        pass

    def connect(self):
        """ Connect to the Google Drive.

        :return: A connected Google Drive object
        """
        if self.google_drive:
            return self.google_drive
        self.__google_auth.LoadCredentialsFile(credentials_file=self.__credential_file)
        if not self.__google_auth.credentials:
            self.__google_auth.LocalWebserverAuth()
        elif self.__google_auth.access_token_expired:
            self.__google_auth.Refresh()
        else:
            self.__google_auth.Authorize()
        self.__google_auth.SaveCredentialsFile(self.__credential_file)
        self.google_drive = GoogleDrive(self.__google_auth)

    def refresh_connection(self):
        """ This function will refresh the connection to the Google Drive when the token has expired. """
        if self.__google_auth.access_token_expired:
            self.__google_auth.Refresh()
            self.__google_auth.SaveCredentialsFile(self.__credential_file)
            self.google_drive = GoogleDrive(self.__google_auth)

    def create_directories(self):
        """ This function will create the nested directories/folders within the Google Drive. """
        root_folder = content_exist(google_drive=self.google_drive, folder_name=ROOT_FOLDER_METADATA['title'])
        folders_ids = {
            "root_directory": root_folder['id'] if root_folder else None,
            "partners": {key: None for key in ALLOWED_PARTNERS}
        }
        if not folders_ids['root_directory']:
            self.google_drive.CreateFile(ROOT_FOLDER_METADATA).Upload()
            folder = content_exist(google_drive=self.google_drive, folder_name=ROOT_FOLDER_METADATA['title'])
            folders_ids['root_directory'] = folder['id'] if folder else None

        for partner in ALLOWED_PARTNERS:
            folder = content_exist(self.google_drive, partner, folders_ids['root_directory'])
            folders_ids['partners'][partner] = folder['id'] if folder else None
            if not folders_ids['partners'][partner]:
                self.google_drive.CreateFile({
                    "title": partner,
                    "parents": [{"id": folders_ids['root_directory']}],
                    "mimeType": ROOT_FOLDER_METADATA['mimeType']
                }).Upload()
                folder = content_exist(self.google_drive, partner, folders_ids['root_directory'])
                folders_ids['partners'][partner] = folder['id'] if folder else None
        return folders_ids

    def upload_file(self, partner: str, file_path: str) -> dict:
        """ This function will upload the file to the Google Drive.

        :param partner: The partner organisation.
        :param file_path: The path to the file to be uploaded.
        """
        parent_folder = content_exist(google_drive=self.google_drive, folder_name=ROOT_FOLDER_METADATA['title'])
        parent_folder_id = parent_folder['id'] if parent_folder else None
        directory = content_exist(google_drive=self.google_drive, folder_name=partner, parent=parent_folder_id)
        directory_id = directory['id'] if directory else None
        file_metadata = {
            'title': 'SAMPLE_TEST',
            'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'parents': [{'id': directory_id}]
        }
        file = self.google_drive.CreateFile(metadata=file_metadata)
        file.SetContentFile(file_path)
        file.Upload()
        file.content.close()
        return content_exist(google_drive=self.google_drive, folder_name=file_metadata['title'],
                             parent=directory_id, type_='file')
