import aiohttp
import asyncio
import jwt
import json



mysecret = 'mysecretflower'  # User password
client_id = '3' # User id aka username


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()



# Not used ATM
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/get') as resp:
            #print(resp.status)
            #print(resp.url)
            #print(resp.method)
            response = await resp.json(content_type='text/plain')
            newToken = response['token'] # Gets string from auth-server
            jwtToken = newToken.encode('UTF-8') # Encodes string backto bytes
            token = jwt.decode(jwtToken, mysecret) # Decode bytestring
            #print(newToken)
            #print(type(newToken))
            await session.close()
            return newToken

# Not used ATM
async def post_handler():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:9090/') as resp1:
                redirectURL = resp1.url# Creates new session with redirect url
                if redirectURL != '':
                    await asyncio.sleep(.1)
                    token = await main() # Gets jwt-token from auth server
                    print(token) # used to debug
                    payload = {"token":token} # Adds jwt-token to payload with parameter 'token', that will be sent to api-server
                    async with session.post(redirectURL, data=payload) as resp: # Connects to api-server and send post-request that, is used to debug
                        print(resp)
                else:
                    print('No redirect url detected!')
    except Exception as e: # gives weird error, that doesn't effect to post request, needs to be troubleshooted.
        pass
            

#Trys to access api information and starts authentication process.
async def get_api_info():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:9090/') as resp1:
                redirectURL = await resp1.text()# Creates new session with redirect url
                print(redirectURL)
                if redirectURL != '':
                    await asyncio.sleep(.1)
                    payload = {
                        'client_id':client_id,
                        'secret':mysecret,
                        'scope':'openid',
                        } 
                    async with session.post(redirectURL,
                                            data=payload) as resp: # Connects to auth-server
                        auth_code = await resp.text()
                        print('Message received:', auth_code)

                        if auth_code != '':
                            payload = {
                                    'auth_code':auth_code,
                                }
                            async with session.post('http://localhost:9090/oauth/token',
                                                    data=payload) as resp2:
                                print(resp2)
    except Exception as e:
        print(e)
                

        
        
    

# Runs asyn functions and waits them to be ready.
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_api_info())
    loop.close()
    

