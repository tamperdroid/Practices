<?php
   $connection = new MongoClient();
   $db = $connection->student;
   $col=$db->json_col;
   $cursor= $col->find();

  foreach ($cursor as $document) {
      	$output[]=$document;
   }

   $encode = json_encode($output);
    echo $encode;
?>
