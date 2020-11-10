from aiohttp import web
import aiohttp
import jwt
import json
import asyncio
import multidict

params = {'red':'flower'}
mysecret = 'mysecretflower'


# takes / request and does some random stuff
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)



# Takes /get request, adds parameters to jwt token and generates jwt token
# for client. Response is json-data that contains jwt token for client.
async def check_authentication(request):
    print('validating api-server request')
    await asyncio.sleep(1)
    post = await request.post()
    getSecret = post.get('secret')
    getID = post.get('client_id')
    userInfo={'id':getID, 'secret':getSecret}
    print(userInfo)
    database = openDatabase()
    
    # checks if user id and secret matches users in database
    def validation():
        i = (len(database)-1)
        at = ''
        while i>=0:
            if database[i]['id'] == userInfo['id']:
                if database[i]['secret'] == userInfo['secret']:
                    at = database[i]['a_code']
                    return at
            if database[i]['id'] != userInfo['id']:
                if database[i]['secret'] != userInfo['secret']:
                    i-=1
            if i == -1:
                at = ''
                return at

    # if validation is successful takes user authentication code and sends it to api-server        
    at = validation()         
    if at != '':
        print('send authentication code', at)
    if at == '':
        print('dont send authentication code')
        
    
    

        
# Opens database and takes its users into a list that is easy to compare with
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



async def token(request):
    print('New token request observed!')
    await asyncio.sleep(1)
    # Defines token parameters and client secret 'mysecretflower'
    token = jwt.encode(params, mysecret)
    tokenStr = token.decode('UTF-8')
    myJson = {'token':tokenStr}
    print('Token sent successful!')
    return web.Response(text=json.dumps(myJson))



async def handle_token(request):
    print('validating api-server request')
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



# Defines web application and http routes
app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/get', token),
                web.post('/checkauthentication', check_authentication),
                web.post('/getinfo', handle_token)])

if __name__ == '__main__':
    web.run_app(app)
