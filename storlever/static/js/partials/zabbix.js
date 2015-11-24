  app.register.controller('Zabbix', ['$scope', '$http', '$q', function($scope, $http, $q){
      $scope.zabbixConf = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.zabbixConf.get();
                  return true;
              },

              data_add: (function () {
                  return {
                      clean_data: function () {//clean add field
                          if ($scope.zabbixConf.data_add === undefined)
                              $scope.zabbixConf.data_add = {};
                          $scope.zabbixConf.data_add.hostname = "";
                          $scope.zabbixConf.data_add.refresh_active_check = "";
                      },

                      submitForm: function () {//add one zabbixConf
                          var putData = {
                              hostname: $scope.zabbixConf.data_add.hostname,
                              refresh_active_check: $scope.zabbixConf.data_add.refresh_active_check
                          };

                          $scope.zabbixConf.data_add.token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/zabbix_agent/conf", putData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {

                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "设置zabbix失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.zabbixConf.data_add.token;
                                      tmpMsg.Callback = "addzabbixConfCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.zabbixConf.show();
                                  });
                      },

                      init: function () {
                          $scope.zabbixConf.data_add.clean_data();
                      },

                      addzabbixConfCallBack:function (event, msg) {

                      }
                  };
              })(),

              get: function () {//clean input,get new
                  $scope.zabbixConf.data_add.clean_data();
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/utils/zabbix_agent/conf", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.zabbixConf.data_add.hostname = response.hostname;
                              $scope.zabbixConf.data_add.refresh_active_check = response.refresh_active_check;
                          });
              }
          }
      })();

      $scope.active_server = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.active_serverlist.get();
                  return true;
              },

              refresh: function () {
                  angular.forEach($scope.active_serverlist.data.servers, function (item, index, array) {
                      if ($scope.active_server.data_mod.bDetailShown !== undefined && $scope.active_server.data_mod.bDetailShown[index] !== undefined)
                          $scope.active_server.data_mod.bDetailShown[index]  = false;
                      if ($scope.active_serverlist.checkbox !== undefined
                          && ($scope.active_serverlist.checkbox[index] !== undefined ))//push unchecked for submit
                      {
                          $scope.active_serverlist.checkbox[index] = false;
                      }
                  });
                  if ($scope.active_serverlist !== undefined && $scope.active_serverlist.checkAllBox!==undefined)
                      $scope.active_serverlist.checkAllBox = false;

                  $scope.active_server.show();
              },

              add: function () {
                  if ($scope.active_server.addShown === undefined) $scope.active_server.addShown = false;
                  $scope.active_server.addShown = !$scope.active_server.addShown;
                  if ($scope.active_server.addShown === true)
                      $scope.active_server.data_add.init();
              },

              delete_all: function () {
                  // $scope.active_server.data.delToken = Math.random();
                  $scope.active_server.data.delArr = [];

                  angular.forEach($scope.active_serverlist.data.servers, function (item, index, array) {
                      if ($scope.active_serverlist !== undefined && $scope.active_serverlist.checkbox !== undefined
                          && ($scope.active_serverlist.checkbox[index] === false || $scope.active_serverlist.checkbox[index] === undefined))//push unchecked for submit
                      {
                          $scope.active_server.data.delArr.push(item);
                      }
                  });

                  $scope.active_server.data_del($scope.active_server.data.delArr);
              },

              data_del: function (submitArr) {
                  // $scope.active_server.data.delToken = Math.random();
                  var postData = submitArr;

                  $scope.active_server.data_del.token = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/utils/zabbix_agent/active_server_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.active_server.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除active_server失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.active_server.data_del.token;
                              tmpMsg.Callback = "delMutiactive_serverCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.active_server.refresh();
                          });
              },

              delMutiactive_serverCallBack:function (event, msg) {

              },

              data_add: (function () {
                  return {
                      clean_data: function () {//clean add field
                          if ($scope.active_server.data_add === undefined)
                              $scope.active_server.data_add = {};
                          $scope.active_server.data_add.active_server_addr = "";
                      },

                      submitForm: function () {//add one active_server
                          var isDuplicate = false;
                          var pushData =  $scope.active_server.data_add.active_server_addr;

                          if ($scope.active_serverlist.data.servers === undefined)
                              $scope.active_serverlist.data.servers = [];

                          angular.forEach($scope.active_serverlist.data.servers, function (item, index, array) {
                              if (item.toString() === $scope.active_server.data_add.active_server_addr.toString())
                              {
                                  isDuplicate = true;
                                  item = $scope.active_server.data_add.active_server_addr;
                              }
                          });

                          if (isDuplicate === false)
                              $scope.active_serverlist.data.servers.push(pushData);
                          var postData = $scope.active_serverlist.data.servers;

                          $scope.active_server.data_add.token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/zabbix_agent/active_server_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.active_server.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "添加active_server失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.active_server.data_add.token;
                                      tmpMsg.Callback = "addactive_serverCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.active_server.refresh();
                                  });
                      },

                      close: function () {//clean input,close add div
                          $scope.active_server.data_add.clean_data();
                          $scope.active_server.addShown = false;
                      },

                      init: function () {
                          $scope.active_server.data_add.clean_data();
                      },

                      addactive_serverCallBack:function (event, msg) {

                      }
                  };
              })(),

              delete_one: function (item) {
                  var tmpServerArr = [];

                  for(var i=0; i< $scope.active_serverlist.data.servers.length;i++){
                      if ($scope.active_serverlist.data.servers[i] !== item)
                          tmpServerArr.push($scope.active_serverlist.data.servers[i]);
                  }

                  var postData = tmpServerArr;

                  $scope.active_server.data.delOneToken = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/utils/zabbix_agent/active_server_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.active_server.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除active_server"+ item +"失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.active_server.data.delOneToken;
                              tmpMsg.Callback = "delactive_serverCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.active_server.refresh();
                          });
              },

              delactive_serverCallBack:function (event, msg) {

              },

              data: (function () {
                  return {
                      showDetail: function (item, index) {
                          if ($scope.active_server.data_mod.bDetailShown === undefined) $scope.active_server.data_mod.bDetailShown = [];
                          if ($scope.active_server.data_mod.bDetailShown[index] === undefined) $scope.active_server.data_mod.bDetailShown[index] = false;
                          $scope.active_server.data_mod.bDetailShown[index] = !(true === $scope.active_server.data_mod.bDetailShown[index]);
                          if ($scope.active_server.data_mod.bDetailShown[index] === true) {//开
                              $scope.active_server.data_mod.init(item, index);
                          } else {

                          }                      }

                  };
              })(),

              data_mod: (function () {
                  return {
                      init: function (item, index) {
                          if ($scope.active_server.data_mod.bDetailShown[index] === true) {
                              if ($scope.active_server.data_mod.active_server_addr === undefined) $scope.active_server.data_mod.active_server_addr = [];
                              $scope.active_server.data_mod.active_server_addr[index] = item;
                          }
                      },

                      submitForm: function (item, index) {
                          var tmpServerArr = [];

                          for(var i=0; i< $scope.active_serverlist.data.servers.length;i++){
                              if (i !== index)
                                  tmpServerArr.push($scope.active_serverlist.data.servers[i]);
                              else{
                                  var tmpModData = $scope.active_server.data_mod.active_server_addr[index];
                                  tmpServerArr.push(tmpModData);
                              }
                          }

                          var postData = tmpServerArr;

                          $scope.active_server.data_mod.Token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/zabbix_agent/active_server_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.active_server.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "修改active_server"+ item.active_server_addr +"失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.active_server.data_mod.Token;
                                      tmpMsg.Callback = "modactive_serverCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.active_server.refresh();
                                  });
                      },

                      modactive_serverCallBack:function (event, msg) {

                      },

                      destroy: function () {
                      }
                  };
              })()

          }
      })();

      $scope.active_serverlist = (function () {
          return {
              toggle_all: function () {
                  if ($scope.active_serverlist.checkAllBox === undefined) $scope.active_serverlist.checkAllBox = false;
                  $scope.active_serverlist.checkAllBox = !$scope.active_serverlist.checkAllBox;
                  var nowCheckState = $scope.active_serverlist.checkAllBox;
                  if ($scope.active_serverlist.checkbox === undefined) $scope.active_serverlist.checkbox = [];

                  angular.forEach($scope.active_serverlist.data.servers, function (item, index, array) {
                      $scope.active_serverlist.checkbox[index] = nowCheckState;
                  });

              },

              get: function () {//clean input,close add div
                  $scope.active_server.data_add.clean_data();
                  //$scope.active_server.addShown = false;
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/utils/zabbix_agent/active_server_list", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.active_serverlist.data = {};
                              $scope.active_serverlist.data.servers = response;
                          });
              }


          };
      })();


      $scope.passive_server = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.passive_serverlist.get();
                  return true;
              },

              refresh: function () {
                  angular.forEach($scope.passive_serverlist.data.servers, function (item, index, array) {
                      if ($scope.passive_server.data_mod.bDetailShown !== undefined && $scope.passive_server.data_mod.bDetailShown[index] !== undefined)
                          $scope.passive_server.data_mod.bDetailShown[index]  = false;
                      if ($scope.passive_serverlist.checkbox !== undefined
                          && ($scope.passive_serverlist.checkbox[index] !== undefined ))//push unchecked for submit
                      {
                          $scope.passive_serverlist.checkbox[index] = false;
                      }
                  });
                  if ($scope.passive_serverlist !== undefined && $scope.passive_serverlist.checkAllBox!==undefined)
                      $scope.passive_serverlist.checkAllBox = false;

                  $scope.passive_server.show();
              },

              add: function () {
                  if ($scope.passive_server.addShown === undefined) $scope.passive_server.addShown = false;
                  $scope.passive_server.addShown = !$scope.passive_server.addShown;
                  if ($scope.passive_server.addShown === true)
                      $scope.passive_server.data_add.init();
              },

              delete_all: function () {
                  // $scope.passive_server.data.delToken = Math.random();
                  $scope.passive_server.data.delArr = [];

                  angular.forEach($scope.passive_serverlist.data.servers, function (item, index, array) {
                      if ($scope.passive_serverlist !== undefined && $scope.passive_serverlist.checkbox !== undefined
                          && ($scope.passive_serverlist.checkbox[index] === false || $scope.passive_serverlist.checkbox[index] === undefined))//push unchecked for submit
                      {
                          $scope.passive_server.data.delArr.push(item);
                      }
                  });

                  $scope.passive_server.data_del($scope.passive_server.data.delArr);
              },

              data_del: function (submitArr) {
                  // $scope.passive_server.data.delToken = Math.random();
                  var postData = submitArr;

                  $scope.passive_server.data_del.token = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/utils/zabbix_agent/passive_server_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.passive_server.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除passive_server失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.passive_server.data_del.token;
                              tmpMsg.Callback = "delMutipassive_serverCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.passive_server.refresh();
                          });
              },

              delMutipassive_serverCallBack:function (event, msg) {

              },

              data_add: (function () {
                  return {
                      clean_data: function () {//clean add field
                          if ($scope.passive_server.data_add === undefined)
                              $scope.passive_server.data_add = {};
                          $scope.passive_server.data_add.passive_server_addr = "";
                      },

                      submitForm: function () {//add one passive_server
                          var isDuplicate = false;
                          var pushData =  $scope.passive_server.data_add.passive_server_addr;

                          if ($scope.passive_serverlist.data.servers === undefined)
                              $scope.passive_serverlist.data.servers = [];

                          angular.forEach($scope.passive_serverlist.data.servers, function (item, index, array) {
                              if (item.toString() === $scope.passive_server.data_add.passive_server_addr.toString())
                              {
                                  isDuplicate = true;
                                  item = $scope.passive_server.data_add.passive_server_addr;
                              }
                          });

                          if (isDuplicate === false)
                              $scope.passive_serverlist.data.servers.push(pushData);
                          var postData = $scope.passive_serverlist.data.servers;

                          $scope.passive_server.data_add.token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/zabbix_agent/passive_server_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.passive_server.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "添加passive_server失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.passive_server.data_add.token;
                                      tmpMsg.Callback = "addpassive_serverCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.passive_server.refresh();
                                  });
                      },

                      close: function () {//clean input,close add div
                          $scope.passive_server.data_add.clean_data();
                          $scope.passive_server.addShown = false;
                      },

                      init: function () {
                          $scope.passive_server.data_add.clean_data();
                      },

                      addpassive_serverCallBack:function (event, msg) {

                      }
                  };
              })(),

              delete_one: function (item) {
                  var tmpServerArr = [];

                  for(var i=0; i< $scope.passive_serverlist.data.servers.length;i++){
                      if ($scope.passive_serverlist.data.servers[i] !== item)
                          tmpServerArr.push($scope.passive_serverlist.data.servers[i]);
                  }

                  var postData = tmpServerArr;

                  $scope.passive_server.data.delOneToken = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/utils/zabbix_agent/passive_server_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.passive_server.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除passive_server"+ item +"失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.passive_server.data.delOneToken;
                              tmpMsg.Callback = "delpassive_serverCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.passive_server.refresh();
                          });
              },

              delpassive_serverCallBack:function (event, msg) {

              },

              data: (function () {
                  return {
                      showDetail: function (item, index) {
                          if ($scope.passive_server.data_mod.bDetailShown === undefined) $scope.passive_server.data_mod.bDetailShown = [];
                          if ($scope.passive_server.data_mod.bDetailShown[index] === undefined) $scope.passive_server.data_mod.bDetailShown[index] = false;
                          $scope.passive_server.data_mod.bDetailShown[index] = !(true === $scope.passive_server.data_mod.bDetailShown[index]);
                          if ($scope.passive_server.data_mod.bDetailShown[index] === true) {//开
                              $scope.passive_server.data_mod.init(item, index);
                          } else {

                          }                      }

                  };
              })(),

              data_mod: (function () {
                  return {
                      init: function (item, index) {
                          if ($scope.passive_server.data_mod.bDetailShown[index] === true) {
                              if ($scope.passive_server.data_mod.passive_server_addr === undefined) $scope.passive_server.data_mod.passive_server_addr = [];
                              $scope.passive_server.data_mod.passive_server_addr[index] = item;
                          }
                      },

                      submitForm: function (item, index) {
                          var tmpServerArr = [];

                          for(var i=0; i< $scope.passive_serverlist.data.servers.length;i++){
                              if (i !== index)
                                  tmpServerArr.push($scope.passive_serverlist.data.servers[i]);
                              else{
                                  var tmpModData = $scope.passive_server.data_mod.passive_server_addr[index];
                                  tmpServerArr.push(tmpModData);
                              }
                          }

                          var postData = tmpServerArr;

                          $scope.passive_server.data_mod.Token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/zabbix_agent/passive_server_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.passive_server.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "修改passive_server"+ item.passive_server_addr +"失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.passive_server.data_mod.Token;
                                      tmpMsg.Callback = "modpassive_serverCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.passive_server.refresh();
                                  });
                      },

                      modpassive_serverCallBack:function (event, msg) {

                      },

                      destroy: function () {
                      }
                  };
              })()

          }
      })();

      $scope.passive_serverlist = (function () {
          return {
              toggle_all: function () {
                  if ($scope.passive_serverlist.checkAllBox === undefined) $scope.passive_serverlist.checkAllBox = false;
                  $scope.passive_serverlist.checkAllBox = !$scope.passive_serverlist.checkAllBox;
                  var nowCheckState = $scope.passive_serverlist.checkAllBox;
                  if ($scope.passive_serverlist.checkbox === undefined) $scope.passive_serverlist.checkbox = [];

                  angular.forEach($scope.passive_serverlist.data.servers, function (item, index, array) {
                      $scope.passive_serverlist.checkbox[index] = nowCheckState;
                  });

              },

              get: function () {//clean input,close add div
                  $scope.passive_server.data_add.clean_data();
                  //$scope.passive_server.addShown = false;
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/utils/zabbix_agent/passive_server_list", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.passive_serverlist.data = {};
                              $scope.passive_serverlist.data.servers = response;
                          });
              }


          };
      })();
      
      $scope.destroy = function () {
          if (undefined !== $scope.aborter) {
              $scope.aborter.resolve();
              delete $scope.aborter;
          }
      };

      $scope.$on('$destroy', $scope.destroy);

//add all callback
      $scope.$on('addzabbixConfCallBack', $scope.zabbixConf.data_add.addzabbixConfCallBack);
      $scope.$on('modactive_serverCallBack', $scope.active_server.data_mod.modactive_serverCallBack);
      $scope.$on('addactive_serverCallBack', $scope.active_server.data_add.addactive_serverCallBack);
      $scope.$on('delactive_serverCallBack', $scope.active_server.delactive_serverCallBack);
      $scope.$on('delMutiactive_serverCallBack', $scope.active_server.delMutiactive_serverCallBack);
      $scope.$on('modpassive_serverCallBack', $scope.passive_server.data_mod.modpassive_serverCallBack);
      $scope.$on('addpassive_serverCallBack', $scope.passive_server.data_add.addpassive_serverCallBack);
      $scope.$on('delpassive_serverCallBack', $scope.passive_server.delpassive_serverCallBack);
      $scope.$on('delMutipassive_serverCallBack', $scope.passive_server.delMutipassive_serverCallBack);


  }]);
