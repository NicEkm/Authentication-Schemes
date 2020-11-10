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

class Native_authcode:
    def __init__(self):
        pass


    ##########################################################################################################
    """ Native Authorization code flow """
    #############################################################################################################

    #Handle authorization request from test-cli,
    #If test-cli credentials (username and password) fits user
    #in database, return authorization code

    async def handle_authentication(self, request):
        try:
            print('Validating test-cli authorization_code request..')
            await asyncio.sleep(1)
            post = await request.post()
            getSecret = post.get('secret')
            getID = post.get('client_id')
            userInfo = {'id': getID, 'secret': getSecret}
            database = self.openDatabase()
            def validation():
                for x in database:
                    if x['id'] == userInfo['id'] and x['secret'] == userInfo['secret']:
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

    #Generates jwt token for current end-user.
    async def token(self, authorization_code):
        try:
            await asyncio.sleep(1)
            database = self.openDatabase()
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


    # Takes authorization code from api-server, validates it and
    # transfers it to ID_token and Access_token.
    async def valid_auth_code(self, request):
        print(
            'New authorization_code validating request observed from api-server!')
        post = await request.post()
        authorization_code = post.get('authorization_code')
        database = self.openDatabase()
        try:
            def validating_authorization_code():
                for x in database:
                    if x['authorization_code'] == authorization_code:
                        print("Found authorization_code pair!")
                        return True
            if validating_authorization_code() == True:
                id_token = await self.token(authorization_code)
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


