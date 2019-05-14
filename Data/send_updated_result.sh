#!/bin/sh
curl -X PUT http://admin:admin@localhost:5984/tweets/_design/tweets-reduce -d @views.json
while true; do
    curl http://admin:admin@127.0.0.1:5984/tweets/_design/tweets-reduce/_view/all-tweets?group_level=3 > new_result.json;
    python send_new_result.py 
    sleep 60;
done