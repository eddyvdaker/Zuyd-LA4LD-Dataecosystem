from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    """
    Returns an API friendly error (as opposed to the standard html errors

    :param status_code: <int> http status code
    :param message: <str> message with extra information
    :return: returns http response with json payload and correct status code
    """
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    """
    Bad Request is a generic error message for bad API calls.

    :param message: <str> The message to be send with the error response
    :return: calls error_response for Bad Request
    """
    return error_response(400, message)
