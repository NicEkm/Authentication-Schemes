import random
import string
import json




# CREATES NEW 10 CHARACTERS TOKEN
def create_token():
    token = []
    randomlist = []
    i = 5
    y = 5
    while i>0 and y>0:
        i-=1
        y-=1
        integer = random.randrange(10)
        letters = string.ascii_lowercase
        word = random.choice(letters)
        randomlist.append(integer)
        randomlist.append(word)
    token.append(randomlist)
    Stoken = ",".join(map(str, token))
    return Stoken

# ADDS NEW TOKEN TO THE CLIENTS AND TOKENS DATABASE
def add_to_json(uniqueID):
    New_token = create_token()
    uniqueID = uniqueID - 1
    try:
        with open('..json/tokens.json') as infile:
            data = json.load(infile)
            dataID = data['tokens'][uniqueID]['id']
            dataToken = data['tokens'][uniqueID]['token']
    
            if len(data['tokens'][uniqueID]['token']) == 0:      
                for elem in data.items():
                    data['tokens'][uniqueID]['token'] = data['tokens'][uniqueID]['token'].replace('',New_token)

                with open('./tokens.json', 'w') as outfile:
                    print("Token created, to the tokens database!")
                    json.dump(data, outfile)

##############################################################################

        with open('.././database.json') as infile:
            NewData = json.load(infile)
            dataID2 = NewData['Clients'][uniqueID]['id']
            dataToken2 = NewData['Clients'][uniqueID]['token']

        if len(NewData['Clients'][uniqueID]['token']) == 0:      
            for elem in NewData.items():
                NewData['Clients'][uniqueID]['token'] = NewData['Clients'][uniqueID]['token'].replace('',New_token)
            
            with open('./database.json', 'w') as outfile:
                print("Token created, to the clients database!")
                json.dump(NewData, outfile)       
        else:
            return print("Token already made!")
    except:
        return print("Error occured while handling the .json file.")




add_to_json(1)
            








