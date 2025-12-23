from odoo.http import request


def valid_response(data, status, pagination_info):
    response_body = {
        'data': data,
        'message': 'successful'
    }
    if pagination_info:
        response_body['pagination_info'] = pagination_info
    return request.make_json_response(response_body, status=status)


def invalid_response(error, status):
    response_body = {
        'error': error,
    }
    return request.make_json_response(response_body, status=status)
