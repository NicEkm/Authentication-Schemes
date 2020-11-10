from aiohttp import web
import aiohttp
import jwt
import asyncio
import json


tokenDict = {'id_token':''} #tokenDict is empty as default
decoding_key = 'myencodingkey' #Hard coded decoding_key (used to validate id_token)

###########################################################################################################
                                        
""" Authorization code flow    """



# takes '/' -request and handles it
async def handle(request):
    #If id_token not in 'tokenDict', redirects to auth-server
    if tokenDict['id_token'] == '':
        print('Redirecting to auth-server!')
        redirecturi = 'http://localhost:8080/authorization'
        return web.Response(text=redirecturi)

    
    #If id_token is in 'tokenDict', validates it and then gives test-cli access to API
    if tokenDict['id_token'] != '':
        print('Validating id_token...')
        await asyncio.sleep(1)
        id_token = tokenDict['id_token']
        def decode_id_token():
            decoded_token = bool(jwt.decode(id_token, decoding_key, algorithms=['HS256']))
            if decoded_token == True:
                return True
            else:
                return False
        if decode_id_token() == True:
            text = {
                    'message':'success',
                    'company_info':'niclasOYJ',
                    'secret_animal':'tiger',
                  }
            print('User now have access to the api.')
            return web.Response(text=json.dumps(text))
        if decode_id_token() == False:
            text = {
                    'message':'Denied, user have no rights to this api!'
                  }
            print('User do not have access to the api!')
            return web.Response(text=json.dumps(text))

                    
                    
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



#######################################################################################################
                                        
""" Implict flow """



#handle '/' -request from test-cli
async def handle2(request):
    #If id_token not in 'tokenDict', redirects to auth-server
    if tokenDict['id_token'] == '':
        print('Redirecting to auth-server!')
        redirecturl = 'http://localhost:8080/authorization2'
        return web.Response(text=redirecturl)
    #If id_token in 'tokenDict', starts validating it..
    if tokenDict['id_token'] != '':
        print('Validating id_token..')
        await asyncio.sleep(1)
        id_token = tokenDict['id_token']
        def decode_id_token():
            decoded_token = bool(jwt.decode(id_token, decoding_key, algorithms=['HS256']))
            if decoded_token == True:
                return True
            else:
                return False
        #If id_token is valid, trusts user is authenticated and lets access to api-data
        if decode_id_token() == True:
            text = {
                'message':'success',
                'company_info':'niclasOYJ',
                'secret_animal':'tiger',
            } 
            print('User now have access to the api.')
            return web.Response(text=json.dumps(text))
        #If id_token is not valid (modified), user is not authenticated and have not access to api.
        if decode_id_token() == False:
            text = {
                'message':'Denied, user have no rights to this api!'
            }
            print('User do not have access to the api!')
            return web.Response(text=json.dumps(text))
            
    
#Takes id_token straight from test-cli and redirects back to '/'-request.
async def id_token_validation(request):
    await asyncio.sleep(1)
    post = await request.post()
    print('id_token received!')
    id_token = post['id_token']
    tokenDict['id_token'] = id_token
    location = request.app.router['main2'].url_for()
    return web.HTTPFound(location=location)




# Defines web application and http routes
app = web.Application()
app.add_routes([web.get('/', handle, name='main'),
                web.get('/api', handle2, name='main2'),
                web.post('/oauth/token', authorization, name='authorization'),
                web.post('/openid/connect/id_token', id_token_validation, name='oidc')
                ])

if __name__ == '__main__':
    web.run_app(app, port=9090) # Opens web app to port 9090
