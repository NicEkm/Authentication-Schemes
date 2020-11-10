import urllib.parse
import asyncio
import json
import aiohttp
import jwt
from aiohttp import web
from yarl import URL
from others.token_validation import Token_validation as tv


tokenDict = {'id_token':''} # tokenDict is empty as default
decoding_key = 'myencodingkey' # Hard coded decoding_key (used to validate id_token)

class Authlib_authcode:
    def __init__(self):
        pass

    # Function that validates token if it already exists in tokenDict.
    def token_validation(self, id_token, decoding_key):
        validation = tv(id_token, decoding_key).validate_token()
        return validation


    #############################################################################################################
    ''' Authlib Authorization code flow '''
    #######################################################################################################

    # Takes base request and if id_token doesn't already exist
    # Redirects user to authentication provider (auth-server)

    async def handle(self):
        # Checks if id_token exists
        if tokenDict['id_token'] == '':
            print('Redirecting to auth-server!')
            redirecturl = 'http://localhost:8080/authorization3'
            return web.Response(text=redirecturl)
        # If it exists starts to vvalidate it
        if tokenDict['id_token'] != '':
            id_token = tokenDict['id_token']
            text = await self.token_validation(id_token, decoding_key)
            return web.Response(text=json.dumps(text))


    # Takes authentication code from test-cli
    # Sends it to auth-server to be validated and then receives
    # Id_token from it.  
    async def authorization(self, request):
        response = request.url
        url = URL(response)
        querys = url.query
        auth_code = str(querys['code'])
        state = str(querys['state'])
        if auth_code != '' and state != '':
            print('Authorization code received! \nSending it to auth-server..')
            payload = {
                    'authorization_code':auth_code,
                    'state':state,
                }
            async with aiohttp.ClientSession() as session:
                async with session.post('http://localhost:8080/oauth/token2',
                                        data=payload) as resp:
                    post = await resp.json(content_type='text/plain')
                    id_token = post['id_token']
                    print('id_token received!')
                    tokenDict['id_token'] = id_token # Saves id_token for further use         
                    location = request.app.router['authlib_authcode_base'].url_for()
                    await session.close()
                    return web.HTTPFound(location=location)
        if auth_code == '' or state == '':
            msg = 'Error occured, Invalid auth_code or state!'
            return web.Response(text=msg)
        
        
