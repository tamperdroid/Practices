angular.module('ionicApp', ['ionic'])

.controller('MyCtrl', function($scope,$http,$log) {
  $scope.groups = [];
   $log.info("Hi");
    $scope.getvalues=function(){
                        $scope.val=[];

            $http({     method:'GET',
                        url : 'http://192.168.1.8:8081/',
                        data:{},
                        headers : {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function(res){
                        $log.info(res);
                        val=res;
                        $scope.val=angular.copy(res);
			$log.info(val);
			for (var i=0; i<val.length; i++) {
			    $scope.groups[i] = {
			    name: val[i]["auther"],
			    items: []
		       	  };
			 // $scope.groups[i].items.push(val[i]["title"]+" "+val[i]["description"]);
			 $scope.groups[i].items.push(val[i]);
		  }
                }).finally(function() {
       // Stop the ion-refresher from spinning
       $scope.$broadcast('scroll.refreshComplete');
     })
.error(function(error){
                        $log.info(error);
        });
}

 $scope.toggleGroup = function(group) {
    if ($scope.isGroupShown(group)) {
      $scope.shownGroup = null;
    } else {
      $scope.shownGroup = group;
    }
  };
  $scope.isGroupShown = function(group) {
    return $scope.shownGroup === group;
  };
  
});
