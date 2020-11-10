import aiohttp
from aiohttp import web
import asyncio
import json
import socket



# Open userdatabase.json file, where is all clients ip addressess listed
# and makes tokenList from them

def get_tokenList():
    try:
        with open('./userdatabase.json') as infile:
            data = json.load(infile)
            tokenList = []
            i=0
            for ip in data['Users']:
                t = data['Users'][i]['ip']
                tokenList.append(t)
                i += 1
            return tokenList
    except Exception as e:
        return "Failed to parse json file"

# Takes tokenList and compares it to ipList which is clients IP address
# If there is corresponding IP in the database.json it counts client
# as authenticated

def get_ip():      
        tokenList = get_tokenList()
        ipList =[]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 9090))
        s.listen(5)
        while True:
                clientsocket, address = s.accept()
                print(f"Connection from {address} has been established")
                Addr = {address[0]}
                newAddr = list(Addr)
                print(newAddr[0])
                print(tokenList[0])
                if newAddr[0] in tokenList:
                    print('Client has rights to this API!')
                    clientsocket.send(bytes(send_success_info_to_api(), "utf-8"))
                    clientsocket.send(bytes(send_success_info_to_api(), "utf-8"))
                
                if newAddr[0] not in tokenList:
                    print('Client has no rights to this API!')
                    clientsocket.send(bytes(send_failed_info_to_api(), "utf-8"))
                    clientsocket.send(bytes(send_success_info_to_api(), "utf-8"))
                    
                
                    
# Success message
                
def send_success_info_to_api():
    answer = "Authentication successful"
    return answer
            
# Failed message

def send_failed_info_to_api():
    answer = "Authentication failed"
    return answer
   

async def handle(request):
    asyncio.run(get_ip())



app = web.Application()
app.router.add_get('/', handle)
web.run_app(app, port=8080)

    



