import json
from flask import Blueprint, request

from cloud_common.cc.google import datastore
from .utils.auth import get_user_uuid_from_token
from .utils.response import success_response, error_response


get_user_info_bp = Blueprint('get_user_info_bp', __name__)


@get_user_info_bp.route('/api/get_user_info/', methods=['POST'])
def get_user_image():
    """Get user profile information.

    .. :quickref: User; User profile

    :reqheader Accept: application/json
    :<json string user_token: User Token returned from the /login API.

    **Example Response**:

      .. sourcecode:: json

        {
            "profile_image": null,
            "username": "exampleuser",
            "email_address": "user@example.org",
            "organization": "Example Foundation",
            "response_code": 200
        }

    """
    received_form_response = request.get_json()

    user_token = received_form_response.get("user_token")
    if user_token is None:
        return error_response(
            message="Please make sure you have added values for all the fields"
        )

    user_uuid = get_user_uuid_from_token(user_token)
    if user_uuid is None:
        return error_response(
            message="Invalid User: Unauthorized"
        )

    query = datastore.get_client().query(kind='Users')
    query.add_filter('user_uuid', '=', user_uuid)
    user = list(query.fetch(1))[0]

    return success_response(
        profile_image=user.get('profile_image'),
        username=user.get('username'),
        email_address=user.get('email_address'),
        organization=user.get('organization')
    )
