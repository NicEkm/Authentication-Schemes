import sys
import importlib
import asyncio
import json
import aiohttp
import jwt



# These are credentials to use to confirm identity to our own authentication server
# You can choose any user with correct id and secret from database.json - file 

client_id = '3' 
client_secret = 'mysecretflower'

# These are credentials to use to confirm identity to Keycloak authentication server
# You can choose any user with correct username and password from keycloak server.
# You can create new users from Keycloak Admin console.

keycloak_username = 'nikke'
keycloak_password = 'moi123'


async def get_arg():
    try:
        runType = (sys.argv[1].replace('-', ''))
        PLUGIN_NAME = ("test_cli.auth_model." + str(runType))

        # Checks that selected authentication method is correct
        try:
            plugin_module = importlib.import_module(PLUGIN_NAME, ".")
        except Exception as e:
            return print('Error:', e)

        # Checks selected authentication method to select correct client credentials.
        if runType[0:8] == 'keycloak':
            plugin = plugin_module.Authentication_methods(keycloak_username, keycloak_password)
        else:
            plugin = plugin_module.Authentication_methods(client_id, client_secret)
        result = await plugin.authenticate()

        return result
    except IndexError as e:
        # Expects index error which means that argument is empty and
        #  if it is empty, shows list of authentication methods
        return print('Enter authorization type:\n -native_authcode ("Native Authorization code flow")\n -native_implict ("Native Implict flow")\n -authlib_authcode ("Authlib Authorization code flow")\n -authlib_implict ("Authlib Implict flow")\n -keycloak_authcode ("Keycloak Authentication code flow")\n -keycloak_implict ("Keycloak Implict flow")')
    

# Runs async functions depending on authentication type and waits them to be ready.
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = get_arg()
    loop.run_until_complete(result)       
        
    
    

