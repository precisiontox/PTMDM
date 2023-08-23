""" This module contains the API routes
"""
from os import path

from flask import Response
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from ptmd.config import app
from ptmd.api.queries import (
    login as login_user, change_password, get_me, logout, enable_account, validate_account, get_users,
    get_organisms, get_organisations,
    get_chemicals, create_chemicals, get_chemical,
    create_gdrive_file, create_user, validate_file,  register_gdrive_file, search_files_in_database, delete_file,
    get_sample, get_samples,
    ship_data, receive_data,
    convert_to_isa,
    send_reset_email, reset_password,
    change_role,
    delete_user,
    verify_token,
    batch_validation,
    update_batch
)
from ptmd.api.const import SWAGGER_DATA_PATH, FILES_DOC_PATH, USERS_DOC_PATH, CHEMICALS_DOC_PATH, SAMPLES_DOC_PATH


###########################################################
#                   USERS ROUTES                          #
###########################################################
@app.route('/api/users', methods=['PUT'])
@swag_from(path.join(USERS_DOC_PATH, 'change_password.yml'))
@jwt_required()
def change_pwd() -> tuple[Response, int]:
    """ Change the password of the current user """
    return change_password()


@app.route('/api/users', methods=['POST'])
@swag_from(path.join(USERS_DOC_PATH, 'create_user.yml'))
def user() -> tuple[Response, int]:
    """ Create a new user """
    return create_user()


@app.route("/api/user", methods=["GET"])
@swag_from(path.join(USERS_DOC_PATH, 'me.yml'))
@jwt_required()
def me() -> tuple[Response, int]:
    """ Get the current user"""
    return get_me()


@app.route("/api/users", methods=["GET"])
@swag_from(path.join(USERS_DOC_PATH, 'users.yml'))
@jwt_required()
def users() -> tuple[Response, int]:
    """ Get the current user"""
    return get_users()


@app.route("/api/session", methods=["POST"])
@swag_from(path.join(USERS_DOC_PATH, 'login.yml'))
def login() -> tuple[Response, int]:
    """ Route to log in a user """
    return login_user()


@app.route("/api/session", methods=["DELETE"])
@swag_from(path.join(USERS_DOC_PATH, 'logout.yml'))
@jwt_required()
def modify_token() -> tuple[Response, int]:
    """ Route to log out a user

    :return: the response and the status code"""
    return logout()


@app.route("/api/session", methods=["GET"])
@swag_from(path.join(USERS_DOC_PATH, 'test_token.yml'))
@jwt_required()
def test_token() -> tuple[Response, int]:
    """ Route to test the user JWT

    :return: the response and the status code
    """
    return verify_token()


@app.route("/api/users/enable/<token>", methods=["GET"])
@swag_from(path.join(USERS_DOC_PATH, 'enable_account.yml'))
def enable_account_(token: str) -> tuple[Response, int]:
    """ Route to enable a user account

    :param token: the token sent by email that will enable the account
    :return: the response and the status code
    """
    return enable_account(token)


@app.route("/api/users/<user_id>/activate", methods=["GET"])
@swag_from(path.join(USERS_DOC_PATH, 'validate_account.yml'))
def validate_account_(user_id: int) -> tuple[Response, int]:
    """ Route to validate a user account. This is an admin only route

    :param user_id: the id of the user to validate
    :return: the response and the status code
    """
    return validate_account(user_id)


@app.route('/api/users/request_reset', methods=['POST'])
@swag_from(path.join(USERS_DOC_PATH, 'request_reset.yml'))
def request_reset() -> tuple[Response, int]:
    """ Route to request a password reset

    :return: the response and the status code
    """
    return send_reset_email()


@app.route('/api/users/reset/<token>', methods=['POST'])
@swag_from(path.join(USERS_DOC_PATH, 'reset_pwd.yml'))
def reset_pwd(token: str) -> tuple[Response, int]:
    """ Route to reset the password

    :param token: the token sent by email that will enable the account
    :return: the response and the status code
    """
    return reset_password(token)


@app.route("/api/users/<user_id>/make_admin", methods=["GET"])
@swag_from(path.join(USERS_DOC_PATH, 'make_admin.yml'))
@jwt_required()
def make_admin(user_id: int) -> tuple[Response, int]:
    """ Route to make a user an admin. This is an admin only route

    :param user_id: the id of the user to make admin
    :return: the response and the status code
    """
    return change_role(user_id=user_id, role='admin')


@app.route("/api/users/<user_id>/ban", methods=["GET"])
@swag_from(path.join(USERS_DOC_PATH, 'ban_user.yml'))
@jwt_required()
def ban_user(user_id: int) -> tuple[Response, int]:
    """ Route to ban a user. This is an admin only route

    :param user_id: the id of the user to ban
    :return: the response and the status code
    """
    return change_role(user_id=user_id, role='banned')


@app.route("/api/users/<user_id>", methods=["DELETE"])
@swag_from(path.join(USERS_DOC_PATH, 'delete_user.yml'))
@jwt_required()
def delete_user_(user_id: int) -> tuple[Response, int]:
    """ Route to delete a user. Admin or user only route

    :param user_id: the id of the user to delete
    :return: the response and the status code
    """
    return delete_user(user_id)


###########################################################
#                     CHEMICALS                           #
###########################################################
@app.route('/api/chemicals', methods=['GET'])
@swag_from(path.join(CHEMICALS_DOC_PATH, 'get_chemicals.yml'))
@jwt_required()
def chemicals() -> tuple[Response, int]:
    """ Get the list of chemicals """
    return get_chemicals()


@app.route('/api/chemicals', methods=['POST'])
@swag_from(path.join(CHEMICALS_DOC_PATH, 'create_chemicals.yml'))
@jwt_required()
def new_chemicals() -> tuple[Response, int]:
    """ Create a new chemical """
    return create_chemicals()


@app.route('/api/chemicals/<ptx_code>', methods=['GET'])
@swag_from(path.join(CHEMICALS_DOC_PATH, 'get_chemical.yml'))
@jwt_required(optional=True)
def chemical(ptx_code: str) -> tuple[Response, int]:
    """ Get a chemical by its PTX code

    :param ptx_code: the PTX code of the chemical
    :return: the chemical and the status code
    """
    return get_chemical(ptx_code)


###########################################################
#                   MISCELLANEOUS                         #
###########################################################
@app.route('/api/organisms', methods=['GET'])
@swag_from(path.join(SWAGGER_DATA_PATH, 'organisms.yml'))
@jwt_required(optional=True)
def organisms() -> tuple[Response, int]:
    """ Get the list of organisms """
    return get_organisms()


@app.route('/api/organisations', methods=['GET'])
@swag_from(path.join(SWAGGER_DATA_PATH, 'organisations.yml'))
@jwt_required(optional=True)
def organisations() -> tuple[Response, int]:
    """ Get the list of organisations """
    return get_organisations()


###########################################################
#                          FILES                          #
###########################################################
@app.route('/api/files', methods=['POST'])
@swag_from(path.join(FILES_DOC_PATH, 'create_file.yml'))
@jwt_required()
def create_file() -> tuple[Response, int]:
    """ Create and saves the spreadsheet in the Google Drive """
    return create_gdrive_file()


@app.route('/api/files/<file_id>/validate', methods=['GET'])
@swag_from(path.join(FILES_DOC_PATH, 'validate_file.yml'))
@jwt_required()
def validate(file_id: int) -> tuple[Response, int]:
    """ Validate a file

    :param file_id: the id of the file to validate
    """
    return validate_file(file_id)


@app.route('/api/files/register', methods=['POST'])
@swag_from(path.join(FILES_DOC_PATH, 'register_file.yml'))
@jwt_required()
def register_file() -> tuple[Response, int]:
    """ Register a file from an external Google Drive """
    return register_gdrive_file()


@app.route('/api/files/search', methods=['GET'])
@jwt_required()
def search_files() -> tuple[Response, int]:
    """ Search files """
    return search_files_in_database()


@app.route('/api/files/<file_id>', methods=['DELETE'])
@swag_from(path.join(FILES_DOC_PATH, 'delete_file.yml'))
@jwt_required()
def delete_file_(file_id: int) -> tuple[Response, int]:
    """ Delete the given  file

    :param file_id: the id of the file to validate
    """
    return delete_file(file_id)


@app.route('/api/files/<file_id>/ship', methods=['POST'])
@swag_from(path.join(FILES_DOC_PATH, 'ship_file.yml'))
@jwt_required()
def ship_file(file_id: int) -> tuple[Response, int]:
    """ Ship the given file

    :param file_id: the id of the file to ship
    """
    return ship_data(file_id)


@app.route('/api/files/<file_id>/receive', methods=['POST'])
@swag_from(path.join(FILES_DOC_PATH, 'receive_file.yml'))
@jwt_required()
def receive_file(file_id: int) -> tuple[Response, int]:
    """ Receive the given file

    :param file_id: the id of the file to receive
    """
    return receive_data(file_id)


@app.route('/api/files/<file_id>/isa', methods=['GET'])
@swag_from(path.join(FILES_DOC_PATH, 'isa.yml'))
@jwt_required()
def file_to_isa(file_id: int) -> tuple[Response, int]:
    """ Convert the given file to ISA-Tab

    :param file_id: the id of the file to convert
    """
    return convert_to_isa(file_id)


@app.route('/api/batch/<batch_code>/validate', methods=['GET'])
@jwt_required()
def validate_batch(batch_code: str) -> tuple[Response, int]:
    """ Validate a batch code

    :param batch_code: the batch code to validate
    """
    return batch_validation(batch_code)


@app.route('/api/files/<file_id>/batch', methods=['GET'])
def update_file_batch(file_id):
    """ Update the batch code of the file

    :param file_id: the id of the file to update
    """
    return update_batch(file_id)


###########################################################
#                          SAMPLES                        #
###########################################################
@app.route('/api/samples/<sample_id>', methods=['GET'])
@swag_from(path.join(SAMPLES_DOC_PATH, 'get_sample.yml'))
@jwt_required(optional=True)
def get_sample_(sample_id: str) -> tuple[Response, int]:
    """ Get a sample by its id

    :param sample_id: the id of the sample to get
    """
    return get_sample(sample_id)


@app.route('/api/samples', methods=['GET'])
@swag_from(path.join(SAMPLES_DOC_PATH, 'get_samples.yml'))
@jwt_required()
def get_samples_() -> tuple[Response, int]:
    """ Get a list of paginated samples
    """
    return get_samples()
