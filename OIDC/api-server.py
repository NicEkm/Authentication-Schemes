import urllib.parse
import asyncio
import json
import aiohttp
import jwt
from aiohttp import web
from yarl import URL





###########################################################################################################      
""" Authorization code flow """
#######################################################################################################
async def native_authcode_handle(request):
    from api_server.auth_model.native_authcode import Native_authcode as na
    base_request = await na().handle()
    return base_request
async def native_auth_authorization(request):
    from api_server.auth_model.native_authcode import Native_authcode as na
    authorization = await na().authorization(request)
    return authorization





#######################################################################################################                            
""" Implict flow """
#######################################################################################################
async def native_implict_handle(request):
    from api_server.auth_model.native_implict import Native_implict as ni
    base_request = await ni().handle()
    return base_request
async def native_implict_receive_id_token(request):
    from api_server.auth_model.native_implict import Native_implict as ni
    id_token = await ni().receive_id_token(request)
    return id_token





#############################################################################################################
''' Authlib Authentication code flow '''
#######################################################################################################
async def authlib_authcode_handle(request):
    from api_server.auth_model.authlib_authcode import Authlib_authcode as aa
    base_request = await aa().handle()
    return base_request
async def authlib_authcode_authorization(request):
    from api_server.auth_model.authlib_authcode import Authlib_authcode as aa
    authorization = await aa().authorization(request)
    return authorization





##############################################################################################################
''' Authlib Implict flow '''
##############################################################################################################
async def authlib_implict_handle(request):
    from api_server.auth_model.authlib_implict import Authlib_implict as ai
    base_request = await ai().handle()
    return base_request
async def authlib_implict_receive_id_token(request):
    from api_server.auth_model.authlib_implict import Authlib_implict as ai
    id_token = await ai().receive_id_token(request)
    return id_token





##############################################################################################################
""" Keycloak Authentication code flow """
##############################################################################################################
async def keycloak_authcode_handle(request):
    from api_server.auth_model.keycloak_authcode import Keycloak_authcode as ka
    base_request = await ka().handle()
    return base_request
async def keycloak_authcode_authorization(request):
    from api_server.auth_model.keycloak_authcode import Keycloak_authcode as ka
    id_token = await ka().authorization(request)
    return id_token





#############################################################################################################
''' Keycloak Implict flow '''
##############################################################################################################
async def keycloak_implict_handle(request):
    from api_server.auth_model.keycloak_implict import Keycloak_implict as ki
    base_request = await ki().handle()
    return base_request
async def keycloak_implict_get_access_token(request):
    from api_server.auth_model.keycloak_implict import Keycloak_implict as ki
    id_token = await ki().get_access_token(request)
    return id_token





##############################################################################################################






# Defines web application and http routes
app = web.Application()
app.add_routes([web.get('/', native_authcode_handle, name='native_authcode_base'),
                web.get('/api', native_implict_handle, name='native_implict_base'),
                web.get('/api_data', authlib_authcode_handle, name='authlib_authcode_base'),
                web.get('/api_data/implict', authlib_implict_handle, name='authlib_implict_base'),
                web.get('/api_data/auth_code/keycloak', keycloak_authcode_handle, name='keycloak_authcode_base'),
                web.get('/api_data/keycloak', keycloak_implict_handle, name='keycloak_implict_base'),
                web.get('/authorize', authlib_authcode_authorization, name='authlib_authcode_authroization'),
                web.get('/authorize2', authlib_implict_receive_id_token, name='authlib_implict_token'),
                web.post('/api_data/authorization_code', keycloak_authcode_authorization, name='keycloak_authcode_authorization'),
                web.post('/api_data/access_token', keycloak_implict_get_access_token, name='keycloak_implict_token'),
                web.post('/oauth/token', native_auth_authorization, name='native_auth_authorization'),
                web.post('/openid/connect/id_token', native_implict_receive_id_token, name='native_implict_token'),
                ])

if __name__ == '__main__':
    web.run_app(app, port=9090) # Opens web app to port 9090
