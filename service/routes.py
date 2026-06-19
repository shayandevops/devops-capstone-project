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
    return jsonify(status="OK"), status.HTTP_200_OK


############################################################
# INDEX
############################################################
@app.route("/")
def index():
    return jsonify(
        name="Account REST API Service",
        version="1.0",
    ), status.HTTP_200_OK


############################################################
# CREATE ACCOUNT
############################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    app.logger.info("Request to create an Account")

    check_content_type("application/json")

    account = Account()
    account.deserialize(request.get_json())
    account.create()

    message = account.serialize()

    location_url = url_for(
        "get_accounts",
        account_id=account.id,
        _external=False
    )

    return make_response(
        jsonify(message),
        status.HTTP_201_CREATED,
        {"Location": location_url}
    )


############################################################
# LIST ACCOUNTS
############################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    app.logger.info("Request to list Accounts")

    accounts = Account.all()
    results = [account.serialize() for account in accounts]

    return jsonify(results), status.HTTP_200_OK


############################################################
# READ SINGLE ACCOUNT
############################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    app.logger.info("Request to read Account id=%s", account_id)

    account = Account.find(account_id)

    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id {account_id} not found"
        )

    return jsonify(account.serialize()), status.HTTP_200_OK


############################################################
# UPDATE ACCOUNT
############################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    app.logger.info("Request to update Account id=%s", account_id)

    account = Account.find(account_id)

    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id {account_id} not found"
        )

    account.deserialize(request.get_json())
    account.update()

    return jsonify(account.serialize()), status.HTTP_200_OK


############################################################
# DELETE ACCOUNT
############################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    app.logger.info("Request to delete Account id=%s", account_id)

    account = Account.find(account_id)

    if account:
        account.delete()

    return "", status.HTTP_204_NO_CONTENT


############################################################
# UTIL
############################################################
def check_content_type(media_type):
    content_type = request.headers.get("Content-Type")

    if content_type == media_type:
        return

    app.logger.error("Invalid Content-Type: %s", content_type)

    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )