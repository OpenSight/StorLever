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
            if (item.bDetailShown === undefined) item.bDetailShown = false;
            item.bDetailShown = !(true === item.bDetailShown);
            if (item.bDetailShown === true){//开
                $scope.config.init(item);
            }
        },
        refresh: function(){
            angular.forEach($scope.data.interfaces, function(item,index,array){
                item.bDetailShown = false;
            });
            ethList.init();
        }
      };
    })();

    $scope.config = (function(){
      return {
        get: function(item){
           if ( $scope.config.data == undefined){
               $scope.config.data = {};
           }

           $scope.aborter = $q.defer(),
           $http.get("/storlever/api/v1/network/eth_list/"+item.name, {
               timeout: $scope.aborter.promise
             }).success(function(response) {
               $scope.config.data[item.name] = response;
               $scope.config.data[item.name].enabled_bf = $scope.config.data[item.name].enabled;
             });
        },

        init: function(item) {
            if (item.bDetailShown === true){
              $scope.destroy();
                //初始化重新拿
              $scope.config.get(item);
            }
        },

        submitForm:function(item) {
            var putData = {
                ip: $scope.config.data[item.name].ip,
                netmask: $scope.config.data[item.name].netmask,
                gateway: $scope.config.data[item.name].gateway
            };

            $scope.aborter = $q.defer(),
            $http.put("/storlever/api/v1/network/eth_list/"+$scope.config.data[item.name].name, putData, {
                timeout: $scope.aborter.promise
            }).success(function(response) {

            }).error(function(response) {
                    alert("修改网络接口失败！");
            });
//op
            if ( $scope.config.data[item.name].enabled_bf !== $scope.config.data[item.name].enabled){
                var postData = {
                    opcode: ($scope.config.data[item.name].enabled === true)?"enable":"disable"
                };
                $scope.aborter = $q.defer(),
                $http.post("/storlever/api/v1/network/eth_list/"+$scope.config.data[item.name].name+"/op", postData, {
                    timeout: $scope.aborter.promise
                }).success(function(response) {

                    }).error(function(response) {
                        if ($scope.config.data.enabled === true)
                            alert("启用网络接口失败！");
                        else alert("停用网络接口失败！");
                    });
            }

        },

        destroy: function(){
        }
      };
    })();

    $scope.state = (function() {
      return {
        get: function(item){
            if ( $scope.state.data == undefined){
                $scope.state.data = {};
            }
          $scope.aborter = $q.defer(),
            $http.get("/storlever/api/v1/network/eth_list/"+item.name+"/stat", {
              timeout: $scope.aborter.promise
            }).success(function(response) {
              $scope.state.data[item.name] = response;
            });
        },
        init: function(item) {
            if (item.bDetailShown === true){
              $scope.destroy();
              $scope.state.get(item);
            }
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
