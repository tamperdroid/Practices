    <?php
//header('Access-Control-Allow-Origin: *');  
//header('Access-Control-Allow-Headers:Content-Type');
if (isset($_SERVER['HTTP_ORIGIN'])) {
        header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
        header('Access-Control-Allow-Credentials: true');
        header('Access-Control-Max-Age: 86400');    // cache for 1 day
    }

    // Access-Control headers are received during OPTIONS requests
    if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {

        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
            header("Access-Control-Allow-Methods: GET, POST, OPTIONS");         

        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
            header("Access-Control-Allow-Headers:        
            {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");

        exit(0);
    }

    mysql_connect("localhost","root","qw12");
    mysql_select_db("ge_admin");
    
    if (_REQUEST['Admin'])
    {
	header("Location: http://192.168.1.170/task/bootstrap_add.html");
    }
    elseif(_POST['myData']) {
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
}
    elseif(_REQUEST['delete']){
	
	$q="delete product_test values where '".."'";	
	if (){
		echo "deletion successfully";
	}
	else{
		echo "deletion failed";
	}
    }
    mysql_close();
    ?>

