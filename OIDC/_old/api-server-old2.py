from aiohttp import web
import aiohttp
import jwt
import asyncio
import json
import multidict


mysecret = 'mysecretflower'

# takes / request and does some random stuff
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

# Takes /get request, adds parameters to jwt token and generates jwt token
# for client. Response is json-data that contains jwt token for client.

async def receive_token(request):
    await asyncio.sleep(1)
    post = await request.post() # Gets post request, that includes jwt-token
    newToken = post.get('token') # Gets 'token' from multidict
    encodedToken = newToken.encode('UTF-8') # Encodes token
    actualData = jwt.decode(encodedToken, mysecret)
    print('Token received: ', encodedToken) # used to debug
    print('Message is: ', actualData) # used to debug

    if newToken != '':
        await send_token(newToken)
    else:
        print('Did not get token from end user.')

    


    
## Send token to auth-server for validating
    
async def send_token(newToken):
    try:
        async with aiohttp.ClientSession() as session:
            await asyncio.sleep(1)
            token = newToken
            payload = {'id':'3', 'token':token}
            async with session.post('http://localhost:8080/getinfo',
                                    data=payload) as resp:
                await print(resp)
    except Exception as e:
        pass
        
    
# Defines web application and http routes
app = web.Application()
app.add_routes([web.get('/', handle),
                web.post('/post', receive_token)]) # When request includes /post,
                                                    # activates receive_token() function 

if __name__ == '__main__':
    web.run_app(app, port=9090) # Opens web app to port 9090
