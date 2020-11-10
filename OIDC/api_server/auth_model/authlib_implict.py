import urllib.parse
import asyncio
import json
import aiohttp
import jwt
from aiohttp import web
from yarl import URL
from others.token_validation import Token_validation as tv



# Global variables

tokenDict = {'id_token':''} # tokenDict is empty as default
decoding_key = 'myencodingkey' # Hard coded decoding_key (used to validate id_token)


class Authlib_implict:
    def __init__(self):
        pass

    # Function that validates token if it already exists in tokenDict.
    def token_validation(self, id_token, decoding_key):
        validation = tv(id_token, decoding_key).validate_token()
        return validation


    ##############################################################################################################
    ''' Authlib Implict flow '''
    ##############################################################################################################

    async def handle(self):
        # Checks if id_token exists

        # If it doesn't exists return redirect url.
        if tokenDict['id_token'] == '':
            print('Redirecting to auth-server!')
            redirecturl = 'http://localhost:8080/authorization4'
            return web.Response(text=redirecturl)
        # If it exists starts to vvalidate it
        if tokenDict['id_token'] != '':
            id_token = tokenDict['id_token']
            text = await self.token_validation(id_token, decoding_key)
            return web.Response(text=json.dumps(text))
        

    # Gets id token from test-cli and redirects back to origianl http request.
    async def receive_id_token(self, request):
        response = request.url   
        url = URL(response)
        querys = url.query
        id_token = querys['id_token']
        if id_token != '':
            print('id_token received!')
            tokenDict['id_token'] = id_token # Saves id_token for further use         
            location = request.app.router['authlib_implict_base'].url_for()
            return web.HTTPFound(location=location)
        if id_token == '':
            msg = 'Error occured, id_token is empty.'
            return web.Response(text=msg)