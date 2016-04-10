    <?php
  
 if($_REQUEST['myData']) {
    $myData = json_decode($_POST['myData']);
    $name=$myData->name;
    $price=$myData->price;      
   
   $connection = new MongoClient();
   $db = $connection->student;
   $col=$db->json_col;
   $doc = array( 
      "title" => ".$name.", 
      "description" => ".$price."
   );
   $col->insert($doc);

?>

