<?php
    require("common/config.php");
    $q=mysql_query("select * from product_test");

    while($e=mysql_fetch_assoc($q)){
        $output[]=$e;
    }

    $encode = json_encode($output);
    
    echo $encode
?>
