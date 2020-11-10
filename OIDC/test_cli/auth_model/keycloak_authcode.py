import json
import asyncio
import aiohttp
import jwt
# Import get_auth_code module that gets auth_code for given credentials
from others.get_auth_code import Get_Auth_Code as GAC 



class Authentication_methods:

    def __init__(self, client_id, mysecret):
        self.client_id = client_id # Usernames
        self.mysecret = mysecret # Password
        
    

    ##############################################################################################################
    """ Keycloak Authorization code flow """
    ##############################################################################################################
    
    async def authenticate(self):
        print('Trying to access API data using Authorization code flow and keycloak auth-server...')
        async def get_redirect_url():
                async with aiohttp.ClientSession() as session1:
                    async with session1.get('http://localhost:9090/api_data/auth_code/keycloak') as resp:       
                        response = await resp.text() # Get's redirect url or json response.
                        return response
        redirect_url = await get_redirect_url()
        if redirect_url[0:4] == 'http':
            print('Gaining authorization code from keycloak..')
            auth_code = GAC(redirect_url, self.client_id, self.mysecret).Auth_code() # Use get_auth_code module to gain auth_code
            payload = {
                    'auth_code':auth_code,
                    'client_id':'auth-server',
                    'client_secret':'dd61da64-60bc-4db8-b0a2-13b34a1fa5d6',
                    'redirect_uri':'http://localhost:8081/callback',
                    }
            print('Sending authorization code to api-server..')
            async with aiohttp.ClientSession() as session:
                async with session.post('http://localhost:9090/api_data/authorization_code',
                                    data=payload) as resp2: # Sends auth_code to api-server and gets authenticated to api-server
                                                            # if auth_code is correct
                    response2 = await resp2.text()
                    if response2[0:4] == '"Err':
                        return print(response2)
            return print('Success!\nJson data is: ',response2)
        if redirect_url[0:4] == '{"me':
            return print('You are already authenticated to this provider.\nJson data is: ',redirect_url)
        if redirect_url[0:4] == '"Err': # If response = error message, print error message
            return print(redirect_url) 

