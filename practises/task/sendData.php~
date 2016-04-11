<?php
   $connection = new MongoClient();
   $db = $connection->student;
    if($_REQUEST['myData']) {
   	 $myData = json_decode($_POST['myData']);
	 $name=$myData->name;
	 $price=$myData->price;      
	 $col=$db->json_col;
	 $cursor= $col->find();

 	 echo $name;
	  echo $price;
	 $document = array( 
	      "title" => ".$name.", 
	      "description" => ".$price", 
	      "likes" => 100,
	      "url" => "http://www.tutorialspoint.com/mongodb/",
	      "by", "tutorials point"
	   );
	
   $col->insert($document);
   
 } 
?>
