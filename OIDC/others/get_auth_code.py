
""" 
THIS IS CODE FOR GAINING AUTHORIZATION CODE FROM KEYCLOAK SERVER 
"""


import requests
from yarl import URL
from bs4 import BeautifulSoup as bs



class Get_Auth_Code:
        def __init__(self, url, username, password):
                self.url = url # The redirect url got from api-server
                self.username = username # Username got from test-cli
                self.password = password # Password got from test-cli

        def Auth_code(self):
                base_url = self.url 
                s = requests.Session() # Creates sesson

                # Gets redirect url and parse its form action http address
                # AKA gets the address that post request is sent to
                response = s.get(base_url)
                text = response.text
                soup = bs(text, 'html.parser')
                log_in_url = soup.find(id='kc-form-login').get('action')

                # Set post url headers and payload
                headers = {
                        'Content-Type':'application/x-www-form-urlencoded'
                }
                payload = {
                        'username':self.username,
                        'password':self.password,
                }
                post_response = s.post(log_in_url, headers=headers, data=payload)

                # Get's response url that has authorization code in it
                # Then parse the auth_code from it and send it to api-server
                # And it can be traded to access token
                response_content = post_response.url
                revalue_response_content = URL(response_content) # Revalue response to YARL - URL
                querys = revalue_response_content.query # Gets all queries from the revalue_response_content
                auth_code = str(querys['code']) # Gets auth code from the revalue_response_content
                return auth_code



