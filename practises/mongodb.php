<?php
   $m = new MongoClient();
   echo "Connection to database successfully";
	
   $db = $m->student;
   echo "Database mydb selected";
   $collection = $db->json_col;
   echo "Collection selected succsessfully";

   $cursor = $collection->find();
   // iterate cursor to display title of documents
	
   foreach ($cursor as $document) {
      echo $document. "\n";
   }
?>
