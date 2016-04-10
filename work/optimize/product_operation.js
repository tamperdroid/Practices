var app=angular.module('app', []);

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
                       
                        if (res=="True"){
				alert(res);
				$window.location.href = 'index.html';
                        }
                }).error(function(error){
                        $log.info(error);
        });
}
});
