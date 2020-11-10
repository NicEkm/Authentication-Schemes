import json
import asyncio
import aiohttp
import jwt
from authlib.integrations.requests_client import OAuth2Session




class Authentication_methods:

    def __init__(self, client_id, mysecret):
        self.client_id = client_id # Username
        self.mysecret = mysecret # Password
        
    



#############################################################################################################
    ''' Authentication flow with libraries '''

    ''' Aiohttp, authlib '''
##############################################################################################################


    async def authenticate(self):
        try:
            print('Trying to access API data using authlib-library and authorization code flow...')
            async def get_redirect_url():
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://localhost:9090/api_data') as resp1:       
                        response = await resp1.text() # Get's redirect url or json response.
                        return response
            response = await get_redirect_url()
            if response[0:4] == 'http': # If response is http address.
                await asyncio.sleep(.1)
                client_id = self.client_id
                client_secret = self.mysecret
                scope = 'openid'  # we want openid scope
                # Using authlib oauth session
                client = OAuth2Session(client_id, client_secret, scope=scope)
                authorization_endpoint = response
                uri, state = client.create_authorization_url(authorization_endpoint)
                async def authorization():
                    async with aiohttp.ClientSession() as session:
                        async with session.get(uri) as resp2:       
                            response = await resp2.text()
                            URI_response = ('http://localhost:9090/authorize?' + response)
                            return URI_response
                URI_response = await authorization()
                if URI_response != '': 
                    async with aiohttp.ClientSession() as session:
                        async with session.get(URI_response) as resp:
                            response2 = await resp.text()
                            if response2[0:4] == '"Err':
                                return print(response2)
                            return print('Success!\nJson data is: ',response2)
            if response[0:4] == '{"me':
                return print('You are already authenticated to this provider.\nJson data is: ',response)
            if response[0:4] == '"Err': # If response = error message, print error message
                return print(response)       
        except Exception as e:
            return print(e)
        
        