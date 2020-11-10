 import aiohttp
from aiohttp import web
import asyncio
import json
import socket


# Listens port 8080 which is AUTH-server, and takes answer which corresponds
# Wheter client has rights to the API or not

# Still not working, WIP

async def get_answer_from_auth_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8080))
    s.listen(5)
    while True:
        clientsocket, address = s.accept()
        msg = s.recv(1024)
        s.close()
        answer = msg.decode("utf-8")
        return answer
        
        


# Takes request from client, and then runs "get_answer_from_auth_server()"
# Which is supposed to return web.Response with correct json data
# Depending if client is authenticated or not

async def handle(request):
    answer = asyncio.run(get_answer_from_auth_server())
    print(answer)
    if answer == "Authentication successful":
        response_object = {"status": "success"}
        return web.Response(text=json.dumps(response_object), status=200)
    if answer == "Authentication failed":
        response_object = {"status": "failed!"}
        return web.Response(text=json.dumps(response_object), status=500)
    


app = web.Application()
app.router.add_get('/', handle)


web.run_app(app, port=9090)
























    


