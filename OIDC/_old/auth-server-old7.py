from aiohttp import web
import aiohttp
import jwt
import json
import time
import asyncio

decoding_key = 'myencodingkey'  # Encoding key that is only known for auth-server
tokenDict = {'original_id_token': ''}

##########################################################################################################
""" Authorization code flow """


#Handle authorization request from test-cli,
#If test-cli credentials (username and password) fits user
#in database, return authorization code
async def handle_authentication(request):
    try:
        print('Validating test-cli authorization_code request..')
        await asyncio.sleep(1)
        post = await request.post()
        getSecret = post.get('secret')
        getID = post.get('client_id')
        userInfo = {'id': getID, 'secret': getSecret}
        database = openDatabase()

        # with for-loop
        def validation():
            for x in database:
                if x['id'] == userInfo['id'] and x['secret'] == userInfo[
                        'secret']:
                    auth_code = x['authorization_code']
                    return auth_code

        auth_code = validation()
        if auth_code != None:
            print('Sending authorization code to test-cli.. ')
            return web.Response(text=auth_code)
        if auth_code == None:
            msg = "Invalid client_id or secret!"
            print('User not in database, can not find authorization code..')
            return web.Response(text=msg)
    except Exception as e:
        msg = 'Error!'
        return (msg, e)


# Opens database and creates list of all users and their credentials.
def openDatabase():
    try:
        with open('./userdatabase.json') as infile:
            data = json.load(infile)
            mylist = []
            for x in data['Users']:
                mylist.append(x)
            return mylist
    except Exception as e:
        print("Failed to parse json file: ", e)


#Generates jwt token for current end-user.
async def token(authorization_code):
    try:
        await asyncio.sleep(1)
        database = openDatabase()
        for x in database:
            if authorization_code == x['authorization_code']:
                client_id = x['id']
                email = x['email']
                payload = {
                    'client_id': client_id,
                    'email': email,
                    'exp': time.time() + 120,
                    'scope': 'openid'
                }
                id_token = jwt.encode(payload, decoding_key,
                                      algorithm='HS256').decode('UTF-8')
                tokenDict['original_id_token'] = id_token
                return id_token
    except Exception as e:
        msg = 'Error occured!'
        return (msg, e)


#Takes authorization code from api-server, validates it and
#transfers it to ID_token and Access_token.
async def valid_auth_code(request):
    print(
        'New authorization_code validating request observed from api-server!')
    post = await request.post()
    authorization_code = post.get('authorization_code')
    database = openDatabase()
    try:

        def validating_authorization_code():
            for x in database:
                if x['authorization_code'] == authorization_code:
                    print("Found authorization_code pair!")
                    return True

        if validating_authorization_code() == True:
            id_token = await token(authorization_code)
            json_data = {
                'id_token': id_token,
                'Access_token': 'qwertyuiop1234'
            }
            print('Sending id_token to api-server..')
            return web.Response(text=json.dumps(json_data))
        else:
            msg = 'Error occured!'
            return web.Response(text=json.dumps(msg))
    except Exception as e:
        return ('Error: ', e)


######################################################################################################################################
"""  implict flow   """


#Takes test-cli authorization request and identifies user, if user
#is in database generates id_token for it.
async def handle_authentication2(request):
    try:
        print('Validating test-cli identity..')
        await asyncio.sleep(1)
        post = await request.post()
        getSecret = post.get('secret')
        getID = post.get('client_id')
        userInfo = {'id': getID, 'secret': getSecret}
        database = openDatabase()
        i = False

        # with for-loop
        def validation():
            for x in database:
                if x['id'] == userInfo['id'] and x['secret'] == userInfo[
                        'secret']:
                    i = True
                    return i
                else:
                    pass

        user_is_legit = validation()
        if user_is_legit == True:
            await asyncio.sleep(1)

            def id_token():
                database = openDatabase()
                for x in database:
                    client_id = x['id']
                    email = x['email']
                    payload = {
                        'client_id': client_id,
                        'email': email,
                        'exp': time.time() + 120,
                        'scope': 'openid'
                    }
                    id_token = jwt.encode(payload,
                                          decoding_key,
                                          algorithm='HS256').decode('UTF-8')
                    return id_token

            generate_token = id_token()
            print('Sending id_token to test-cli.. ')
            return web.Response(text=generate_token)
        if user_is_legit == False:
            msg = "Invalid client_id or secret!"
            print('User not in database, can not generate id_token')
            return web.Response(text=msg)
    except Exception as e:
        msg = 'Error!'
        return print(msg, e)


#############################################################################################################
''' Authentication flow with libraries '''
authDict = {'auth_code':''}
async def handle_authentication3(request):
    from yarl import URL
    import urllib.parse
    
    response = request.url
    print(await request.text())
    url = URL(response)
    print(url)
    querys = url.query
    response_type = querys['response_type']
    client_id = querys['client_id']
    scope = querys['scope']
    state = querys['state']
    print('response type: ', response_type, 'client id: ', client_id, 'scope: ', scope, 'state: ', state)
    database = openDatabase()
    i = False
    # with for-loop
    def validation():
        for x in database:
            if x['id'] == client_id:
                i = True
                return i
            else:
                pass
    user_is_legit = validation()
    if user_is_legit == True:
        await asyncio.sleep(1)
        import string
        import random
        def string_generator(size=35, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))
        auth_code = string_generator()
        print(auth_code)
        authDict['code'] = auth_code
        print(authDict['code'])
        redirect_uri = (urllib.parse.urlencode({"code":auth_code,"state":state}))
        return web.Response(text=redirect_uri)
    if user_is_legit == False:
        return 'Error! User not in database!'




##############################################################################################################
''' Implict flow with libraries '''








# Defines web application and http routes
app = web.Application()
app.add_routes([
    web.post('/authorization', handle_authentication, name='authorize'),
    web.post('/authorization2', handle_authentication2, name='authorize2'),
    web.get('/authorization3', handle_authentication3, name='authorize3'),
    web.post('/oauth/token', valid_auth_code, name='oauth'),
])

if __name__ == '__main__':
    web.run_app(app)
