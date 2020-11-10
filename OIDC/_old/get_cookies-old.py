

import requests
from bs4 import BeautifulSoup as bs



url = 'http://localhost:8080/auth/realms/myrealm/protocol/openid-connect/auth?client_id=auth-server&response_type=code'
s = requests.session()

get_url = s.get(url)
text = get_url.text
soup = bs(text, 'html.parser')
log_in_url = soup.find(id='kc-form-login').get('action')

cookie = s.cookies 
tr = cookie['Cookie']
print(tr)
headers = {
        'Content-Type':'application/x-www-form-urlencoded'
}
cookies = {
        'Cookie':str(cookie)
}
print(cookie)
payload = {
        'username':'nikke',
        'password':'moi123',
        'credentialId':'',
    }
response = s.post(url, headers=headers, cookies=cookies, data=payload)
print(response.status_code)



