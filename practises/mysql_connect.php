    <?php
    
    $email = $_REQUEST['emailId'];
    mysql_connect("localhost","root","qw12");
    mysql_select_db("ge_admin");
    
   
    $q=mysql_query("select * from controlUsers where emailId='".$email."'");
//   $res = mysql_fetch_row($q);
    //print_r($res);

while($e=mysql_fetch_assoc($q)){
//	print_r($e);
        $output[]=$e;
     }
    //    print(json_encode($output));*/
    $encode = json_encode($output);
    echo $encode;
    mysql_close();
    ?>

