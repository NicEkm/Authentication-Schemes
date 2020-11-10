import aiohttp
import asyncio
import jwt
import json



mysecret = 'mysecretflower'  # User secret aka password
client_id = '3' # User id aka username


#Trys to access api information and starts authentication process.
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


        
# Runs async functions and waits them to be ready.
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_api_data())
    loop.close()
    

