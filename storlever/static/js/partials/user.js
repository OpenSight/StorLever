(function(){
  controllers.controller('User', ['$scope', '$http', '$q', function($scope, $http, $q){
    $scope.data = (function(){
      return {
        get: function(){
          $scope.aborter = $q.defer(),
          $http.get("/storlever/api/v1/system/user_list", {
            timeout: $scope.aborter.promise
          }).success(function(response) {
            $scope.data.users = response;
          });
          
          $http.get("/storlever/api/v1/system/group_list", {
            timeout: $scope.aborter.promise
          }).success(function(response) {
            $scope.data.groups = response;
          });
        },
        showDetail: function(item){
          item.bDetailShown = !(true === item.bDetailShown);
        }
      };
    })();
    
    $scope.user = (function(){
      return {
        init: function() {
          $scope.distory();
          $scope.data.get();
        },
        showAddForm: function() {
          $scope.user.adding = !(true === $scope.user.adding);
        },
        distory: function(){
        }
      };
    })();

    $scope.group = (function() {
      return {
        init: function() {
          $scope.distory();          
          $scope.aborter = $q.defer(),
            $http.get("/storlever/api/v1/system/group_list", {
              timeout: $scope.aborter.promise
            }).success(function(response) {
              $scope.group.list = response;
            });
        },
		distory: function(){}
      };
    })();
    

    $scope.distory = function(){
      if (undefined !== $scope.aborter){
          $scope.aborter.resolve();
          delete $scope.aborter;
      }
    };

    $scope.$on('$destroy', $scope.distory);
  }]);
})();