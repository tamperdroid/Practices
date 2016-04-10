var app=angular.module('app_dashboard', []);

app.controller('productctrl', function($scope, $http,$log) {
    $log.info("Hi");
    $scope.getvalues=function(){
			$scope.val=[];
		
       	    $http({     method:'GET',
                        url : 'getData.php',
                        data:{},
                        headers : {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function(res){
                        $log.info(res);
			val=res;
			$scope.val=angular.copy(res);
                }).error(function(error){
                        $log.info(error);
        });
}

});

