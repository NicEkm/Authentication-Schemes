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

class Keycloak_implict:
    def __init__(self):
        pass

    # Function that validates token if it already exists in tokenDict.
    def token_validation(self, id_token):
        validation = tv(id_token).validate_access_token()
        return validation


    #############################################################################################################
    ''' Keycloak Implict flow '''
    ##############################################################################################################
    
    async def handle(self):
        # Checks if id_token exists
        if tokenDict['id_token'] == '':
            print('Redirecting to auth-server!')
            redirecturl = 'http://localhost:8080/auth/'
            return web.Response(text=redirecturl)
        # If it exists starts to vvalidate it
        if tokenDict['id_token'] != '':
            print('Validating id_token...')
            id_token = tokenDict['id_token']
            text = await self.token_validation(id_token)
            return web.Response(text=json.dumps(text))
    async def get_access_token(self, request):
        print('Id token received from test-cli!')
        await asyncio.sleep(1)
        post = await request.post()
        id_token = post['access_token']
        tokenDict['id_token'] = id_token # Saves id_token for further use  
        location = request.app.router['keycloak_implict_base'].url_for()
        return web.HTTPFound(location=location)

        
        
