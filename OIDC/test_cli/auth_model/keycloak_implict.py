import json
import asyncio
import aiohttp
import jwt
from keycloak import KeycloakOpenID






class Authentication_methods:

    def __init__(self, client_id, mysecret):
        self.client_id = client_id # Username
        self.mysecret = mysecret # Password
        
    

    ##############################################################################################################
    """ Keycloak Implict flow """
    ##############################################################################################################
    
    async def authenticate(self):
        print('Trying to access API data using Implict flow and keycloak auth-server...')
        try:
            async def get_redirect_url():
                async with aiohttp.ClientSession() as session1:
                    async with session1.get('http://localhost:9090/api_data/keycloak') as resp1:       
                        response = await resp1.text() # Get's redirect url or json response.
                        return response
            response = await get_redirect_url()
            if response[0:4] == 'http':
                keycloak_openid = KeycloakOpenID(server_url=response,
                            client_id="auth-server",
                            realm_name="myrealm",
                            client_secret_key="dd61da64-60bc-4db8-b0a2-13b34a1fa5d6",
                            verify=True)
                username = self.client_id
                password = self.mysecret
                token = keycloak_openid.token(username, password)
                access_token = token['access_token']
                if access_token != '':
                    payload = {
                        'access_token':access_token
                    }
                    async with aiohttp.ClientSession() as session2:
                        async with session2.post('http://localhost:9090/api_data/access_token',
                                                data=payload) as resp2:
                            response = await resp2.text()
                            if response[0:4] == '"Err':
                                return print(response)
                            return print('Success!\nJson data is: ',response)
            if response[0:4] == '{"me':
                return print('You are already authenticated to this provider.\nJson data is: ',response)
            if response[0:4] == '"Err': # If response = error message, print error message
                return print(response) 
        except Exception as e:
            return print(e)
        