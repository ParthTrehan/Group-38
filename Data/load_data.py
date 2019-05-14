import couchdb
import json

server_address = "http://admin:admin@172.26.38.88:5984"
data = json.load(open("new_result.json"))
couch = couchdb.Server(server_address)
input_file = ""
try:
    results_db = couch["analyze_results"]
except:
    results_db = couch.create("analyze_results")

with open(input_file, 'rt', encoding='utf8') as f: