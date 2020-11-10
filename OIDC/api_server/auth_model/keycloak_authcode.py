import requests
import urllib.parse
import asyncio
import json
import aiohttp
import jwt
from aiohttp import web
from yarl import URL
from others.keycloak_token_validation import Token_validation as tv



tokenDict = {'id_token':''} # tokenDict is empty as default

class Keycloak_authcode:
    def __init__(self):
        pass

    # Function that validates token if it already exists in tokenDict.
    def token_validation(self, id_token):
        validation = tv(id_token).validate_access_token()
        return validation


    ##############################################################################################################
    """ Keycloak Authorization code flow """
    ##############################################################################################################

    async def handle(self):
        # Checks if id_token exists
        if tokenDict['id_token'] == '':
            print('Redirecting to auth-server!')
            redirecturl = 'http://localhost:8080/auth/realms/myrealm/protocol/openid-connect/auth?client_id=auth-server&response_type=code'
            return web.Response(text=redirecturl)
        # If it exists starts to vvalidate it
        if tokenDict['id_token'] != '':
            print('Validating id_token...')
            id_token = tokenDict['id_token']
            text = await self.token_validation(id_token)
            return web.Response(text=json.dumps(text))

    async def authorization(self, request):
        print('Authorization code received from test-cli!')
        await asyncio.sleep(1)
        post = await request.post()
        auth_code = post['auth_code']
        client_id = post['client_id']
        client_secret = post['client_secret']
        redirect_uri = post['redirect_uri']
        url = 'http://localhost:8080/auth/realms/myrealm/protocol/openid-connect/token'
        payload = {
            "Content-Type": "application/x-www-form-urlencoded",
            'grant_type':'authorization_code',
            'client_id':client_id,
            'client_secret':client_secret,
            'code':auth_code,
            'redirect_uri':redirect_uri,
            }
        try: 
            print('Trying to trade authorization code to id token..')   
            request_data = requests.post(url, data=payload)
            response = request_data.json()
            id_token = response['access_token']
            tokenDict['id_token'] = id_token # Saves id_token for further use
            location = request.app.router['keycloak_authcode_base'].url_for()
            print('ID token received successfully.')
            return web.HTTPFound(location=location)
        except Exception:
            text = 'Something went wrong, please check that auth_code and payload are correct. (Auth code is one time useable)'
            return print(text)
        
        
