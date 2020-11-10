import aiohttp
import asyncio
import jwt
import json
import sys



mysecret = 'mysecretflower'  #User secret AKA password
client_id = '3' #User id AKA username



###################################################################################################################
                                
""" Authorization code flow """



#Tries to access api information and starts authentication process with authorization code flow.
async def get_api_data():
    try:
        print('Trying to access API data..')
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:9090/') as resp1:       
                redirectURL = await resp1.text()#Get's redirect url.
                if redirectURL != '':
                    await asyncio.sleep(.1)
                    #Define user credentials and parameters
                    payload = {
                        'client_id':client_id,
                        'secret':mysecret,
                        'scope':'openid',
                        } 
                    async with session.post(redirectURL,
                                            data=payload) as resp: #Request redirect url and gets auth_code from auth-server.
                        auth_code = await resp.text()
                        if auth_code != '':
                            payload = {
                                    'auth_code':auth_code,
                                }
                            async with session.post('http://localhost:9090/oauth/token',
                                                    data=payload) as resp2: #Sends auth_code to api-server and gets authenticated to api-server
                                                                            #if auth_code is correct
                                return print(await resp2.text())
                                await session.close()
                else:
                    print(redirectURL)
    except Exception as e:
        return e



##################################################################################################################
                                                
""" implict flow """




#Tries to access api information and starts authentication process with implict flow.
async def get_api_data2():
    try:
        print('Trying to access API data..')
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:9090/api') as resp1:       
                redirectURL = await resp1.text()#Get's redirect url.
                if redirectURL != '':
                    await asyncio.sleep(.1)
                    #Define user credentials and parameters
                    payload = {
                        'client_id':client_id,
                        'secret':mysecret,
                        'scope':'openid',
                        }
                    #Makes authentication request to auth-server to get id_token
                    async with session.post(redirectURL,
                                            data=payload) as resp: #Request redirect url and gets auth_code from auth-server.
                        id_token = await resp.text()
                            if id_token != '':
                            payload = {
                                    'id_token':id_token,
                                }
                            async with session.post('http://localhost:9090/openid/connect/id_token',
                                                    data=payload) as resp2: #Sends id_token to api-server and gets authenticated to api-server
                                                                            #if id_token is correct
                                return print(await resp2.text())
                                await session.close()
                else:
                    print(redirectURL)
    except Exception as e:
        return e

    
   
# Runs async functions and waits them to be ready.
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if len(sys.argv) == 2: 
        runType = sys.argv[1] # Takes cli argument and defines it.
        if runType == '-a':
            loop.run_until_complete(get_api_data())
            loop.close()
        if runType == '-i':
            loop.run_until_complete(get_api_data2())
            loop.close()
        if runType != '':
            if runType != '-i':
                if runType != '-a':
                    print('Invalid authorization type..')
    if len(sys.argv) != 2: #If there is no argument sends error message and asks one.
        print('Enter authorization type -a ("authorization code flow") or -i ("implict flow")')

    

