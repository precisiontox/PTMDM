from os import path
from unittest import TestCase
from unittest.mock import patch

from pydrive2.auth import GoogleAuth

from ptmd.lib import GoogleDriveConnector


class MockGoogleAuth(GoogleAuth):
    credentials = None
    access_token_expired = True

    def LoadCredentialsFile(*args, **kwargs):
        pass

    def LocalWebserverAuth(*args, **kwargs):
        pass

    def SaveCredentialsFile(*args, **kwargs):
        pass

    def Refresh(*args, **kwargs):
        pass

    def Authorize(self, *args, **kwargs):
        pass

    def SaveCredentials(self, backend=None):
        pass


class ContentMock:
    def __init__(self, *args, **kwargs):
        pass

    def close(self):
        pass


class FileMock(dict):
    content = ContentMock()

    def Upload(self):
        return {'id': '1234'}

    def SetContentFile(self, *args, **kwargs):
        pass

    def InsertPermission(self, *args, **kwargs):
        pass

    def GetContentFile(self, *args, **kwargs):
        return {"title": "title test"}

    def Delete(self, *args, **kwargs):
        pass

    def CreateFile(self, *args, **kwargs):
        return self

    def GetPermissions(self, *args, **kwargs):
        return [{'id': '1234'}]

    def DeletePermission(self, *args, **kwargs):
        pass


class MockGoogleDrive:
    def CreateFile(self, *args, **kwargs):
        return FileMock()


class MockGoogleDriveForFilename:
    def CreateFile(self, *args, **kwargs):
        return {"title": "title test"}


@patch('ptmd.lib.gdrive.core.GoogleAuth')
class TestGetFileName(TestCase):
    def test_get_filename(self, google_auth_mock):
        with patch('ptmd.lib.gdrive.core.GoogleDrive') as google_drive_mock:
            google_drive_mock.return_value.CreateFile.return_value = {"title": "title test"}
            gdrive_connector = GoogleDriveConnector()
            filename = gdrive_connector.get_filename(file_id="123")
            self.assertEqual(filename, "title test")


@patch('ptmd.lib.gdrive.core.GoogleAuth', return_value=MockGoogleAuth)
@patch('ptmd.lib.gdrive.core.GoogleDrive', return_value=MockGoogleDrive())
class TestGoogleDriveConnector(TestCase):

    def test_constructor(self, google_drive_mock, google_auth_mock):
        gdrive_connector = GoogleDriveConnector()
        self.assertIsNotNone(gdrive_connector.google_drive)
        gdrive_connector.connect()
        self.assertIsNotNone(gdrive_connector.google_drive)

        gdrive_connector.google_drive = None
        gdrive_connector._GoogleDriveConnector__google_auth = MockGoogleAuth()
        gdrive_connector.connect()
        self.assertIsNotNone(gdrive_connector.google_drive)

        gdrive_connector.google_drive = None
        gdrive_connector._GoogleDriveConnector__google_auth = MockGoogleAuth()
        gdrive_connector._GoogleDriveConnector__google_auth.credentials = True
        gdrive_connector._GoogleDriveConnector__google_auth.access_token_expired = False
        gdrive_connector.connect()
        self.assertIsNotNone(gdrive_connector.google_drive)

    @patch('ptmd.lib.gdrive.core.get_folder_id', return_value=None)
    def test_create_directories_skip(self, content_exist_mock, google_drive_mock, google_auth_mock):
        gdrive_connector = GoogleDriveConnector()
        gdrive_connector.create_directories()
        self.assertEqual(20, content_exist_mock.call_count)

    @patch('ptmd.lib.gdrive.core.get_folder_id', return_value=None)
    def test_create_directories_no_files(self, google_drive_mock, content_exist_mock, google_auth_mock):
        gdrive_connector = GoogleDriveConnector()
        folders_ids, files = gdrive_connector.create_directories()
        for file in files.items():
            self.assertIsNotNone(file)
        self.assertIsNone(folders_ids['root_directory'])
        for partner in folders_ids['partners']:
            self.assertIsNone(folders_ids['partners'][partner]['g_drive'])
            self.assertIsNotNone(folders_ids['partners'][partner]['long_name'])

        gdrive_connector2 = GoogleDriveConnector()
        self.assertEqual(gdrive_connector, gdrive_connector2)
        gdrive_connector2.google_drive = None
        gdrive_connector2._GoogleDriveConnector__google_auth.access_token_expired = True
        gdrive_connector2.connect()
        self.assertIsNotNone(gdrive_connector2.google_drive)

    @patch('ptmd.lib.gdrive.core.get_folder_id', return_value={'id': '1234'})
    @patch('ptmd.lib.gdrive.core.find_files_in_folder', return_value=[{'id': '1234'}])
    def test_create_directories_with_files(self, mock_find_files_in_folder, mock_get_folder,
                                           content_exist_mock, google_auth_mock):
        gdrive_connector = GoogleDriveConnector()
        folders_ids, files = gdrive_connector.create_directories()
        for file in files.items():
            self.assertEqual(file[1], [{'id': '1234'}])

    def test_download_file(self, google_drive_mock, google_auth_mock):
        gdrive_connector = GoogleDriveConnector()
        file_id = "123"
        file_metadata = gdrive_connector.download_file(file_id=file_id, filename='test.xlsx')
        self.assertNotIn('test.xlsx', file_metadata)
        self.assertIn('test_', file_metadata)
        self.assertIn('.xlsx', file_metadata)


@patch('ptmd.lib.gdrive.core.GoogleAuth')
@patch('ptmd.lib.gdrive.core.GoogleDrive')
class TestUploader(TestCase):

    def setUp(self) -> None:
        here = path.abspath(path.dirname(__file__))
        self.xlsx_file = path.join(here, '..', '..', 'data', 'excel', 'test.xlsx')

    @patch('ptmd.lib.gdrive.core.get_file_information', return_value={'id': '1234'})
    def test_upload_file(self, content_exist_mock, google_drive_mock, google_auth_mock):
        google_drive_mock.CreateFile().return_value = FileMock()
        gdrive_connector = GoogleDriveConnector()
        file_metadata = gdrive_connector.upload_file(file_path=self.xlsx_file, directory_id="123")
        self.assertEqual(content_exist_mock.return_value, file_metadata)

    @patch('ptmd.lib.gdrive.core.get_file_information', return_value={'id': '1234'})
    def test_update_file(self, content_exist_mock, google_drive_mock, google_auth_mock):
        google_drive_mock.CreateFile().return_value = FileMock()
        gdrive_connector = GoogleDriveConnector()
        file_metadata = gdrive_connector.update_file(file_id="1", file_path=self.xlsx_file, title="test")
        self.assertEqual(file_metadata, "1")

    def test_upload_file_no_file(self, google_drive_mock, google_auth_mock):
        google_drive_mock.CreateFile().return_value = None
        gdrive_connector = GoogleDriveConnector()
        self.assertIsNone(gdrive_connector.upload_file(file_path=self.xlsx_file, directory_id="123"))

    def test_upload_file_no_drive(self, google_drive_mock, google_auth_mock):
        google_drive_mock.return_value = None
        gdrive_connector = GoogleDriveConnector()
        self.assertIsNone(gdrive_connector.upload_file(file_path=self.xlsx_file, directory_id="123"))

    def test_delete_file_success(self, google_drive_mock, google_auth_mock):
        google_drive_mock.return_value = FileMock()
        gdrive_connector = GoogleDriveConnector()
        file_id = gdrive_connector.delete_file(file_id="123")
        self.assertEqual(file_id, '123')

    def test_delete_file_permission_denied(self, google_drive_mock, google_auth_mock):
        class FileError:
            def Delete(self):
                raise Exception()

        err = 'Unable to delete file 123 from Google Drive. This is probably because it is an external file.'
        google_drive_mock.return_value = FileError()
        gdrive_connector = GoogleDriveConnector()
        with self.assertRaises(PermissionError) as context:
            gdrive_connector.delete_file(file_id="123")
        self.assertEqual(str(context.exception), err)


@patch('ptmd.lib.gdrive.core.GoogleAuth')
class TestLockFile(TestCase):

    @patch('ptmd.lib.gdrive.core.GoogleDrive', return_value=MockGoogleDrive())
    def test_lock_file_success(self, drive_mock, google_auth_mock):
        gdrive_connector = GoogleDriveConnector()
        self.assertIsNone(gdrive_connector.lock_file(file_id="123"))

    @patch('ptmd.lib.gdrive.core.GoogleDrive', return_value=MockGoogleDrive())
    def test_lock_file_permission_denied(self, drive_mock, google_auth_mock):
        gdrive_connector = GoogleDriveConnector()
        gdrive_connector.google_drive = None
        with self.assertRaises(PermissionError) as context:
            gdrive_connector.lock_file(file_id="123")
        self.assertEqual(str(context.exception), "Unable to lock file 123 from Google Drive. This is probably because "
                                                 "it is an external file: "
                                                 "'NoneType' object has no attribute 'CreateFile'")
