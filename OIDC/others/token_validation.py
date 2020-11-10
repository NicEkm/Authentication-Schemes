
""" 
THIS CODE IS TO VALIDATE TOKEN GAINED FROM OUR OWN AUTHENTICATION SERVER 
"""


import asyncio
import jwt


#########################################################
""" Token validation """
#########################################################

class Token_validation:
    def __init__(self, token, decoding_key):
        self.token = token
        self.decoding_key = decoding_key

# Function that validates token if it already exists in tokenDict.
    async def validate_token(self):
        print('Validating id_token...')
        await asyncio.sleep(1)
        id_token = self.token
        decoding_key = self.decoding_key
        # Decodes id_token to make sure it's valid and from correct provider
        def decode_id_token():
            try:
                decoded_token = bool(jwt.decode(id_token, decoding_key, algorithms=['HS256']))
            except Exception:
                text = 'Error'
                return text
            if decoded_token == True:
                return True
            else:
                return False
        # If id_token is valid, gives user access to json data
        if decode_id_token() == True:
            print('Id token validation successful')
            text = {
                    'message':'success',
                    'company_info':'niclasOYJ',
                    'secret_animal':'tiger',
                    }
            print('User now have access to the api.')
            return text
        # If id_token is not valid, returns error message.
        if decode_id_token() == False:
            text = {
                    'message':'Denied, user have no rights to this api!'
                    }
            print('User do not have access to the api!')
            return text
        if decode_id_token() == 'Error':
            print('Id token validation failed!')
            text = 'Error while handeling token. It is either invalid or expired, please try again..'
            return text

