import json
import asyncio
import aiohttp
import jwt




class Authentication_methods:

    def __init__(self, client_id, mysecret):
        self.client_id = client_id # Username
        self.mysecret = mysecret # Password
        
    

    ##################################################################################################################                                                  
    """ Native Implict flow """
    ##############################################################################################################
    
    # Tries to access api information and starts authentication process with implict flow.
    async def authenticate(self):
        try:
            print('Trying to access API data using native implict flow...')
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:9090/api') as resp1:       
                    response = await resp1.text() # Get's redirect url or json response.
                    if response[0:4] == 'http':
                        await asyncio.sleep(.1)
                        #Define user credentials and parameters
                        payload = {
                            'client_id':self.client_id,
                            'secret':self.mysecret,
                            'scope':'openid',
                            }
                        # Makes authentication request to auth-server to get id_token
                        async with session.post(response,
                                                data=payload) as resp: # Request redirect url and gets auth_code from auth-server.
                            id_token = await resp.text()
                            if id_token != '':
                                payload = {
                                        'id_token':id_token,
                                    }
                                async with session.post('http://localhost:9090/openid/connect/id_token',
                                                        data=payload) as resp2: # Sends id_token to api-server and gets authenticated to api-server
                                                                                # if id_token is correct
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