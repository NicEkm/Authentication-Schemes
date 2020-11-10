# OIDC Demo
My aim is to create authentication software using OIDC specifications (OpenID Connect, OAuth2.0)
using 3 different methods and 2 different flows (Authorization code flow and Implict flow)

## Workflow
There are three main files in this authentication process. They work slightly diffrently depending on authentication flow. I have explained how files work on both flows down below.

* Authorization code flow
    * test-cli.py
        - Works as end-user in our web app. Test-cli tries to access to api-server that includes some really awesome json data! Api-server is secured so   everybody can't access it.
        Api-server redirects end-user request to auth-server that authenticates end-user for api-server. 
        Auth-server first gives authorization code which is transferred to ID_token and Access_token by api-server. After claiming authorization code with 
        login credentials end-user sends authorization code to api-server and then api-server transfers it to ID_token and Access_token with auth-server (assuming authorization code is correct). After api-server receives ID_token, it
        can be used to authenticate user for future api visits! If ID-token is correct user have access to API.
    * auth-server.py
        - Works as authentication server just like Google-auth and Facebook-auth. It takes end-user login credentials and checks database if user with those credentials already exists. If user is found, it generates authorization code,
        that can be transferred to ID_token and Access_token. With correct ID_token api-server (or someone with that token) can access end-users information and in that way authenticate end-user without end-users physical contact.
    * api-server.py
        - Works as client such as Stack overflow or Blizzard. It takes end-user request and redirects it to auth-server. Authentication is processed in auth-server so there is no much authentication or security work for api-server. 
        Api-server trades authorization code to ID_token and Access_token and with them verifies end-users identity. If end-user is legit and has rights to access the API it let's end-user to the API.

* Implict flow
    * test-cli.py
        - Works as end-user in our web app. Test-cli tries to access to api-server that includes some really awesome json data! Api-server is secured so   everybody can't access it.
        Api-server redirects end-user request to auth-server that authenticates end-user for api-server. 
        Auth-server sends signatured ID_token to test-cli, if credentials are correct. Then test-cli sends ID_token straight to the api-server that can validate it. If ID-token is correct user have access to API.
    * auth-server.py
        - Works as authentication server just like Google-auth and Facebook-auth. It takes end-user login credentials and checks database if user with those credentials already exists. If user is found, it creates signatured ID_token and then sends it to test-cli.
    * api-server.py
        - Works as client such as Stack overflow or Blizzard. It takes end-user request and redirects it to auth-server. Authentication is processed in auth-server so there is no much authentication or security work for api-server. 
        Api-server gets ID_token from test-cli and with ID_token it can verify end-users identity. If end-user is legit and has rights to access the API it let's end-user to the API.
