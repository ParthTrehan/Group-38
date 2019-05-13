#!/bin/bash
export masternode=$1
export node=$2
curl -XPOST "http://admin:admin@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \
        \"username\": \"admin\", \"password\":\"admin\", \"port\": \"5984\", \
        \"remote_node\": \"${node}\", \
        \"remote_current_user\":\"admin\", \"remote_current_password\":\"admin\"}"

curl -XPOST "http://admin:admin@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"add_node\", \"host\":\"${node}\", \
        \"port\": \"5984\", \"username\": \"admin\", \"password\":\"admin\"}"