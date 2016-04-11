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
    $myData = json_decode($_POST['myData']);
    $email=$myData->emailId;
    $pwd=$myData->password;      

    $q=mysql_query("select * from controlUsers where emailId='".$email."'");

    while($e=mysql_fetch_assoc($q)){
        $output[]=$e;
    }
     
    $encode = json_encode($output);
    $json = json_decode($encode, true);
    //echo $pwd;
    //echo $email;
    $md5_value =hash(md5,$pwd, FALSE);
    //echo $json;	    
    if(strcmp($json[0]['password'],$md5_value)==0){
	  echo "password matched";
     }
    else{
	echo "password not matched";
     }
//    echo $md5_value;
    mysql_close();
    ?>

