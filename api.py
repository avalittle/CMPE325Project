#!/usr/bin/python

# Utility to generate response object
def success(statusCode, msg, body=None):
    if body is None:
        response_body = {'message': msg}
    else:
        response_body = body

    return response_body, statusCode


def error(statusCode, errortype, msg):
    response_body = {
        'errorType': errortype, 
        'message': msg
    }
    return response_body, statusCode