import couchdb
import json

data = json.load(open('db_config.json'))
server_address = data["db_url"]
tweets_db_name = data["tweets_db_name"]
users_db_name = data["users_db_name"]
server = couchdb.Server(server_address)

while True:
    g = input("Which DB do you want to delete?\n \t 1. Tweets \n \t 2. Users \n Enter number :")
    if g == "1":
        sure = input("Are you sure you want to delete Tweets DB? (y/n) : ")
        if sure == 'y':
            try:
                del server[tweets_db_name]
            except:
                print("\nDB not found")
        else:
            print("Run script again to delete")
        break
    elif g == "2":
        sure = input("Are you sure you want to delete Users DB? (y/n) : ")
        if sure == 'y':
            try:
                del server[users_db_name]
            except:
                print("\nDB not found")
        else:
            print("Run script again to delete")
        break
    else:
        print("Please enter a correct number. \n")
