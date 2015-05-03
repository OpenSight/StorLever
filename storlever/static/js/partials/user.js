(function(){
  controllers.controller('User', ['$scope', '$http', '$q', function($scope, $http, $q){
    $scope.data = (function(){
      return {
        get: function(){
          $scope.data.users = [];
          $scope.data.groups = [];
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
        },
        showAddForm: function(item){
          item.adding = !(true === item.adding);
        }
      };
    })();
    
    $scope.user = (function(){
      return {
        init: function() {
          $scope.distory();
          $scope.data.get();
        },
        distory: function(){
        }
      };
    })();

    $scope.group = (function() {
      return {
        init: function() {
          $scope.distory();          
          $scope.data.get();
        },
        showDetail: function(g){
          g.bDetailShown = !(true === g.bDetailShown);
          if (undefined !== g.users){
            return;
          }
          g.users = [];
          for (var i = 0, l = $scope.data.users.length; i < l; i ++){
            g.users.push({
              name: $scope.data.users[i].name,
              selected: -1 !== g.member.indexOf($scope.data.users[i].name)
            });
          }
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