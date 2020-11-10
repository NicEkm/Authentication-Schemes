import urllib.parse
import json
import time
import asyncio
import aiohttp
import jwt
from aiohttp import web
from yarl import URL

# Global variables

decoding_key = 'myencodingkey'  # Encoding key that is only known for auth-server
tokenDict = {'original_id_token': ''}
authDict = {'code':'', 'state':'', 'client_id':''}


class Authlib_authcode:
    def __init__(self):
        pass


    #######################################################################################################      
    """ Authlib Authorization code flow """
    #######################################################################################################

    async def handle_authentication(self, request):
        
        print('New authorization request received!')
        response = request.url
        url = URL(response)
        querys = url.query
        response_type = querys['response_type']
        client_id = querys['client_id']
        authDict['client_id'] = client_id # Save client_id for further use
        scope = querys['scope']
        state = querys['state']
        authDict['state'] = state
        database = self.openDatabase()
        i = False
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
            def string_generator(size=35, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
                return ''.join(random.choice(chars) for _ in range(size))
            auth_code = string_generator()
            authDict['code'] = auth_code # Save auth_code for further use
            authDict['state'] = state # Savve state for further use
            redirect_uri = (urllib.parse.urlencode({"code":auth_code,"state":state}))
            return web.Response(text=redirect_uri)
        if user_is_legit == False:
            return 'Error! User not in database!'

    # Opens database and creates list of all users and their credentials.
    def openDatabase(self):
        try:
            with open('./database/userdatabase.json') as infile:
                data = json.load(infile)
                mylist = []
                for x in data['Users']:
                    mylist.append(x)
                return mylist
        except Exception as e:
            print("Failed to parse json file: ", e)

    async def get_id_token(self, client_identification):
        try:
            await asyncio.sleep(1)
            database = self.openDatabase()
            for x in database:
                if client_identification == x['id']:
                    email = x['email']
                    payload = {
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

    async def valid_auth_code(self, request):
        print('New authorization_code validating request observed from api-server!')
        post = await request.post()
        authorization_code = post.get('authorization_code')
        state = post.get('state')
        i = False
        def validation():
            if authDict['code'] == authorization_code:
                if authDict['state'] == state:
                    i = True
                    return i
            else:
                pass
        if validation() == True:
            print('Authorization was successful!')
            client_identification = authDict['client_id']
            id_token = await self.get_id_token(client_identification)     
            if id_token != '':
                tokenDict['original_id_token'] = id_token
                json_data = {
                    'id_token': id_token,
                    'Access_token': 'qwertyuiop1234'
                }
                print('Sending id_token to api-server..')
                return web.Response(text=json.dumps(json_data))
            else:
                msg = 'Error occured!'
                return web.Response(text=json.dumps(msg))    
        if validation() == False:
            msg = 'Invalid authorization code!'
            return web.Response(text=json.dumps(msg))


