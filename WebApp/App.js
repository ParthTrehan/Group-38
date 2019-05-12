const express = require('express');
const bodyparser = require('body-parser');
const path = require('path');
const NodeCouchDb = require('node-couchdb');

const couch = new NodeCouchDb({
    auth: {
        user: 'admin',
        password: 'admin'
    }
});

couch.listDatabases().then(function (dbs) {
    console.log(dbs);
});

const dbName = 'mycompany';
const viewurl = '_design/get_grid/_view/new-view';
const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(bodyparser.json());
app.use(bodyparser.urlencoded({ extended: false }));

app.get('/', function (req, res) {
    couch.get(dbName, viewurl).then(
        function (data, headers, status) {
            res.render('index', {
                grid:data.data.rows[0]
            });
        },
        function name(err) {
            res.send(err);
        });
});

app.listen(3000, function () {
    console.log('Server started on port 3000')
})