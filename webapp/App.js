const express = require('express');
const bodyparser = require('body-parser');
const path = require('path');
const NodeCouchDb = require('node-couchdb');

// node-couchdb instance talking to external service
const couchExternal = new NodeCouchDb({
    host: 'admin:admin@172.26.38.34',
    protocol: 'http',
    port: 5984
});

couchExternal.listDatabases().then(function (dbs) {
    console.log(dbs);
});

const dbName = 'grid';
const resultsDbName = 'analyze_results';
const gridViewUrl = '_design/get_map/_view/grid';
const resultViewUrl = '/_all_docs?descending=true&include_docs=true&limit=1';
const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(bodyparser.json());
app.use(bodyparser.urlencoded({
    extended: false
}));

app.get('/', function (req, res) {
    couchExternal.get(dbName, gridViewUrl).then(
        function (data, headers, status) {
            res.render('index', {
                grid: data.data.rows[0]
            });
        },
        function name(err) {
            res.send(err);
        });
});

app.get('/data', function (req, res) {
    var jsonData = {};
    couchExternal.get(resultsDbName, resultViewUrl).then(
        function (data, headers, status) {
            res.setHeader('Content-Type', 'application/json');
            jsonData = data.data.rows[0].doc.value;
            res.end(JSON.stringify(jsonData));
        },
        function name(err) {
            res.end(err);
        });
});

app.listen(3000, function () {
    console.log('Server started on port 3000')
})