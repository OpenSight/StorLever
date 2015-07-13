  app.register.controller('Statistics', ['$scope', '$http', '$q', function($scope, $http, $q){
    $scope.cpu = (function(){
      return {
        init: function() {
          $scope.destroy();
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
        destroy: function(){
        }
      };
    })();

    $scope.io = (function(){
      return {
        init: function() {
          $scope.destroy();
          $scope.io.get();
        },
        get: function(){
          $scope.io.total = {};
          $scope.io.per = [];

          $scope.aborter = $q.defer();

          $scope.io.getData("/storlever/api/v1/system/disk_io_counters", 'total');
          $scope.io.getData("/storlever/api/v1/system/per_disk_io_counters", 'per');
        },
        getData: function(url, key){
          $http.get(url, {
            timeout: $scope.aborter.promise
          }).success(function(response) {
            $scope.io[key] = response;
          });
        },
        destroy: function(){
        }
      };
    })();

    $scope.destroy = function(){
      if (undefined !== $scope.aborter){
          $scope.aborter.resolve();
          delete $scope.aborter;
      }
    };

    $scope.$on('$destroy', $scope.destroy);
  }]);
