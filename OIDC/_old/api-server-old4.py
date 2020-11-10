from aiohttp import web
import aiohttp
import jwt
import asyncio
import json



# takes / request and redirects it to auth-server
async def handle(request):
    print('Redirecting to auth-server!')
    redirecturi = 'http://localhost:8080/checkauthentication'
    return web.Response(text=redirecturi)


#takes authorization_code from test-cli and
#sends it to auth-server to be validated.
#gets back ID_token
async def get_authorization_code(request):
    try:
        await asyncio.sleep(1)
        post = await request.post()
        auth_code = post.get('auth_code')
        if auth_code != 'Invalid client_id or secret!':
            print('Authorization code received!')
            payload = {
                    'authorization_code':auth_code,
                }
            async with aiohttp.ClientSession() as session:
                async with session.post('http://localhost:8080/oauth/token',
                                        data=payload) as resp:
                    post = await resp.json(content_type='text/plain')
                    ID_token = post['ID_token']
                    print('ID_token is:',ID_token)
        if auth_code == 'Invalid client_id or secret!':
            return print('Invalid client_id or secret!')
    except Exception as e:
        msg = 'Error!'
        return print(msg,e)
        


# Not used ATM
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

    

    

        
    
# Defines web application and http routes
app = web.Application()
app.add_routes([web.get('/', handle),
                web.post('/oauth/token', get_authorization_code, name='authorizate'),
                web.post('/post', receive_token, name='post')]) # When request includes /post,
                                                    # activates receive_token() function 

if __name__ == '__main__':
    web.run_app(app, port=9090) # Opens web app to port 9090
