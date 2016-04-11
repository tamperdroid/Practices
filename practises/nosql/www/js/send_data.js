var app=angular.module("app",["ionic"]);
app.controller('appctrl', function($scope, $http,$log,$location) {
    $scope.add=function(title,desc){
        $log.info(title);
	$log.info("HI");
        $log.info(desc);
                var formData = {'name': title,'price':desc};
                var postData = 'myData='+JSON.stringify(formData);
	       //var postData = {'myData':formData};
	    $http({     method:'POST',
                        url : 'http://localhost/nosql/www/send_data.php',
                        data:postData,
                        headers : {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function(res){
                        $log.info(res);
                        alert(res);
                }).error(function(error){
                        $log.info(error);
        });
}
});
