import aiohttp
import asyncio
import jwt
import json
import ujson



mysecret = 'mysecretflower'


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


# creates new client session with /get request
# gets jwt-token fromm auth-server.
# Returns jwt-token

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

async def post_handler():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:9090/') as resp1:
                redirectURL = resp1.url# Creates new session
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
            
# makes new session to api-server that is redirected to auth server
async def practice():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:9090/') as resp:
            print(resp)
        
        
    

# Runs asyn functions and waits them to be ready.
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(practice())
    loop.close()
    

