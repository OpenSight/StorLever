  app.register.controller('Statistics', ['$scope', '$http', '$q', function($scope, $http, $q){
    $scope.cpu = (function(){
      return {
        init: function() {
          $scope.distory();
          $scope.cpu.get();
        },
        get: function(){
          $scope.cpu.total = {};
          $scope.cpu.mem = {};
          $scope.cpu.per = [];

          $scope.aborter = $q.defer(),

          $scope.cpu.getData("/storlever/api/v1/system/cpu_times", 'total');
          $scope.cpu.getData("/storlever/api/v1/system/memory", 'mem');
          $scope.cpu.getData("/storlever/api/v1/system/per_cpu_times", 'per');
        },
        getData: function(url, key){
          $http.get(url, {
            timeout: $scope.aborter.promise
          }).success(function(response) {
            $scope.cpu[key] = response;
          });
        },
        distory: function(){
        }
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
