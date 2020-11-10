import asyncio
import json
import aiohttp
import jwt
from aiohttp import web
from others.token_validation import Token_validation as tv


tokenDict = {'id_token':''} # tokenDict is empty as default
decoding_key = 'myencodingkey' # Hard coded decoding_key (used to validate id_token)

class Native_implict:
    def __init__(self):
        pass

    # Function that validates token if it already exists in tokenDict.
    def token_validation(self, id_token, decoding_key):
        validation = tv(id_token, decoding_key).validate_token()
        return validation


    #######################################################################################################                
    """ Native Implict flow """
    #######################################################################################################

    async def handle(self):
        # If id_token not in 'tokenDict', redirects to auth-server
        if tokenDict['id_token'] == '':
            print('Redirecting to auth-server!')
            redirecturl = 'http://localhost:8080/authorization2'
            return web.Response(text=redirecturl)
        # If id_token in 'tokenDict', starts validating it..
        if tokenDict['id_token'] != '':
            id_token = tokenDict['id_token']
            text = await self.token_validation(id_token, decoding_key)
            return web.Response(text=json.dumps(text))
                
        
    # Takes id_token straight from test-cli and redirects back to '/'-request.
    async def receive_id_token(self, request):
        await asyncio.sleep(1)
        post = await request.post()
        id_token = post['id_token']
        tokenDict['id_token'] = id_token # Saves id_token for further use  
        location = request.app.router['native_implict_base'].url_for()
        return web.HTTPFound(location=location)

