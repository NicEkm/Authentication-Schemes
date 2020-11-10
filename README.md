# inoi-misc-demo-auth
Miscellaneous demo setups of various authentication schemes (Trainee / Niclas Ekman)

## Current version
All files includes OIDC authorization code flow AND implict flow.

## Usage

* !! I recommend to use virtual environment (such as: anaconda, etc.) !!
	- Run api-server and auth-server, then go to cmd and navigate to same directory with all .py files. Use '$ python test-cli.py' to get list of all authentication methods and then add it to end of the command.
	Example cmd command (python test-cli.py -la) where '-la' is for authentication code flow with libraries.


## Authorization code flow

* test-cli.py
	- Makes request to api-server, gets redirected to auth-server. Confirms identity with credentials (username, password) and then receives authorization code. 
	Then sends authorization code to api-server, which can trade it to ID_token (and Access_token).
* api-server.py
	- Takes test-cli request and redirects it to auth-server to verify test-cli identity. Receives authorization_code from test-cli and exchanges it to signatured ID_token (and Access_token) with auth-server. 
	Validates signatured ID_token with correct key.
* auth-server.py
	- Takes test-cli request (which was redirected by api-server), takes test-cli login credentials and checks database for existing user. If user exists auth-server sends authorization code to test-cli. It can later be exchanged
	to signatured ID_token (and Access_token). With ID_token api-server can verify test-cli identity without need to communicate with test-cli.

## Implict flow

* test-cli.py
	 - Makes request to api-server, gets redirected to auth-server. Confirms identity with credentials (username, password) and then receives signatured ID_token.
	Then sends ID_token to api-server
* api-server.py
	- Takes test-cli request and redirects it to auth-server to verify test-cli identity. 
	Receives ID_token right away from test-cli and can validate test-cli identity with correct decoding key that can decode the ID_token
* auth-server.py
	- Takes test-cli request (which was redirected by api-server), takes test-cli login credentials and checks database for existing user. If user exists in auth-server sends signatured ID_token to test-cli.



## Authorization code flow with libraries
I'm working on now same flow as previous ones but now I'm tryig to use libraries that use OIDC specifications. Today I started this
by using OAuthlib in python. I got started but not very far, I had difficulties to understand some parts. Will continue on this on monday.

* test-cli.py
	- Makes request to api-server, gets redirected to auth-server. Confirms identity with credentials (username, password) and then receives authorization code. 
	Then sends authorization code to api-server, which can trade it to ID_token (and Access_token). This happens using aiohttp and authlib -libraries.
* api-server.py
	- Takes test-cli request and redirects it to auth-server to verify test-cli identity. Receives authorization_code from test-cli and exchanges it to signatured ID_token (and Access_token) with auth-server. 
	Validates signatured ID_token with correct key.
* auth-server.py
	- Takes test-cli request (which was redirected by api-server), takes test-cli login credentials and checks database for existing user. 
	If user exists in auth-server sends authorization code to test-cli. 
	Auth-server saves also the state of the test-cli request and uses that among authentication code to validate api-server. 
	It can later be exchanged to signatured ID_token (and Access_token). With ID_token api-server can verify test-cli identity without need to communicate with test-cli.

## Implict flow with libraries

* test-cli.py
	 - Makes request to api-server, gets redirected to auth-server. Confirms identity with credentials (username, password) and then receives signatured ID_token.
	Then sends ID_token to api-server (Uses authlib and aiohttp - libraries)
* api-server.py
	- Takes test-cli request and redirects it to auth-server to verify test-cli identity. 
	Receives ID_token right away from test-cli and can validate test-cli identity with correct decoding key that can decode the ID_token
* auth-server.py
	- Takes test-cli request (which was redirected by api-server), takes test-cli login credentials and checks database for existing user. If user exists in auth-server sends signatured ID_token to test-cli.

## Keycloak Authentication code flow 

* Empty atm

## Keycloak Implict flow

* test-cli.py
	 - Makes request to api-server, gets redirected to keycloak-server. Confirms identity with credentials (username, password) and then receives signatured ID_token.
	Then sends ID_token to api-server (Uses authlib and aiohttp - libraries)
* api-server.py
	- Takes test-cli request and redirects it to keycloak-server to verify test-cli identity. 
	Receives ID_token right away from test-cli and can validate test-cli identity with id_token and python-keycloak library.
* auth-server.py
	- KEYCLOAK SERVER

## Document files:
[HLD-file](OIDC/Docs/HLD.md)

More is coming soon...