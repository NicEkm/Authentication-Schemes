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
authDict = {'state':'','client_id':''}


class Authlib_implict:
    def __init__(self):
        pass


    ##############################################################################################################
    ''' Authlib Implict flow '''
    #############################################################################################################


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
        authDict['state'] = state # Save state for further use
        database = self.openDatabase()
        i = False
        def validation():
            for x in database:
                if x['id'] == client_id:
                    if authDict['state'] == state:
                        i = True
                        return i
                    else:
                        pass
        user_is_legit = validation()
        if user_is_legit == True:
            print('User authenticated successfully!')
            await asyncio.sleep(1)
            client_identification = authDict['client_id']
            id_token = await self.get_id_token2(client_identification)
            tokenDict['original_id_token'] = id_token
            payload = (urllib.parse.urlencode({"id_token":id_token}))
            print('Sending id_token to test-cli.. ')
            return web.Response(text=payload)
        if user_is_legit == False:
            print('User authentication failed!')
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


    async def get_id_token2(self, client_identification):
        try:
            await asyncio.sleep(1)
            database = self.openDatabase()
            for x in database:
                if client_identification == x['id']:
                    email = x['email']
                    payload = {
                        'email': email,
                        'state':authDict['state'],
                        'exp': time.time() + 120,
                        'scope': 'openid'
                    }
                    id_token = jwt.encode(payload, decoding_key,
                                        algorithm='HS256').decode('UTF-8')
                    return id_token
        except Exception as e:
            msg = 'Error occured!'
            return (msg, e)





