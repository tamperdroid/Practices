var app=angular.module('app', []);
app.controller('productctrl', function($scope, $http,$log) {
    $log.info("Hi");
    $scope.getvalues=function(){
                        $scope.val=[];

            $http({     method:'GET',
                        url : 'get_data.php',
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

