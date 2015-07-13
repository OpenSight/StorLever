/*
* /network/eth_list
 /network/eth_list/{port_name}
 /network/bond/bond_list
 /network/bond/bond_list/{port_name}
 /network/eth_list/{port_name}/op*/
  app.register.controller('Interface', ['$scope', '$http', '$q', function($scope, $http, $q){

    $scope.data = (function(){
      return {
        get: function(){
          $scope.data.interfaces = [];
          $scope.aborter = $q.defer(),
          $http.get("/storlever/api/v1/network/eth_list", {
            timeout: $scope.aborter.promise
          }).success(function(response) {
            $scope.data.interfaces = response;
          });
        },
        showDetail: function(item){
          item.bDetailShown = !(true === item.bDetailShown);
        }
      };
    })();

    $scope.config = (function(){
      return {
        get: function(item){
           $scope.aborter = $q.defer(),
           $http.get("/storlever/api/v1/network/eth_list/"+item.name, {
               timeout: $scope.aborter.promise
             }).success(function(response) {
               $scope.config.data = response;
             });
        },

        init: function(item) {
          $scope.destroy();
            //初始化重新拿
          $scope.config.get(item);
        },

        submitForm:function() {
            var putData = {
                ip: $scope.config.data.ip,
                netmask: $scope.config.data.netmask,
                gateway: $scope.config.data.gateway
            };

            $scope.aborter = $q.defer(),
            $http.put("/storlever/api/v1/network/eth_list/"+$scope.config.data.name, putData, {
                timeout: $scope.aborter.promise
            }).success(function(response) {

            }).error(function(response) {
                    alert("修改网络接口失败！");
            });
//op
            var postData = {
                opcode: $scope.config.data.enabled?"enable":"disable"
            };
            $scope.aborter = $q.defer(),
                $http.post("/storlever/api/v1/network/eth_list/"+$scope.config.data.name+"/op", postData, {
                    timeout: $scope.aborter.promise
                }).success(function(response) {

                    }).error(function(response) {
                        if ($scope.config.data.enabled)
                            alert("启用网络接口失败！");
                        else alert("停用网络接口失败！");
                    });

        },

        destroy: function(){
        }
      };
    })();

    $scope.state = (function() {
      return {
        get: function(item){
          $scope.aborter = $q.defer(),
            $http.get("/storlever/api/v1/network/eth_list/"+item.name+"/stat", {
              timeout: $scope.aborter.promise
            }).success(function(response) {
              $scope.state.data = response;
            });
        },
        init: function(item) {
          $scope.destroy();          
          $scope.state.get(item);
        },

        destroy: function(){}
      };
    })();
    

    $scope.destroy = function(){
      if (undefined !== $scope.aborter){
          $scope.aborter.resolve();
          delete $scope.aborter;
      }
    };

    $scope.$on('$destroy', $scope.destroy);

      var ethList = (function() {
          return {
              init: function() {
                  $scope.destroy();
                  $scope.data.get();
                  return true;
              },

              destroy: function(){}
          };
      })();

      ethList.init();
  }]);
