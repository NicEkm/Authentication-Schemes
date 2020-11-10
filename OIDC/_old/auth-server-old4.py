from aiohttp import web
import aiohttp
import jwt
import json
import asyncio


mysecret = 'myencodingkey' # Encoding key that is only known for auth-server


# takes / request and does some random stuff
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


# Takes /get request, adds parameters to jwt token and generates jwt token
# for client. Response is json-data that contains jwt token for client.
async def check_authentication(request):
    try:
        print('validating api-server request')
        await asyncio.sleep(1)
        post = await request.post()
        getSecret = post.get('secret')
        getID = post.get('client_id')
        userInfo={'id':getID, 'secret':getSecret}
        print(userInfo)
        database = openDatabase()

        # with for-loop
        def validation1():
            for x in database:
                if x['id']== userInfo['id'] and x['secret'] == userInfo['secret']:
                    at = x['authorization_code']
                    print(at)
                    return at
                
        at = validation1()         
        if at != None:
            print('Sending authorization code to test-cli: ', at)
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
        print('New token request observed!')
        await asyncio.sleep(1)
        # Defines token parameters and client secret 'mysecretflower'
        database = openDatabase()
        for x in database:
            if authorization_code == x['authorization_code']:
                ID = x['id']
                secret = x['secret']
                params = {ID:secret}
        token = jwt.encode(params, mysecret)
        return token
    except Exception as e:
        msg = 'Error occured!'
        return (msg,e)


# This is extra now (not used yet on anywhere)
async def handle_token(request):
    print('validating test-cli request')
    await asyncio.sleep(1)
    post = await request.post()
    getToken = post.get('token')
    getID = post.get('id')
    encodedToken = getToken.encode('UTF-8')
    actualData = jwt.decode(encodedToken, mysecret)

    if actualData == params:
        msg = 'Correct token!'
        print(msg)
        newParams = {'fakeusername':'fakepassword'}
        newToken = jwt.encode(newParams, mysecret)
        decodedToken = newToken.decode('UTF-8')
        print(decodedToken)
        
        
    if actualData != params:
        msg = 'Invalid token, process timed out!'
        print(msg)


#Takes authorization code from api-server, validates it and
#transfers it to ID_token and Access_token.
async def valid_auth_code(request):
    post = await request.post()
    authorization_code = post.get('authorization_code')
    database = openDatabase()
    print(authorization_code)
    try:
        def validating_authorization_code():
            for x in database:
                if x['authorization_code'] == authorization_code:
                    print("found pair!: ",x['authorization_code'], authorization_code)
                    return True
        if validating_authorization_code() == True:
            ID_token = await token(authorization_code)
            ID_token = ID_token.decode('UTF-8')
            print('ID_token is :', ID_token)
            decoded_token = jwt.decode(ID_token, mysecret)
            print(decoded_token)
            json_data = {'ID_token':ID_token, 'Access_token':'qwertyuiop1234'}
            return web.Response(text = json.dumps(json_data))
        else:
            msg = 'Error occured!'
            return web.Response(text=json.dumps(msg))
    except Exception as e:
        return('Error: ',e)
        
        
            

    
    

# Defines web application and http routes
app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/get', token, name='get_token'),
                web.post('/checkauthentication', check_authentication),
                web.post('/oauth/token', valid_auth_code),
                web.post('/getinfo', handle_token)])

if __name__ == '__main__':
    web.run_app(app)
