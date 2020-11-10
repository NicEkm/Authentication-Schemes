import aiohttp
import asyncio
import requests
import socket


#Makes request to port 9090 which is API-Server

def client_request():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9090))
    msg = s.recv(1024)
    print(msg.decode("utf-8"))

client_request()



