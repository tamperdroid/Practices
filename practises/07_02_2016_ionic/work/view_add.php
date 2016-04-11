<?php
require_once("common/head.php");
?>
<script src="module/product_operations.js"></script>
</head>
<body ng-app="App" ng-controller="appctrl">
<div class="dashboard">
    <Button type="button" class="btn btn-success" ng-click="add(product_name,product_price)">Add</Button>
</div>
<div>
Product-Name<input type="text" id="production" ng-model="product_name">
Price<input type="text" id="price" ng-model="product_price">
<Button type="button" class="btn btn-warning" ng-click="update(product_name,product_price)">Edit</Button>
<Button type="button" class="btn btn-success" ng-click="del(product_name,product_price)">Delete</Button>
</div>
</body>
</html>                                		
