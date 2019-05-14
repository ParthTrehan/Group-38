import couchdb
import json
from datetime import datetime

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(" ", "_")

server_address = "http://admin:admin@127.0.0.1:5984"
data = json.load(open("new_result.json"))
couch = couchdb.Server(server_address)
try:
    results_db = couch["analyze_results"]
except:
    results_db = couch.create("analyze_results")
doc = {"_id" : now, "value" : data}

results_db.save(doc)