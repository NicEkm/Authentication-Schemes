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

class Native_implict:
    def __init__(self):
        pass


    ##############################################################################################################
    """  Native Implict flow   """
    ##############################################################################################################

    # Takes test-cli authorization request and identifies user, if user
    # is in database generates id_token for it.
    async def handle_authentication2(self, request):
        try:
            print('Validating test-cli identity..')
            await asyncio.sleep(1)
            post = await request.post()
            getSecret = post.get('secret')
            getID = post.get('client_id')
            userInfo = {'id': getID, 'secret': getSecret}
            database = self.openDatabase()
            i = False
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
                    database = self.openDatabase()
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





