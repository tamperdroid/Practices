var app=angular.module('App', []);

app.controller('appctrl', function($scope, $http,$log,$location) {
    $scope.add=function(product_name,product_price){
        $log.info(product_name);
	$log.info("HI");
        $log.info(product_price);
                var formData = {'name': product_name,'price':product_price};
                var postData = 'myData='+JSON.stringify(formData);
	    $http({     method:'POST',
                        url : 'sendData.php',
                        data:postData,
                        headers : {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function(res){
                        $log.info(res);
                       alert("Added");
                        if (res=="True"){
				
				$window.location.href = 'index.php';
                        }
                }).error(function(error){
                        $log.info(error);
        });
}
	
	$scope.del=function(product_name,product_price){
	var form = {'name':product_name,'price':product_price};
	var del='delete='+JSON.stringify(form);
	 $http({     method:'POST',
                        url : 'sendData.php',
                        data:del,
                        headers : {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function(res){
                        $log.info(res);
                       alert(res);
                        if (res=="True"){
				
				$window.location.href = 'index.php';
                        }
                }).error(function(error){
                        $log.info(error);
        });
}
      $scope.update=function(product_name,product_price){
	var formupdate = {'name':product_name,'price':product_price};
	var update='update='+JSON.stringify(formupdate);
	 $http({     method:'POST',
                        url : 'sendData.php',
                        data:update,
                        headers : {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function(res){
                        $log.info(res);
                       alert(res);
                        if (res=="True"){
				
				$window.location.href = 'index.php';
                        }
                }).error(function(error){
                        $log.info(error);
        });
}
});

