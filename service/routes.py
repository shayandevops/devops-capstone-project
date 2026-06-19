"""
Account Service

This microservice handles the lifecycle of Accounts
"""

from flask import jsonify, request, make_response, abort, url_for
from service.models import Account
from service.common import status
from . import app


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


############################################################
# GET INDEX
############################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )


############################################################
# CREATE ACCOUNT
############################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint creates an account from posted data
    """
    app.logger.info("Request to create an Account")

    check_content_type("application/json")

    account = Account()
    account.deserialize(request.get_json())
    account.create()

    message = account.serialize()

    location_url = url_for(
        "get_accounts",
        account_id=account.id,
        _external=True,
    )

    return make_response(
        jsonify(message),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


############################################################
# READ ACCOUNT
############################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """
    Reads an Account
    This endpoint reads an account by account_id
    """
    app.logger.info("Request to read an Account with id: %s", account_id)

    account = Account.find(account_id)

    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id [{account_id}] could not be found.",
        )

    return account.serialize(), status.HTTP_200_OK


############################################################
# LIST ACCOUNTS
############################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all Accounts"""
    app.logger.info("Request to list Accounts")

    accounts = Account.all()
    account_list = [account.serialize() for account in accounts]

    return jsonify(account_list), status.HTTP_200_OK


############################################################
# UPDATE ACCOUNT
############################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """
    Updates an Account
    This endpoint updates an account by account_id
    """
    app.logger.info("Request to update Account with id: %s", account_id)

    account = Account.find(account_id)

    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id [{account_id}] could not be found.",
        )

    account.deserialize(request.get_json())
    account.update()

    return account.serialize(), status.HTTP_200_OK


############################################################
# DELETE ACCOUNT
############################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """
    Deletes an Account
    This endpoint deletes an account by account_id
    """
    app.logger.info("Request to delete Account with id: %s", account_id)

    account = Account.find(account_id)

    if account:
        account.delete()

    return "", status.HTTP_204_NO_CONTENT


############################################################
# UTILITY FUNCTIONS
############################################################
def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")

    if content_type and content_type == media_type:
        return

    app.logger.error("Invalid Content-Type: %s", content_type)

    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
