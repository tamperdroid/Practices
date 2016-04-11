<?php
require_once("common/head.php");
?>

<script src="module/dashbord.js"></script>

<style type="text/css">
body { 
background: url("cinqueterre.jpg")  repeat ; 
background-size: cover;
}
.dashboard{
margin:50px 20px 20px 20px;
}
.hi{
margin:30px;
}
</style>

</head>
<body class="hi" ng-app="app_dashboard"  ng-controller="productctrl" ng-init="getvalues()" >
<div class="panel panel-success">

<div class="panel-heading">DASHBOARD</div>
<a ng-href="view_add.php">ADD</a>
</div>
<div class="dashboard" >
<div class="row" ng-repeat="row in val" ng-if="$index % 2 == 0">
<div class="col-xs-6">
    <div class="panel panel-primary" >
        <div class="panel-heading">Product Name {{val[$index].productname}}</div>
        <div class="panel-heading">Price {{val[$index].product_price}}</div>
    </div>
</div>
<div class="col-xs-6">
    <div class="panel panel-primary" >
        <div class="panel-heading">Product Name {{val[$index+1].productname}}</div>
        <div class="panel-heading">Price {{val[$index+1].product_price}}</div>
    </div>
</div>

</div>

</div>
</body>
</html>                                		
