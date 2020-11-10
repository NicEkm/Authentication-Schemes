from aiohttp import web
import jwt
import json
import asyncio

params = {'red':'flower'}
mysecret = 'mysecretflower'

# takes / request and does some random stuff
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

# Takes /get request, adds parameters to jwt token and generates jwt token
# for client. Response is json-data that contains jwt token for client.

async def token(request):
    print('New token request observed!')
    await asyncio.sleep(1)
    # Defines token parameters and client secret 'mysecretflower'
    token = jwt.encode(params, mysecret)
    tokenStr = token.decode('UTF-8')
    myJson = {'token':tokenStr}
    print('Token sent successful!')
    return web.Response(text=json.dumps(myJson))

async def handle_token(request):
    print('validating api-server request')
    await asyncio.sleep(1)
    post = await request.post()
    getToken = post.get('token')
    getID = post.get('id')
    encodedToken = getToken.encode('UTF-8')
    actualData = jwt.decode(encodedToken, mysecret)

    if actualData == params:
        msg = 'Correct token!'
        print(msg)
        newParams = {'fakeusername':'fakepassword'}
        newToken = jwt.encode(newParams, mysecret)
        decodedToken = newToken.decode('UTF-8')
        print(decodedToken)
        
        
    if actualData != params:
        msg = 'Invalid token, process timed out!'
        print(msg)

# Defines web application and http routes
app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/get', token),
                web.post('/getinfo', handle_token)])

if __name__ == '__main__':
    web.run_app(app)
