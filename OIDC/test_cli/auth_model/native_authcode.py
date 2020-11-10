import json
import asyncio
import aiohttp
import jwt




class Authentication_methods:

    def __init__(self, client_id, mysecret):
        self.client_id = client_id # Username
        self.mysecret = mysecret # Password
        
    
    ############################################################################################################## 
    """ Native Authorization code flow """
    ##############################################################################################################

    # Tries to access api information and starts authentication process with authorization code flow.
    async def authenticate(self):
        try:
            print('Trying to access API data using native authorization code flow...')
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:9090/') as resp1:       
                    response = await resp1.text() 
                    if response[0:4] == 'http': # Get's redirect url or json response.
                        await asyncio.sleep(.1)
                        # Define user credentials and parameters
                        payload = {
                            'client_id':self.client_id,
                            'secret':self.mysecret,
                            'scope':'openid',
                            }
                        async with session.post(response,
                                                data=payload) as resp: # Request redirect url and gets auth_code from auth-server.
                            auth_code = await resp.text()
                            if auth_code != '':
                                payload = {
                                        'auth_code':auth_code,
                                    }
                                async with session.post('http://localhost:9090/oauth/token',
                                                        data=payload) as resp2: # Sends auth_code to api-server and gets authenticated to api-server
                                                                                # if auth_code is correct
                                    response2 = await resp2.text()
                                    if response2[0:4] == '"Err':
                                        return print(response2)
                                    return print('Success!\nJson data is: ',response2)
                    if response[0:4] == '{"me':
                        return print('You are already authenticated to this provider.\nJson data is: ',response)
                    if response[0:4] == '"Err': # If response = error message, print error message
                        return print(response)     
        except Exception as e:
            return print(e)

