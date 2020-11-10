from aiohttp import web
import aiohttp
import jwt
import asyncio
import json


tokenDict = {'id_token':''} # tokenDict is empty as default
decoding_key = 'myencodingkey' # Hard coded decoding_key (used to validate id_token)


# Function that validates token if it already exists in tokenDict.
async def tokenDict_is_not_empty():
    print('Validating id_token...')
    await asyncio.sleep(1)
    id_token = tokenDict['id_token']
    # Decodes id_token to make sure it's valid and from correct provider
    def decode_id_token():
        try:
            decoded_token = bool(jwt.decode(id_token, decoding_key, algorithms=['HS256']))
        except Exception as e:
            text = 'Error, token has expired!'
            return text
        if decoded_token == True:
            return True
        else:
            return False
    # If id_token is valid, gives user access to json data
    if decode_id_token() == True:
        text = {
                'message':'success',
                'company_info':'niclasOYJ',
                'secret_animal':'tiger',
                }
        print('User now have access to the api.')
        return text
    # If id_token is not valid, returns error message.
    if decode_id_token() == False:
        text = {
                'message':'Denied, user have no rights to this api!'
                }
        print('User do not have access to the api!')
        return text
    if decode_id_token() == 'Error, token has expired!':
        msg = 'Error, token has expired'
        print(msg)
        return msg



###########################################################################################################
                                        
""" Authorization code flow    """

#######################################################################################################



# takes '/' -request and handles it
async def handle(request):
    # If id_token not in 'tokenDict', redirects to auth-server
    if tokenDict['id_token'] == '':
        print('Redirecting to auth-server!')
        redirecturi = 'http://localhost:8080/authorization'
        return web.Response(text=redirecturi)

    
    # If id_token is in 'tokenDict', validates it and then gives test-cli access to API
    if tokenDict['id_token'] != '':
        text = await tokenDict_is_not_empty()
        return web.Response(text=json.dumps(text))

                    
                    
# Takes authorization_code from test-cli and
# sends it to auth-server to be validated.
# gets back id_token and saves it into 'tokenDict' - dictionary
# Then redirects back to '/' - request
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
                tokenDict['id_token'] = id_token # Saves id_token for further use  
                location = request.app.router['main'].url_for()
                await session.close()
                return web.HTTPFound(location=location)
    if auth_code == 'Invalid client_id or secret!':
        print(auth_code)
        return web.Response(text=auth_code)



#######################################################################################################
                                        
""" Implict flow """

#######################################################################################################



# handle '/' -request from test-cli
async def handle2(request):
    # If id_token not in 'tokenDict', redirects to auth-server
    if tokenDict['id_token'] == '':
        print('Redirecting to auth-server!')
        redirecturl = 'http://localhost:8080/authorization2'
        return web.Response(text=redirecturl)
    # If id_token in 'tokenDict', starts validating it..
    if tokenDict['id_token'] != '':
        text = await tokenDict_is_not_empty()
        return web.Response(text=json.dumps(text))
            
    
# Takes id_token straight from test-cli and redirects back to '/'-request.
async def id_token_validation(request):
    await asyncio.sleep(1)
    post = await request.post()
    id_token = post['id_token']
    tokenDict['id_token'] = id_token # Saves id_token for further use  
    location = request.app.router['main2'].url_for()
    return web.HTTPFound(location=location)





#############################################################################################################

''' Authentication code flow with libraries '''

#######################################################################################################



# Takes base request and if id_token doesn't already exist
# Redirects user to authentication provider (auth-server)

async def handle3(request):
    # Checks if id_token exists
    if tokenDict['id_token'] == '':
        print('Redirecting to auth-server!')
        redirecturl = 'http://localhost:8080/authorization3'
        return web.Response(text=redirecturl)
    # If it exists starts to vvalidate it
    if tokenDict['id_token'] != '':
        text = await tokenDict_is_not_empty()
        return web.Response(text=json.dumps(text))


# Takes authentication code from test-cli
# Sends it to auth-server to be validated and then receives
# Id_token from it.  
async def get_auth_code_and_request_id_token(request):
    from yarl import URL
    import urllib.parse

    response = request.url
    url = URL(response)
    querys = url.query
    auth_code = querys['code']
    state = querys['state']
    if auth_code != '' and state != '':
        print('Authorization code received! \nSending it to auth-server..')
        payload = {
                'authorization_code':auth_code,
                'state':state,
            }
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:8080/oauth/token2',
                                    data=payload) as resp:
                post = await resp.json(content_type='text/plain')
                id_token = post['id_token']
                print('id_token received!')
                tokenDict['id_token'] = id_token # Saves id_token for further use         
                location = request.app.router['main3'].url_for()
                await session.close()
                return web.HTTPFound(location=location)
    if auth_code == '' or state == '':
        msg = 'Error occured, Invalid auth_code or state!'
        return web.Response(text=msg)
    
    



##############################################################################################################

''' Implict flow with libraries '''

##############################################################################################################



async def handle4(request):
    # Checks if id_token exists

    # If it doesn't exists return redirect url.
    if tokenDict['id_token'] == '':
        print('Redirecting to auth-server!')
        redirecturl = 'http://localhost:8080/authorization4'
        return web.Response(text=redirecturl)
    # If it exists starts to vvalidate it
    if tokenDict['id_token'] != '':
        text = await tokenDict_is_not_empty()
        return web.Response(text=json.dumps(text))
    

# Gets id token from test-cli and redirects back to origianl http request.
async def get_id_token(request):
    from yarl import URL
    import urllib.parse
    
    response = request.url   
    url = URL(response)
    querys = url.query
    id_token = querys['id_token']
    if id_token != '':
        print('id_token received!')
        tokenDict['id_token'] = id_token # Saves id_token for further use         
        location = request.app.router['main4'].url_for()
        return web.HTTPFound(location=location)
    if id_token == '':
        msg = 'Error occured, id_token is empty.'
        return web.Response(text=msg)






##############################################################################################################

""" Authentication code flow with keycloak """

##############################################################################################################



# EMPTY ATM




#############################################################################################################

''' Implict flow with keycloak '''

##############################################################################################################



async def handle5(request):
    # Checks if id_token exists
    if tokenDict['id_token'] == '':
        print('Redirecting to auth-server!')
        redirecturl = 'http://localhost:8080/auth/'
        return web.Response(text=redirecturl)
    # If it exists starts to vvalidate it
    if tokenDict['id_token'] != '':
        print('Validating id_token...')
        id_token = tokenDict['id_token']
        text = await validate_access_token(id_token)
        return web.Response(text=json.dumps(text))

    
async def validate_access_token(access_token):
    from keycloak import KeycloakOpenID

    keycloak_openid = KeycloakOpenID(server_url='http://localhost:8080/auth/',
                    client_id="auth-server",
                    realm_name="myrealm")
    def decode_access_token():
        try:
            decode_token = bool(keycloak_openid.userinfo(access_token))
        except Exception as e:
            text = 'Error, token has expired!'
            return text
        if decode_token == True:
            return True
        else:
            return False
    if decode_access_token() == True:
        print('Id token validation successful!')
        text = {
                'message':'success',
                'company_info':'niclasOYJ',
                'secret_animal':'tiger',
                }
        print('User now have access to the api.')
        return text
    # If id_token is not valid, returns error message.
    if decode_access_token() == False:
        print('Id token validation failed!')
        text = {
                'message':'Denied, user have no rights to this api!'
                }
        print('User do not have access to the api!')
        return text
    if decode_access_token() == 'Error, token has expired!':
        msg = 'Error, token has expired'
        print(msg)
        return msg
        

async def get_access_token(request):
    print('Id token received from test-cli!')
    await asyncio.sleep(1)
    post = await request.post()
    id_token = post['access_token']
    tokenDict['id_token'] = id_token # Saves id_token for further use  
    location = request.app.router['main5'].url_for()
    return web.HTTPFound(location=location)




##############################################################################################################

# Defines web application and http routes
app = web.Application()
app.add_routes([web.get('/', handle, name='main'),
                web.get('/api', handle2, name='main2'),
                web.get('/api_data', handle3, name='main3'),
                web.get('/api_data/implict', handle4, name='main4'),
                web.get('/api_data/keycloak', handle5, name='main5'),
                web.post('/api_data/access_token', get_access_token, name='access-token'),
                web.post('/oauth/token', authorization, name='authorization'),
                web.post('/openid/connect/id_token', id_token_validation, name='oidc'),
                web.get('/authorize', get_auth_code_and_request_id_token, name='id-token'),
                web.get('/authorize2', get_id_token, name='id-token-library-implict'),
                ])

if __name__ == '__main__':
    web.run_app(app, port=9090) # Opens web app to port 9090
