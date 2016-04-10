var app=angular.module("app",["ionic"]);
app.controller('appctrl', function($scope, $http,$log,$location) {
    $scope.add=function(auther,title,desc){
        $log.info(title);
	$log.info("HI");
        $log.info(auther);
        if ((auther==undefined)||(title==undefined)||(desc==undefined)){
	   alert("pls fill the required field");
	}

	else{
                var formData = {'auther':auther,'name':title,'price':desc};
                var postData = 'myData='+JSON.stringify(formData);
	       //var postData = {'myData':formData};
	    $http({   method:'POST',
                        url :'http://192.168.1.8:8081/post',
                        data:postData,
                        headers : {'Content-Type': 'application/x-www-form-urlencoded'}
                  }).success(function(res){
                        $log.info(res);
                        alert(res);
                  }).error(function(error){
                        $log.info(error);
        });
	}
}	
});
