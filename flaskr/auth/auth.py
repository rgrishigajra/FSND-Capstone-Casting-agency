from functools import wraps

import requests
from flask import request
from jose import jwt

AUTH0_DOMAIN = ''
ALGORITHMS = ['RS256']
API_AUDIENCE = ''


class AuthError(Exception):
    """A standardized way to communicate auth failures"""
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    Obtains the access token from the authorization header
    :return: token
    """
    token = request.headers.get('Authorization')

    if not token:
        raise AuthError('no authorization header', 401)

    # analyse token parts
    token_parts = token.split()

    # should have 2 parts
    if len(token_parts) != 2:
        raise AuthError('authorization token should contain two parts', 401)

    bearer = token_parts[0]
    token = token_parts[1]

    # first part should be 'Bearer'
    if bearer.capitalize() != 'Bearer':
        raise AuthError('first part of the token should be Bearer', 401)

    return token


def verify_decode_jwt(token):
    jwks = requests.get('https://dev-wsb8jitr.auth0.com/.well-known/jwks.json')
    jwks = jwks.json()

    try:
        header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError('invalid token', 400)

    if 'kid' not in header:
        raise AuthError("'kid' not in header", 401)

    for key in jwks['keys']:
        if key['kid'] == header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer='https://' + AUTH0_DOMAIN + '/'
                )
                return payload
            except jwt.ExpiredSignatureError:
                raise AuthError('expired token', 401)
            except jwt.JWTClaimsError:
                raise AuthError('invalid claims', 401)
            except Exception:
                raise AuthError('invalid header', 400)
        else:
            raise AuthError('unauthorized', 401)


def check_permissions(permission, payload):
    permissions = payload.get('permissions')
    if not permissions or permission not in permissions:
        raise AuthError('unauthorized', 403)
    return True


def requires_auth(permission=''):
    """
    ensures user is authenticated and authorized to access the endpoint
    :param permission: the permissions required to access the endpoint
    """
    def requires_auth_decorator(f):
        """
        auth decorator to reuse in protecting endpoints
        :param f: endpoint that we'll be protecting
        """
        @wraps(f)
        def wrapper(*args, **kwargs):
            """
            ensures request has Authorization header with bearer token
            verifies the given token and checks the permissions embedded within it
            appropriate exceptions are raised if any step fails, else, access is granted
            """
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator