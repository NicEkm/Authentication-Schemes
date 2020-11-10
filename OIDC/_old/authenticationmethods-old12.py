import aiohttp
import asyncio
import jwt
import json






class Authentication_methods:

    def __init__(self, client_id, mysecret):
        self.client_id = client_id
        self.mysecret = mysecret
        
    


###################################################################################################################
                                    
    """ Authorization code flow """

##############################################################################################################



    # Tries to access api information and starts authentication process with authorization code flow.
    async def authentication_code_flow(self):
        try:
            print('Trying to access API data..')
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
                                    return print('Success!\nJson data is: ',await resp2.text())
                    if response[0:4] != 'http': # If user is already authenticated response returns json data, instead of http.
                        return print('You are already authenticated to this provider.\nJson data is: ',response)    
        except Exception as e:
            return print(e)



##################################################################################################################
                                                    
    """ implict flow """

##############################################################################################################



    # Tries to access api information and starts authentication process with implict flow.
    async def implict_flow(self):
        try:
            print('Trying to access API data..')
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
                                    return print('Success!\nJson data is: ',await resp2.text())
                    if response[0:4] != 'http': # If user is already authenticated response returns json data, instead of http-address.
                        return print('You are already authenticated to this provider.\nJson data is: ',response)    
        except Exception as e:
            return print(e)





#############################################################################################################

    ''' Authentication flow with libraries '''

    ''' Aiohttp, authlib '''

##############################################################################################################


    async def authentication_code_flow_with_libraries(self):
        try:
            print('Trying to access API data using authlib-library and authorization code flow..')
            from authlib.integrations.requests_client import OAuth2Session    
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
                            return print('Success!\n''Json data is: ',await resp.text())
            if response[0:4] != 'http': # If user is already authenticated response returns json data, instead of http-address.
                return print('You are already authenticated to this provider.\nJson data is: ',response)      
        except Exception as e:
            return print(e)
        
        




##############################################################################################################

    ''' Implict flow with libraries '''

    ''' Aiohttp, authlib '''
    
##############################################################################################################


    async def implict_flow_with_libraries(self):
        try:
            print('Trying to access API data using authlib-library and implict flow..')
            from authlib.integrations.requests_client import OAuth2Session    
            async def get_redirect_url():
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://localhost:9090/api_data/implict') as resp1:       
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
                            URI_response = ('http://localhost:9090/authorize2?' + response)
                            return URI_response
                URI_response = await authorization()
                if URI_response != '':
                    async with aiohttp.ClientSession() as session:
                        async with session.get(URI_response) as resp:
                            return print('Success!\n''Json data is: ',await resp.text())
            if response[0:4] == '{"me': # If user is already authenticated response returns json data, instead of http-address.
                return print('You are already authenticated to this provider.\nJson data is: ',response)
            if response[0:4] == '"Err': # If response = error message, print error message
                return print(response) 
        except Exception as e:
            return print(e)





##############################################################################################################

    """ Authentication code flow 
            with keycloak """

##############################################################################################################


    #async def authentication_code_flow_with_keycloak():
    #    try:
    #        print('Trying to access API data using authlib-library and implict flow..')
    #        from authlib.integrations.requests_client import OAuth2Session    
    #        async def get_redirect_url():
    #            async with aiohttp.ClientSession() as session:
    #                async with session.get('http://localhost:9090/api_data/implict') as resp1:       
    #                    response = await resp1.text() # Get's redirect url or json response.
    #                    return response
    #        response = await get_redirect_url()
    #




##############################################################################################################

    """ Implict flow 
        with keycloak """
    
##############################################################################################################
    


    async def implict_flow_with_keycloak(self):
        print('Trying to access API data using Implict flow and keycloak auth-server...')
        try:
            from keycloak import KeycloakOpenID

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
                            return print('Success!\nJson data is: ',await resp2.text())
            if response[0:4] == '{"me':
                return print('You are already authenticated to this provider.\nJson data is: ',response)
            if response[0:4] == '"Err': # If response = error message, print error message
                return print(response) 
        except Exception as e:
            return print(e)
   

##############################################################################################################
