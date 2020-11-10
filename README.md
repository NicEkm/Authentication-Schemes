# Authentication methods
Miscellaneous setups of various authentication schemes

## Current version
All methods include 2 flows (Authorization code flow and Implict flow) AND 3 different methods of performing user authentication. There is Native-method, Authlib-method and Keycloak-method. Every single method have their own test-cli.py, api-server.py and auth-server.py files. I will link their full source path on down below. There is also such files under OIDC folder and they are used to run this program. 

## Usage / setup

* I recommend to use virtual environment (such as: conda, etc.)

* By default there is my own credentials on all parts where credentials are needed. You can change them from [test-cli.py](OIDC/test-cli.py)-file.

* Usage
	- Run [api-server.py](OIDC/api-server.py) and [auth-server.py](OIDC/auth-server.py), then go to cmd/terminal and navigate to same directory with previous .py files. Use '$ python test-cli.py ' -command to get list of all authentication methods and then add it to end of the command.
	Example command would look like: ($ python test-cli.py -native_authcode) where '-native_authcode' is for native authorization code flow. If you are using mac or linux 
	you might need to use 'python3' command instead of 'python'. So the example command would look like: ($ python3 test-cli.py -native_authcode) where '-native_authcode' is for native authorization code flow.
* Keycloak server setup
	- When you use Keycloak authentication server instead of our own auth-server, you need to create keycloak server. Easiest way to create it is using docker, and full
	server installation instructions are under Keycloak/setup-folder. Keep in mind that both keycloak server and auth-server are running in same port (8080) by default,
	so you can't run them simultaniously without changing other ones port. You can read the server installation instructions from [HERE](OIDC/Docs/KEYCLOAK_SERVER_INSTALLATION.txt).

	- If you are using KEYCLOAK-server instead of our own auth-server you need to install the server and then create your own user there from the admin console. Then you need to change correct KEYCLOAK log-in -credentials from this [test-cli.py](OIDC/test-cli.py)-file.

* Database
	- There is fictional database with existing users under database folder. Database is .json -file and you can create your own users there. To be able to authenticate by using your own user, you need to create your own user to the database and then change "log in"- credentials to your own credentials from this [test-cli.py](OIDC/test-cli.py)-file.


## Native Authorization code flow

Here is Native authorization code flow and implict flow. This means that we are not using any 3rd party libraries to fulfill OIDC specifications but we are doing every single step ourself. 

* [test-cli.py](OIDC/test_cli/auth_model/native_authcode.py)
	- Makes request to api-server, gets redirected to auth-server. Confirms identity with credentials (username, password) and then receives authorization code. 
	Then sends authorization code to api-server, which can trade it to ID_token (and Access_token).
* [api-server.py](OIDC/api_server/auth_model/native_authcode.py)
	- Takes test-cli request and redirects it to auth-server to verify test-cli identity. Receives authorization_code from test-cli and exchanges it to signatured ID_token (and Access_token) with auth-server. 
	Validates signatured ID_token with correct key.
* [auth-server.py](OIDC/auth_server/auth_model/native_authcode.py)
	- Takes test-cli request (which was redirected by api-server), takes test-cli login credentials and checks database for existing user. If user exists auth-server sends authorization code to test-cli. It can later be exchanged
	to signatured ID_token (and Access_token). With ID_token api-server can verify test-cli identity without need to communicate with test-cli.

## Native Implict flow

* [test-cli.py](OIDC/test_cli/auth_model/native_implict.py)
	- Makes request to api-server, gets redirected to auth-server. Confirms identity with credentials (username, password) and then receives signatured ID_token.
	Then sends ID_token to api-server
* [api-server.py](OIDC/api_server/auth_model/native_implict.py)
	- Takes test-cli request and redirects it to auth-server to verify test-cli identity. 
	Receives ID_token right away from test-cli and can validate test-cli identity with correct decoding key that can decode the ID_token
* [auth-server.py](OIDC/auth_server/auth_model/native_implict.py)
	- Takes test-cli request (which was redirected by api-server), takes test-cli login credentials and checks database for existing user. If user exists in auth-server sends signatured ID_token to test-cli.



## Authlib Authorization code flow

Same flows, but now we are using some python libraries.

* [test-cli.py](OIDC/test_cli/auth_model/authlib_authcode.py)
	- Makes request to api-server, gets redirected to auth-server. Confirms identity with credentials (username, password) and then receives authorization code. 
	Then sends authorization code to api-server, which can trade it to ID_token (and Access_token). This happens using aiohttp and authlib -libraries.
* [api-server.py](OIDC/api_server/auth_model/authlib_authcode.py)
	- Takes test-cli request and redirects it to auth-server to verify test-cli identity. Receives authorization_code from test-cli and exchanges it to signatured ID_token (and Access_token) with auth-server. 
	Validates signatured ID_token with correct key.
* [auth-server.py](OIDC/auth_server/auth_model/authlib_authcode.py)
	- Takes test-cli request (which was redirected by api-server), takes test-cli login credentials and checks database for existing user. 
	If user exists in auth-server sends authorization code to test-cli. 
	Auth-server saves also the state of the test-cli request and uses that among authorization code to validate api-server. 
	It can later be exchanged to signatured ID_token (and Access_token). With ID_token api-server can verify test-cli identity without need to communicate with test-cli.

## Authlib Implict flow

* [test-cli.py](OIDC/test_cli/auth_model/authlib_implict.py)
	- Makes request to api-server, gets redirected to auth-server. Confirms identity with credentials (username, password) and then receives signatured ID_token.
	Then sends ID_token to api-server (Uses authlib and aiohttp - libraries)
* [api-server.py](OIDC/api_server/auth_model/authlib_implict.py)
	- Takes test-cli request and redirects it to auth-server to verify test-cli identity. 
	Receives ID_token right away from test-cli and can validate test-cli identity with correct decoding key that can decode the ID_token
* [auth-server.py](OIDC/auth_server/auth_model/authlib_implict.py)
	- Takes test-cli request (which was redirected by api-server), takes test-cli login credentials and checks database for existing user. If user exists in auth-server sends signatured ID_token to test-cli.

## Keycloak Authorization code flow 

Same flows, but now instead of our own auth-server we are using Keycloak-server to authenticate user.

* [test-cli.py](OIDC/test_cli/auth_model/keycloak_authcode.py)
	- Makes request to api-server, gets redirected to keycloak-server. Confirms identity with credentials (username, password) and then receives authorization code.
	Then sends auth_code to api-server.
* [api-server.py](OIDC/api_server/auth_model/keycloak_authcode.py)
	- Takes test-cli request and redirects it to keycloak-server to verify test-cli identity. 
	Receives authorization code from test-cli and then sends it to keycloak-server in order to gain id_token from it. Then validates id_token using python-keycloak library.
* auth-server.py
	- KEYCLOAK SERVER

## Keycloak Implict flow

* [test-cli.py](OIDC/test_cli/auth_model/keycloak_implict.py)
	- Makes request to api-server, gets redirected to keycloak-server. Confirms identity with credentials (username, password) and then receives signatured ID_token.
	Then sends ID_token to api-server.
* [api-server.py](OIDC/api_server/auth_model/keycloak_implict.py)
	- Takes test-cli request and redirects it to keycloak-server to verify test-cli identity. 
	Receives ID_token right away from test-cli and can validate test-cli identity with id_token and python-keycloak library.
* auth-server.py
	- KEYCLOAK SERVER

## Selfmade modules

This code uses Python own libraries such as requests, etc. It also use 3rd party libraries for example jwt or python-keycloak and some self made modules. I have listed my self made modules down below:

* Token_validation.py
	- This is module to validate normal tokens that are signatured by our own auth-server
	- Full path: /others/token_validation.py [token-validation](OIDC/others/token_validation.py)
* Keycloak_token_validation.py
	- This is module to validate tokens that are signatured by keycloak authentication server
	- Full path: /others/keycloak_token_validation.py [keycloak-token-validation](OIDC/others/keycloak_token_validation.py)
* Get_auth_code.py
	- This is module to gain authorization code from keycloak server
	- Full path: /keycloak_server/scripts/get_auth_code.py [get-auth-code](OIDC/others/get_auth_code.py)


	
## Document files:

* [HLD-file](OIDC/Docs/HLD.md)
* [KEYCLOAK-SERVER-INSTALLATION](OIDC/Docs/KEYCLOAK_SERVER_INSTALLATION.txt)
* [RESOURCES](OIDC/Docs/resources.txt)
	- Here is listed some links that I found useful while creating this. There is links and sources considering OIDC and how to create applications around it.


## Authors
* Niclas Ekman


More is coming soon...