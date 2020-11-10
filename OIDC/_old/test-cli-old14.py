from authenticationmethods import Authentication_methods
import aiohttp
import asyncio
import jwt
import json
import sys




userdata = Authentication_methods('3', 'mysecretflower') # This is used when we use our own authentication server.
userdata_for_keycloak = Authentication_methods('nikke', 'moi123') # This is used when we use Keycloak authentication server.


# Runs async functions depending on authentication type and waits them to be ready.
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if len(sys.argv) == 2: 
        runType = sys.argv[1] # Takes cli (command line interface) argument and defines it.
        if runType == '-a': # For authentication code flow
            loop.run_until_complete(userdata.authentication_code_flow())
            loop.close()
        if runType == '-i': # For implict flow
            loop.run_until_complete(userdata.implict_flow())
            loop.close()
        if runType == '-la': # For authentication code flow using libraries
            loop.run_until_complete(userdata.authentication_code_flow_with_libraries())
            loop.close()
        if runType == '-li': # For implict flow using libraries
            loop.run_until_complete(userdata.implict_flow_with_libraries())
            loop.close()
        if runType == '-lak': # For authentication code flow with keycloak
            loop.run_until_complete(userdata_for_keycloak.authentication_code_flow_with_keycloak())
            loop.close()
        if runType == '-lik': # For implict flow with keycloak
            loop.run_until_complete(userdata_for_keycloak.implict_flow_with_keycloak())
            loop.close()
        if runType != '':
            if runType != '-i':
                if runType != '-a':
                    if runType != '-la':
                        if runType != '-li':
                            if runType != '-lak':
                                if runType != '-lik':
                                    print('Invalid authorization type..')
    if len(sys.argv) != 2: # If there is no argument in python call, asks argument from user
        print('Enter authorization type:\n -a ("Authorization code flow")\n -i ("Implict flow")\n -la ("Authorization code flow with libraries")\n -li ("Implict flow with libraries")\n -lak ("Authentication code flow with keycloak")\n -lik ("Implict flow with keycloak")')

    

