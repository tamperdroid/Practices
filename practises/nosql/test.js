var MongoClient = require('mongodb').MongoClient;

MongoClient.connect('mongodb://localhost:27017/student', function(err, db) {
  if (err) {
    throw err;
  }
  db.collection('json_col').find().toArray(function(err, result) {
    if (err) {
      throw err;
    }
    console.log(result);
  });
});

