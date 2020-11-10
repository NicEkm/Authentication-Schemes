import urllib.parse
import time
import json
import asyncio
import aiohttp
import jwt
from aiohttp import web
from yarl import URL





##############################################################################################################
""" Authorization code flow  """
##############################################################################################################
async def native_authcode_handle_authentication(request):
    from auth_server.auth_model.native_authcode import Native_authcode as na
    auth_code = await na().handle_authentication(request)
    return auth_code
async def native_authcode_valid_auth_code(request):
    from auth_server.auth_model.native_authcode import Native_authcode as na
    id_token = await na().valid_auth_code(request)
    return id_token





##############################################################################################################
"""  implict flow   """
##############################################################################################################
async def native_implict_handle_authentication(request):
    from auth_server.auth_model.native_implict import Native_implict as ni
    id_token = await ni().handle_authentication2(request)
    return id_token





##############################################################################################################
""" Authlib Authorization code flow  """
##############################################################################################################
async def authlib_authcode_handle_authentication(request):
    from auth_server.auth_model.authlib_authcode import Authlib_authcode as aa
    auth_code = await aa().handle_authentication(request)
    return auth_code
async def authlib_authcode_valid_auth_code(request):
    from auth_server.auth_model.authlib_authcode import Authlib_authcode as aa
    id_token = await aa().valid_auth_code(request)
    return id_token





##############################################################################################################
""" Authlib Implict flow  """
##############################################################################################################
async def authlib_implict_handle_authentication(request):
    from auth_server.auth_model.authlib_implict import Authlib_implict as ai
    id_token = await ai().handle_authentication(request)
    return id_token





# Defines web application and http routes
app = web.Application()
app.add_routes([
    web.post('/authorization', native_authcode_handle_authentication, name='native_authcode_base'),
    web.post('/authorization2', native_implict_handle_authentication, name='native_implict_base'),
    web.get('/authorization3', authlib_authcode_handle_authentication, name='authlib_authcode_base'),
    web.get('/authorization4', authlib_implict_handle_authentication, name='authlib_implict_base'),
    web.post('/oauth/token', native_authcode_valid_auth_code, name='native_authcode_validation'),
    web.post('/oauth/token2', authlib_authcode_valid_auth_code, name='authlib_authcode_auth_code_request')
])

if __name__ == '__main__':
    web.run_app(app)
