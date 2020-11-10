from aiohttp import web
import aiohttp
import jwt
import asyncio
import json


tokenDict = {'id_token':''} #tokenDict is empty as default

   
# takes / request and handles it
async def handle(request):
    
    #If id_token not in 'tokenDict', redirects to auth-server
    if tokenDict['id_token'] == '':
        print('Redirecting to auth-server!')
        redirecturi = 'http://localhost:8080/authorization'
        return web.Response(text=redirecturi)
    
    #If id_token is in 'tokenDict', validates it through auth-server and then gives test-cli access to API
    
    if tokenDict['id_token'] != '':
        print('Validating id_token..')
        async with aiohttp.ClientSession() as session:
            id_token = tokenDict['id_token']
            payload = {
                    'id_token':id_token
                }
            async with session.post('http://localhost:8080/uservalidation',
                                    data=payload) as resp:
                user_has_rights = await resp.text()
                if user_has_rights == 'True':
                    #text = {'Message':'This is super secret message, not many people sees this!'}
                    print('User now have access to the api.')
                    location = request.app.router['API'].url_for()
                    raise web.HTTPFound(location=location)
                    await session.close()
                if user_has_rights == 'False':
                    text = {'Message':'Unfortunately you have no rights to this awesome api :('}
                    print('User do not have access to the api!')
                    
                    location = request.app.router['deny'].url_for()
                    raise web.HTTPFound(location=location)
                    await session.close()

#Takes authorization_code from test-cli and
#sends it to auth-server to be validated.
#gets back id_token and saves it into 'tokenDict' - dictionary
#Then redirects back to '/' - request
async def authorization(request):
    await asyncio.sleep(1)
    post = await request.post()
    auth_code = post.get('auth_code')
    if auth_code != 'Invalid client_id or secret!':
        print('Authorization code received! \nSending it to auth-server..')
        payload = {
                'authorization_code':auth_code,
            }
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:8080/oauth/token',
                                    data=payload) as resp:
                post = await resp.json(content_type='text/plain')
                id_token = post['id_token']
                print('id_token received!')
                tokenDict['id_token'] = id_token
                location = request.app.router['main'].url_for()
                await session.close()
                return web.HTTPFound(location=location)
    if auth_code == 'Invalid client_id or secret!':
        print(auth_code)
        return web.Response(text=auth_code)


#Api data that test-cli wants to access.
async def api_data(request):
    data = {
        'message':'success',
        'company_info':'niclasOYJ',
        'secret_animal':'tiger'
        }
    return web.Response(text=json.dumps(data))

#Deny redirect
async def deny_api_data(request):
    data = {
        'message':'denied',
        }
    return web.Response(text=json.dumps(data))
    
# Defines web application and http routes
app = web.Application()
app.add_routes([web.get('/', handle, name='main'),
                web.post('/oauth/token', authorization, name='authorization'),
                web.get('/api_info',api_data, name='API'),
                web.get('/api_deny',deny_api_data, name='deny'),
                ])

if __name__ == '__main__':
    web.run_app(app, port=9090) # Opens web app to port 9090
