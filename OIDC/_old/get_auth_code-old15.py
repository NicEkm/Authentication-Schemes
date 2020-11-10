import requests
from yarl import URL
from bs4 import BeautifulSoup as bs



class Get_Auth_Code:
        def __init__(self, url, username, password):
                self.url = url # The redirect url got from api-server
                self.username = username # Username got from test-cli
                self.password = password # Password got from test-cli

        def Auth_code(self):
                url = self.url 
                s = requests.Session() # Creates sesson

                # Gets redirect url and parse its form action http address
                # AKA gets the address to post the log in form
                get_url = s.get(url)
                text = get_url.text
                soup = bs(text, 'html.parser')
                log_in_url = soup.find(id='kc-form-login').get('action')

                cookie = s.cookies

                # Takes cookie names and values that can be added into cookieJar
                FirstCookieName = 'AUTH_SESSION_ID'
                FirstCookieContent = cookie[FirstCookieName]
                SecondCookieName =  'AUTH_SESSION_ID_LEGACY'
                SecondCookieContent = cookie[SecondCookieName]
                ThirdCookieName = 'KC_RESTART'
                ThirdCookieContent = cookie[ThirdCookieName]

                # Configure cookieJar
                cookieJar = requests.cookies.RequestsCookieJar()
                cookieJar.set(FirstCookieName, FirstCookieContent, domain='localhost:8080', path='/auth/realms/myrealm/protocol/openid-connect/auth?client_id=auth-server&response_type=code')
                cookieJar.set(SecondCookieName, SecondCookieContent, domain='localhost:8080', path='/auth/realms/myrealm/protocol/openid-connect/auth?client_id=auth-server&response_type=code')
                cookieJar.set(ThirdCookieName, ThirdCookieContent, domain='localhost:8080', path='/auth/realms/myrealm/protocol/openid-connect/auth?client_id=auth-server&response_type=code')

                # Set post url headers and payload
                headers = {
                        'Content-Type':'application/x-www-form-urlencoded'
                }
                payload = {
                        'username':self.username,
                        'password':self.password,
                        'credentialId':'', # This is empty credential that KeyCloak asks
                }
                response = s.post(log_in_url, headers=headers, data=payload)

                # Get's response url that has authorization code in it
                # Then parse the auth_code from it and send it to api-server
                # And it can be traded to access token
                response_url = response.url
                url2 = URL(response_url)
                querys = url2.query
                auth_code = str(querys['code'])
                return auth_code



