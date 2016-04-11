var express = require('express');
var MongoClient = require('mongodb').MongoClient;
var stringify = require('json-stringify-safe');
var bodyParser = require('body-parser');

var app = express();

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.use(bodyParser());

app.get('/', function (req, res) {
  MongoClient.connect('mongodb://localhost:27017/student', function(err, db) {
  if (err) {
    throw err;
  }
  db.collection('json_col').find().toArray(function(err, result) {
    if (err) {
      throw err;
    }
    console.log(result);
    res.send(result);
  });
});

})

app.post('/post', function (req, res) {

	var data= JSON.parse(req.body.myData);
	var name=data.name;
	var desc=data.price;
	var auther=data.auther;
	console.log(JSON.parse(req.body.myData).price);
  MongoClient.connect('mongodb://localhost:27017/student', function(err, db) {
  if (err) {
    throw err;
  }

var document ={auther:auther,title:name,description:desc};

	db.collection('json_col').insert(document, function(err, records) {
		if (err) throw err;
		console.log("Record added as "+records);
	}); 
});
	res.send("insert sucessfully");
})


var server = app.listen(8081, function () {

  var host = server.address().address
  var port = server.address().port

  console.log("listening at http://%s:%s", host, port)
})
