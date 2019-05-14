const express = require('express');
const bodyparser = require('body-parser');
const path = require('path');
const NodeCouchDb = require('node-couchdb');

// node-couchdb instance talking to external service
const couchExternal = new NodeCouchDb({
    host: 'admin:admin@127.0.0.1',
    protocol: 'http',
    port: 5984
});

couchExternal.listDatabases().then(function (dbs) {
    console.log(dbs);
});

const dbName = 'grid';
const gridViewUrl = '_design/get_map/_view/grid';
const resultViewUrl = '/analyze_results/_all_docs?descending=true&include_docs=true&limit=1';
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
    couchExternal.get(dbName, resultViewUrl).then(
        function (data, headers, status) {
            res.render('index', {
                grid: data.rows[0].doc.value
            });
        },
        function name(err) {
            res.send(err);
        });
});

app.listen(3000, function () {
    console.log('Server started on port 3000')
})