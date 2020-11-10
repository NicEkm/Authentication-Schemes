import json
import asyncio
import aiohttp
import jwt
from aiohttp import web
from others.token_validation import Token_validation as tv


# Glonal variables

tokenDict = {'id_token':''} # tokenDict is empty as default
decoding_key = 'myencodingkey' # Hard coded decoding_key (used to validate id_token)




class Native_authcode:
    def __init__(self):
        pass

    # Function that validates token if it already exists in tokenDict.
    def token_validation(self, id_token, decoding_key):
        validation = tv(id_token, decoding_key).validate_token()
        return validation


    #######################################################################################################      
    """ Native Authorization code flow """
    #######################################################################################################

    # takes '/' -request and handles it
    async def handle(self):
        # If id_token not in 'tokenDict', redirects to auth-server
        if tokenDict['id_token'] == '':
            print('Redirecting to auth-server!')
            redirecturi = 'http://localhost:8080/authorization'
            return web.Response(text=redirecturi)

        
        # If id_token is in 'tokenDict', validates it and then gives test-cli access to API
        if tokenDict['id_token'] != '':
            id_token = tokenDict['id_token']
            text = await self.token_validation(id_token, decoding_key)
            return web.Response(text=json.dumps(text))

    # Takes authorization_code from test-cli and
    # sends it to auth-server to be validated.
    # gets back id_token and saves it into 'tokenDict' - dictionary
    # Then redirects back to 'base' - request
    async def authorization(self, request):
        await asyncio.sleep(1)
        post = await request.post()
        auth_code = post.get('auth_code')
        if auth_code != 'Invalid client_id or secret!':
            print('Authorization code received! \nSending it to auth-server..')
            payload = {
                    'authorization_code':auth_code,
                }
            async with aiohttp.ClientSession() as session:
                async with session.post('http://localhost:8080/oauth/token',
                                        data=payload) as resp:
                    post = await resp.json(content_type='text/plain')
                    id_token = post['id_token']
                    print('id_token received!')
                    tokenDict['id_token'] = id_token # Saves id_token for further use  
                    location = request.app.router['native_authcode_base'].url_for()
                    await session.close()
                    return web.HTTPFound(location=location)
        if auth_code == 'Invalid client_id or secret!':
            print(auth_code)
            return web.Response(text=auth_code)
