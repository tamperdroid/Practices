<?php
   $connection = new MongoClient();
   $db = $connection->student;
    if($_REQUEST['myData']) {
   	 $myData = json_decode($_POST['myData']);
	 $name=$myData->name;
	 $price=$myData->price;      
	 $col=$db->json_col;
	 $cursor= $col->find();

	 $document = array( 
	      "title" => ".$name.", 
	      "description" => ".$price" 
	   );
	
   $col->insert($document);
   echo "insertion success" ;
 } 
?>
