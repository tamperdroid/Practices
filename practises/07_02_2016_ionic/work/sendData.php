    <?php

	require_once("common/config.php");

    if($_REQUEST['myData']) {
    $myData = json_decode($_POST['myData']);
    $name=$myData->name;
    $price=$myData->price;      
    $q=mysql_query("insert into product_test values('".$name."','".$price."')");
    if ($q){
	echo "True";
    	}
     else{
	echo "False";
      }
    }elseif($_REQUEST['delete']){
        echo "hi";
	$del = json_decode($_POST['delete']);
    $name=$del->name;
    $price=$del->price;
	$q=mysql_query("delete from product_test  where  productname ='".$name."'");	
	echo "Hi";
	if($q){
	     echo "deletion successfully";
	}
	else{
	     echo "deletion failed";
	}
    }
    elseif($_REQUEST['update']){
        echo "hi";
	$update = json_decode($_POST['update']);
	$name=$update->name;
	$price=$update->price;
	$q=mysql_query("update product_test set productname ='".$name."' where productname ='".$price."'");	
	echo "Hi";
	if($q){
	     echo "deletion successfully";
	}
	else{
	     echo "deletion failed";
	}
    }
    mysql_close();
    ?>

