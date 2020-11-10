import aiohttp
import asyncio
import jwt
import json
import sys



mysecret = 'mysecretflower'  # User secret AKA password
client_id = '3' # User id AKA username



###################################################################################################################
                                
""" Authorization code flow """



# Tries to access api information and starts authentication process with authorization code flow.
async def get_api_data1():
    try:
        print('Trying to access API data..')
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:9090/') as resp1:       
                response = await resp1.text() 
                if response[0:4] == 'http': # Get's redirect url or json response.
                    await asyncio.sleep(.1)
                    # Define user credentials and parameters
                    payload = {
                        'client_id':client_id,
                        'secret':mysecret,
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
        return e



##################################################################################################################
                                                
""" implict flow """




# Tries to access api information and starts authentication process with implict flow.
async def get_api_data2():
    try:
        print('Trying to access API data..')
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:9090/api') as resp1:       
                response = await resp1.text() # Get's redirect url or json response.
                if response[0:4] == 'http':
                    await asyncio.sleep(.1)
                    #Define user credentials and parameters
                    payload = {
                        'client_id':client_id,
                        'secret':mysecret,
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
        return e






#############################################################################################################

''' Authentication flow with libraries '''

''' Aiohttp, authlib '''

async def get_api_data3():
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
            client_secret = 'mysecret'
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
        return e
    
    




##############################################################################################################

''' Implict flow with libraries '''

''' Aiohttp, authlib '''


async def get_api_data4():
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
            client_secret = 'mysecret'
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
        if response[0:4] != 'http': # If user is already authenticated response returns json data, instead of http-address.
            return print('You are already authenticated to this provider.\nJson data is: ',response)      
    except Exception as e:
        return e
   
# Runs async functions and waits them to be ready.
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if len(sys.argv) == 2: 
        runType = sys.argv[1] # Takes cli (command line interface) argument and defines it.
        if runType == '-a': # For authentication code flow
            loop.run_until_complete(get_api_data1())
            loop.close()
        if runType == '-i': # For implict flow
            loop.run_until_complete(get_api_data2())
            loop.close()
        if runType == '-la': # For authentication code flow using libraries
            loop.run_until_complete(get_api_data3())
            loop.close()
        if runType == '-li': # For implict flow using libraries
            loop.run_until_complete(get_api_data4())
            loop.close()
        if runType != '':
            if runType != '-i':
                if runType != '-a':
                    if runType != '-la':
                        if runType != '-li':
                            print('Invalid authorization type..')
    if len(sys.argv) != 2: # If there is no argument in python call, asks argument from user
        print('Enter authorization type -a ("Authorization code flow") or -i ("Implict flow") or -la ("Authorization code flow with libraries") or -li ("Implict flow with libraries")')

    

