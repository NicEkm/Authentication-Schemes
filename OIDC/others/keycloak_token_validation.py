
""" 
THIS CODE IS TO VALIDATE TOKEN GAINED FROM KEYCLOAK AUTHENTICATION SERVER 
"""


from keycloak import KeycloakOpenID

#########################################################
""" Keycloak token validation """
#########################################################

class Token_validation:
    def __init__(self, token):
        self.token = token


    async def validate_access_token(self):
        keycloak_openid = KeycloakOpenID(server_url='http://localhost:8080/auth/',
                        client_id="auth-server",
                        realm_name="myrealm")
        access_token = self.token
        def decode_access_token():
            try:
                decode_token = bool(keycloak_openid.userinfo(access_token))
            except Exception:
                text = 'Error'
                return text
            if decode_token == True:
                return True
            else:
                return False
        if decode_access_token() == True:
            print('Id token validation successful!')
            text = {
                    'message':'success',
                    'company_info':'niclasOYJ',
                    'secret_animal':'tiger',
                    }
            print('User now have access to the api.')
            return text
        # If id_token is not valid, returns error message.
        if decode_access_token() == False:
            print('Id token validation failed!')
            text = {
                    'message':'Denied, user have no rights to this api!'
                    }
            print('User do not have access to the api!')
            return text
        if decode_access_token() == 'Error':
            print('Id token validation failed!')
            text = 'Error while handeling token. It is either invalid or expired, please try again..'
            return text


