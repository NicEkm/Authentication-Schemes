from aiohttp import web
import aiohttp
import jwt
import json
import asyncio


decoding_token = 'myencodingkey' # Encoding key that is only known for auth-server


# takes / request and does some random stuff
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


#Handle authorization request from test-cli,
#If test-cli credentials (username and password) fits user
#in database, return authorization code
async def handle_authentication(request):
    try:
        print('Validating test-cli authorization_code request')
        await asyncio.sleep(1)
        post = await request.post()
        getSecret = post.get('secret')
        getID = post.get('client_id')
        userInfo={'id':getID, 'secret':getSecret}
        database = openDatabase()

        # with for-loop
        def validation():
            for x in database:
                if x['id']== userInfo['id'] and x['secret'] == userInfo['secret']:
                    at = x['authorization_code']
                    return at             
        at = validation()         
        if at != None:
            print('Sending authorization code to test-cli.. ')
            return web.Response(text=at)
        if at == None:
            msg = "Invalid client_id or secret!"
            print('User not in database, can not find authorization code.')
            return web.Response(text=msg)
    except Exception as e:
        msg = 'Error!'
        return(msg,e)
        
    
    
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
                ID = x['id']
                secret = x['secret']
                params = {ID:secret}
        token = jwt.encode(params,decoding_token)
        return token
    except Exception as e:
        msg = 'Error occured!'
        return (msg,e)





#Takes authorization code from api-server, validates it and
#transfers it to ID_token and Access_token.
async def valid_auth_code(request):
    print('New authorization_code validating request observed from api-server!')
    post = await request.post()
    authorization_code = post.get('authorization_code')
    database = openDatabase()
    try:
        def validating_authorization_code():
            for x in database:
                if x['authorization_code'] == authorization_code:
                    print("found authorization_code pair! ")
                    return True
        if validating_authorization_code() == True:
            id_token = await token(authorization_code)
            id_token = id_token.decode('UTF-8')
            json_data = {'id_token':id_token, 'Access_token':'qwertyuiop1234'}
            print('Sending id_token to api-server.')
            return web.Response(text = json.dumps(json_data))
        else:
            msg = 'Error occured!'
            return web.Response(text=json.dumps(msg))
    except Exception as e:
        return('Error: ',e)
        

#Confirms ID_token is correct and then authenticates user.      
async def valid_user(request):
    print('New id_token validating request observed from api-server!\nValidating id_token..')
    await asyncio.sleep(1)
    post = await request.post()
    id_token = post.get('id_token')
    decoded_id_token = jwt.decode(id_token, decoding_token)
    database = openDatabase()
    user_id = list(decoded_id_token.keys())[0]
    user_pass = list(decoded_id_token.values())[0]
    for x in database:
        if x['id'] == user_id:
            if x['secret'] == user_pass:
                print('Correct id_token!')
                return web.Response(text='True')
    print('Not correct id_token..')
    return web.Response(text='False')
    
    

# Defines web application and http routes
app = web.Application()
app.add_routes([web.get('/', handle, name="main"),
                web.post('/authorization', handle_authentication, name='authorize'),
                web.post('/oauth/token', valid_auth_code, name='oauth'),
                web.post('/uservalidation', valid_user, name='user_validation'),])

if __name__ == '__main__':
    web.run_app(app)
