echo "couchdb couchdb/mode select clustered
couchdb couchdb/mode seen true
couchdb couchdb/nodename string couchdb@$1
couchdb couchdb/nodename seen true
couchdb couchdb/cookie string couchdb_cluster
couchdb couchdb/cookie seen true
couchdb couchdb/bindaddress string 0.0.0.0
couchdb couchdb/bindaddress seen true
couchdb couchdb/adminpass password admin
couchdb couchdb/adminpass seen true
couchdb couchdb/adminpass_again password admin
couchdb couchdb/adminpass_again seen true" | sudo debconf-set-selections