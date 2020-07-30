import json
import os
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from flask import abort

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = os.getenv('ALGORITHMS')
API_AUDIENCE = os.getenv('API_AUDIENCE')

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
    def __repr__(self):
        return 'class'+str(self.error)+" code "+str(self.status_code)+' what'


# Auth Header

'''
get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if auth is None:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header not present'
        }, 401)
    auth = auth.split(' ')
    if len(auth) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header length error.'
        }, 401)
    if auth[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header doesnt start with bearer!'
        }, 401)
    return auth[1]


'''
 implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload
    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permissions, payload):
    if 'permissions' not in payload:
        abort(400)
    if permissions not in payload['permissions']:
        return False
    return True


'''
implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)
    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
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
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 401)
    return unverified_header


'''
@requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            # print(payload)
            if not check_permissions(permission, payload):
                raise AuthError({
                'code': 'invalid_header',
                'description': 'The user doesnt have permissions to perform this step'
            }, 401) 
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

ass_token= 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJWRXNSUnYwWUZRUDdtU3g5VGJ0TSJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYzM0eTlscS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMjAzYzNjMTNiMTMwMjI4ZjgxM2FhIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeUFQSSIsImlhdCI6MTU5NjA4NDA2NCwiZXhwIjoxNTk2MDkxMjY0LCJhenAiOiJYZXF3T3U2UHNBZUMwYndtMmRkNmdpTlAwSkphYXhJZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.FwRgsF9chpVTOKedMvPQKuq2BTtEsRMxxay9HO_sAse19rtN-bLAD6qE9f1nTByGnWoxtNZBmpDgl3ZYyioLgpx30AiGo7kzQkBZUUbDABu1PAIi8SSi_QdwMqAd735vIWgI7m3VOYl0PwLuDDbIr1jP3PEAVub3P-tcK3xAWvqUQZDcYIV-zVpooClMdIIeX9mtpmN04Pf6tpr-NcohBXNZDza2qRTThXprklLK9sd5dY7lh9pDfdxrPb4FDb7qL4OQ8I06EmdsYB5opIZ3ghMIdvRbJHhrwp6LMafCAxJVwq2-FsAZFX-RSn5N1vzvxzyvjEDVyJAh3D1E-ZzUhw'
director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJWRXNSUnYwWUZRUDdtU3g5VGJ0TSJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYzM0eTlscS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMjA2MjI1Yzg0OGYwMDM3YzQxNTJmIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeUFQSSIsImlhdCI6MTU5NjA4Mzk1NiwiZXhwIjoxNTk2MDkxMTU2LCJhenAiOiJYZXF3T3U2UHNBZUMwYndtMmRkNmdpTlAwSkphYXhJZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.RAfpcwZoiMbZQc6sfekgC5Yy9CyKW4kY4JPOfRptjyrPYqovl1TZ8cCng0CpxyeVq6PvFalGpEEVfcOF9oalTEw50ODRZ4nk7PINpMgfurcTjfibFBOEqBK6_-CuaOSgWdXxAaPDJaTwW3Nnn40Y_sbZeI5UJYS_OaXP5jLKDNZCTiMdLKxrieAEkiL86LZ9jbkQMWdsJLWn089KncWVj6XBjcY7RVTOjWO4QdK8BdI3gXazsY_T1dmPEkmnbYhcJPzrPXAFRgAoGPvMi2yP0_2Fx1BlUDao4J8KlQr-6BxMTYT-SASPu5CirHrkQK8Mll8iffE7Z5nP1JOIAjtdug'
prod_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJWRXNSUnYwWUZRUDdtU3g5VGJ0TSJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYzM0eTlscS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMjRkNGQ1Yzg0OGYwMDM3YzQxNzFkIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeUFQSSIsImlhdCI6MTU5NjA4Mzg1MSwiZXhwIjoxNTk2MDkxMDUxLCJhenAiOiJYZXF3T3U2UHNBZUMwYndtMmRkNmdpTlAwSkphYXhJZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.MNTt-R91aRc073xna4LFKDwwBr9pdQb_P-htAG5F4lzll9375VnR-YxKRPKgPGsgpb-_AhB24OLl1x7zoOIR9y7_OUxA48luJkp4kqoJs63MWOA4fR6dUfxVZafw_llx32gouoV_ZzI_TG3HJeRo1fI0OqHZ_OGPsVdMIvSjiHD1F9dYzX1gvtnKoRaZDvv9CtqlcNNIWl2fAhI6kWuimZsrkAkvFgF5QO7FHSSLppJkPKeLDnn_5ZtTIxlHkJg5CJw-pOwIciZn2tZSy9ZF8uIt9nCkhkjOPaGR2bI3_rD73_XfmzM6jeGA3Gg5TGf7IesswUcaOk1q6q3GswiWFA'
print('\n\nAssistant',verify_decode_jwt(ass_token),'\n\nDirector',verify_decode_jwt(director_token),'\n\nProducer',verify_decode_jwt(prod_token),'\n\n')