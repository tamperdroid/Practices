angular.module('ionicApp', ['ionic'])

.controller('MyCtrl', function($scope,$http,$log) {
  $scope.groups = [];
   $log.info("Hi");
    $scope.getvalues=function(){
                        $scope.val=[];

            $http({     method:'GET',
                        url : 'http://192.168.1.8/nosql/www/get_data.php',
                        data:{},
                        headers : {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function(res){
                        $log.info(res);
                        val=res;
                        $scope.val=angular.copy(res);
			$log.info(val);
			for (var i=0; i<val.length; i++) {
			    $scope.groups[i] = {
			    name: i,
			    items: []
		       	  };
			 // $scope.groups[i].items.push(val[i]["title"]+" "+val[i]["description"]);
			 $scope.groups[i].items.push(val[i]);
		  }
                }).error(function(error){
                        $log.info(error);
        });
}

  /*
   * if given group is the selected group, deselect it
   * else, select the given group
   */
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
