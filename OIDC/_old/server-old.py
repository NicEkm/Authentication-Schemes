from aiohttp import web
import requests
import json

# READ REQUIREMENTS.TXT


uniqueID = 1 # Authentication "key", if id is not in database (tokens.json),
             # user is not authenticated to see the message.


def create_api(request):
    def get_message(uniqueID):
        uniqueID = uniqueID - 1 # -1 because index starts with 0
        url = 'http://localhost:8080/?'
        path = '/tokens.json'

        # Try to open database and checks if there is uniqueID
        try:
            with open('./tokens.json') as infile:
                data = json.load(infile)
                DataID = data['tokens'][uniqueID]['id']
                dataToken = data['tokens'][uniqueID]['token']

        # If there is uniqueID, let's request to pass.
                         
            if DataID != "":
                response_object = { 'status': 'success', 'message': 'You can only see this if you are authenticated!'}
                print("You have access to this information!")
                return response_object
            
        # If there is no ID, won't let request to pass.
            else:
                response_object = { 'status': 'failed!', 'message': 'You are not authenticated!', 'Solution': 'Propably typo from host, client on your index position is created but not granted with ID'}
                print("You have no access to this information!")
                return response_object
            
        # In case of other unexpected error, returns Fail status and errormessage!
        except Exception as e:
            error_message = str(e)
            response_object = { 'status': 'failed!', 'message': 'You are not authenticated!','Solution': 'Ask host to add you to the database.'}
            print("Error handeling request file, error: ",e)
            return response_object
            
    
    return web.Response(text=json.dumps(get_message(uniqueID)), status=200)
            


app = web.Application()
app.router.add_get('/', create_api)

web.run_app(app)
