  app.register.controller('Ntp', ['$scope', '$http', '$q', function($scope, $http, $q){
      $scope.server = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.serverlist.get();
                  return true;
              },
              
              refresh: function () {
                     angular.forEach($scope.serverlist.data.servers, function (item, index, array) {
                         if ($scope.server.data_mod.bDetailShown && $scope.server.data_mod.bDetailShown[index] !== undefined)
                          $scope.server.data_mod.bDetailShown[index]  = false;
                         if ($scope.serverlist.checkbox !== undefined
                              && ($scope.serverlist.checkbox[index] !== undefined ))//push unchecked for submit
                         {
                             $scope.serverlist.checkbox[index] = false;
                         }
                      });

                  if ($scope.serverlist !==undefined && $scope.serverlist.checkAllBox!==undefined)
                      $scope.serverlist.checkAllBox = false;
                  $scope.server.show();
              },
              
              add: function () {
                  if ($scope.server.addShown === undefined) $scope.server.addShown = false;
                  $scope.server.addShown = !$scope.server.addShown;
                  if ($scope.server.addShown === true)
                      $scope.server.data_add.init();
              },
              
              delete_all: function () {
                 // $scope.server.data.delToken = Math.random();
                  $scope.server.data.delArr = [];

                  angular.forEach($scope.serverlist.data.servers, function (item, index, array) {
                      if ($scope.serverlist !== undefined && $scope.serverlist.checkbox !== undefined
                          && ($scope.serverlist.checkbox[index] === false || $scope.serverlist.checkbox[index] === undefined))//push unchecked for submit
                      {
                        $scope.server.data.delArr.push(item);
                      }
                  });

                  $scope.server.data_del($scope.server.data.delArr);
              },

              data_del: function (submitArr) {
                  // $scope.server.data.delToken = Math.random();
                  var postData =  submitArr;

                  $scope.server.data_del.token = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/utils/ntp/server_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.server.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除server失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.server.data_del.token;
                              tmpMsg.Callback = "delMutiserverCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.server.refresh();
                          });
              },

              delMutiserverCallBack:function (event, msg) {

              },

              data_add: (function () {
                  return {
                      clean_data: function () {//clean add field
                          if ($scope.server.data_add === undefined)
                              $scope.server.data_add = {};
                          $scope.server.data_add.server_addr = "";
                          $scope.server.data_add.ipv6 = false;
                          $scope.server.data_add.prefer = false;
                          $scope.server.data_add.mode = 0;
                          $scope.server.data_add.stratum = 0;
                          $scope.server.data_add.flag1 = 0;
                          $scope.server.data_add.flag2 = 0;
                          $scope.server.data_add.flag3 = 0;
                          $scope.server.data_add.flag4 = 0;
                      },

                      submitForm: function () {//add one server
                          var isDuplicate = false;
                          var pushData = {
                              server_addr: $scope.server.data_add.server_addr,
                              ipv6: $scope.server.data_add.ipv6,
                              prefer: $scope.server.data_add.prefer,
                              mode: $scope.server.data_add.mode,
                              stratum: $scope.server.data_add.stratum,
                              flag1: $scope.server.data_add.flag1,
                              flag2: $scope.server.data_add.flag2,
                              flag3: $scope.server.data_add.flag3,
                              flag4: $scope.server.data_add.flag4
                          };

                          angular.forEach($scope.serverlist.data.servers, function (item, index, array) {
                                  if (item.server_addr.toString() === $scope.server.data_add.server_addr.toString())
                                  {
                                      isDuplicate = true;
                                      item.server_addr = $scope.server.data_add.server_addr;
                                      item.ipv6 = $scope.server.data_add.ipv6;
                                      item.prefer = $scope.server.data_add.prefer;
                                      item.mode = $scope.server.data_add.mode;
                                      item.stratum = $scope.server.data_add.stratum;
                                      item.flag1 = $scope.server.data_add.flag1;
                                      item.flag2 = $scope.server.data_add.flag2;
                                      item.flag3 = $scope.server.data_add.flag3;
                                      item.flag4 =  $scope.server.data_add.flag4;
                                  }
                          });

                          if (isDuplicate === false)
                              $scope.serverlist.data.servers.push(pushData);


                          var postData = $scope.serverlist.data.servers;

                          $scope.server.data_add.token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/ntp/server_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.server.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "添加server失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.server.data_add.token;
                                      tmpMsg.Callback = "addserverCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.server.refresh();
                                  });
                      },

                      close: function () {//clean input,close add div
                          $scope.server.data_add.clean_data();
                          $scope.server.addShown = false;
                      },

                      init: function () {
                          $scope.server.data_add.clean_data();
                      },

                      addserverCallBack:function (event, msg) {

                      }
                  };
              })(),

              delete_one: function (item) {
                  var tmpServerArr = [];

                  for(var i=0; i< $scope.serverlist.data.servers.length;i++){
                      if ($scope.serverlist.data.servers[i] !== item)
                          tmpServerArr.push($scope.serverlist.data.servers[i]);
                  }

                  var postData =  tmpServerArr;

                  $scope.server.data.delOneToken = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/utils/ntp/server_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.server.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除server"+ item.server_addr +"失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.server.data.delOneToken;
                              tmpMsg.Callback = "delserverCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.server.refresh();
                          });
              },

              delserverCallBack:function (event, msg) {

              },

              data: (function () {
                  return {
                      showDetail: function (item, index) {
                          if ($scope.server.data_mod.bDetailShown === undefined) $scope.server.data_mod.bDetailShown = [];
                          if ($scope.server.data_mod.bDetailShown[index] === undefined) $scope.server.data_mod.bDetailShown[index] = false;
                          $scope.server.data_mod.bDetailShown[index] = !(true === $scope.server.data_mod.bDetailShown[index]);
                          if ($scope.server.data_mod.bDetailShown[index] === true) {//开
                              $scope.server.data_mod.init(item,index);
                          } else {
                              
                          }
                      }
                  };
              })(),

              data_mod: (function () {
                  return {
                      init: function (item, index) {
                          if ($scope.server.data_mod.bDetailShown[index] === true) {
                              if ($scope.server.data_mod.server_addr === undefined) $scope.server.data_mod.server_addr = [];
                              $scope.server.data_mod.server_addr[index] = item.server_addr;
                              if ($scope.server.data_mod.ipv6 === undefined) $scope.server.data_mod.ipv6 = [];
                              $scope.server.data_mod.ipv6[index] = item.ipv6;
                              if ($scope.server.data_mod.prefer === undefined) $scope.server.data_mod.prefer = [];
                              $scope.server.data_mod.prefer[index] = item.prefer;
                              if ($scope.server.data_mod.mode === undefined) $scope.server.data_mod.mode = [];
                              $scope.server.data_mod.mode[index] = item.mode;
                              if ($scope.server.data_mod.stratum === undefined) $scope.server.data_mod.stratum = [];
                              $scope.server.data_mod.stratum[index] = item.stratum;
                              if ($scope.server.data_mod.flag1 === undefined) $scope.server.data_mod.flag1 = [];
                              $scope.server.data_mod.flag1[index] = item.flag1;
                              if ($scope.server.data_mod.flag2 === undefined) $scope.server.data_mod.flag2 = [];
                              $scope.server.data_mod.flag2[index] = item.flag2;
                              if ($scope.server.data_mod.flag3 === undefined) $scope.server.data_mod.flag3 = [];
                              $scope.server.data_mod.flag3[index] = item.flag3;
                              if ($scope.server.data_mod.flag4 === undefined) $scope.server.data_mod.flag4 = [];
                              $scope.server.data_mod.flag4[index] = item.flag4;
                          }
                      },

                      submitForm: function (item, index) {
                          var tmpServerArr = [];

                          for(var i=0; i< $scope.serverlist.data.servers.length;i++){
                              if (i !== index)
                                  tmpServerArr.push($scope.serverlist.data.servers[i]);
                              else{
                                  var tmpModData = {
                                      server_addr: $scope.server.data_mod.server_addr[index],
                                      ipv6: $scope.server.data_mod.ipv6[index],
                                      prefer: $scope.server.data_mod.prefer[index],
                                      mode: $scope.server.data_mod.mode[index],
                                      stratum: $scope.server.data_mod.stratum[index],
                                      flag1: $scope.server.data_mod.flag1[index],
                                      flag2: $scope.server.data_mod.flag2[index],
                                      flag3: $scope.server.data_mod.flag3[index],
                                      flag4: $scope.server.data_mod.flag4[index]
                                  };
                                  tmpServerArr.push(tmpModData);

                              }
                          }

                          var postData = tmpServerArr;
                          $scope.server.data_mod.Token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/ntp/server_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.server.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "修改server"+ item.server_addr +"失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.server.data_mod.Token;
                                      tmpMsg.Callback = "modserverCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.server.refresh();
                                  });
                      },

                      modserverCallBack:function (event, msg) {

                      },

                      destroy: function () {
                      }
                  };
              })()

          }
      })();      
      
      $scope.serverlist = (function () {
          return {
              toggle_all: function () {
                  if ($scope.serverlist.checkAllBox === undefined) $scope.serverlist.checkAllBox = false;
                  $scope.serverlist.checkAllBox = !$scope.serverlist.checkAllBox;
                  var nowCheckState = $scope.serverlist.checkAllBox;
                  if ($scope.serverlist.checkbox === undefined) $scope.serverlist.checkbox = [];

                  angular.forEach($scope.serverlist.data.servers, function (item, index, array) {
                      $scope.serverlist.checkbox[index] = nowCheckState;
                  });

              },

              get: function () {//clean input,close add div
                  $scope.server.data_add.clean_data();
                  //$scope.server.addShown = false;
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/utils/ntp/server_list", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.serverlist.data = {};
                              $scope.serverlist.data.servers = response;
                      });
              }


          };
      })();

      $scope.restrict = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.restrictlist.get();
                  return true;
              },

              refresh: function () {
                  angular.forEach($scope.restrictlist.data.servers, function (item, index, array) {
                      if ($scope.restrict.data_mod.bDetailShown !== undefined && $scope.restrict.data_mod.bDetailShown[index] !== undefined)
                          $scope.restrict.data_mod.bDetailShown[index]  = false;
                      if ($scope.restrictlist.checkbox !== undefined
                          && ($scope.restrictlist.checkbox[index] !== undefined ))//push unchecked for submit
                      {
                          $scope.restrictlist.checkbox[index] = false;
                      }
                  });
                  if ($scope.restrictlist !== undefined && $scope.restrictlist.checkAllBox!==undefined)
                      $scope.restrictlist.checkAllBox = false;

                  $scope.restrict.show();
              },

              add: function () {
                  if ($scope.restrict.addShown === undefined) $scope.restrict.addShown = false;
                  $scope.restrict.addShown = !$scope.restrict.addShown;
                  if ($scope.restrict.addShown === true)
                      $scope.restrict.data_add.init();
              },

              delete_all: function () {
                  // $scope.restrict.data.delToken = Math.random();
                  $scope.restrict.data.delArr = [];

                  angular.forEach($scope.restrictlist.data.servers, function (item, index, array) {
                      if ($scope.restrictlist !== undefined && $scope.restrictlist.checkbox !== undefined
                          && ($scope.restrictlist.checkbox[index] === false || $scope.restrictlist.checkbox[index] === undefined))//push unchecked for submit
                      {
                          $scope.restrict.data.delArr.push(item);
                      }
                  });

                  $scope.restrict.data_del($scope.restrict.data.delArr);
              },

              data_del: function (submitArr) {
                  // $scope.restrict.data.delToken = Math.random();
                  var postData = submitArr;

                  $scope.restrict.data_del.token = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/utils/ntp/restrict_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.restrict.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除restrict失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.restrict.data_del.token;
                              tmpMsg.Callback = "delMutirestrictCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.restrict.refresh();
                          });
              },

              delMutirestrictCallBack:function (event, msg) {

              },

              data_add: (function () {
                  return {
                      clean_data: function () {//clean add field
                          if ($scope.restrict.data_add === undefined)
                              $scope.restrict.data_add = {};
                          $scope.restrict.data_add.restrict_addr = "";
                          $scope.restrict.data_add.ipv6 = false;
                          $scope.restrict.data_add.mask = "";
                          $scope.restrict.data_add.ignore = false;
                          $scope.restrict.data_add.nomodify = false;
                          $scope.restrict.data_add.noquery = false;
                          $scope.restrict.data_add.noserve = false;
                          $scope.restrict.data_add.notrap = false;                          
                      },

                      submitForm: function () {//add one restrict
                          var isDuplicate = false;
                          var pushData = {
                              restrict_addr: $scope.restrict.data_add.restrict_addr,
                              ipv6: $scope.restrict.data_add.ipv6,
                              mask: $scope.restrict.data_add.mask,
                              ignore: $scope.restrict.data_add.ignore,
                              nomodify: $scope.restrict.data_add.nomodify,
                              noquery: $scope.restrict.data_add.noquery,
                              noserve: $scope.restrict.data_add.noserve,
                              notrap: $scope.restrict.data_add.notrap
                          };

                          if ($scope.restrictlist.data.servers === undefined)
                              $scope.restrictlist.data.servers = [];

                          angular.forEach($scope.restrictlist.data.servers, function (item, index, array) {
                              if (item.restrict_addr.toString() === $scope.restrict.data_add.restrict_addr.toString())
                              {
                                  isDuplicate = true;
                                  item.restrict_addr = $scope.restrict.data_add.restrict_addr;
                                  item.ipv6 = $scope.restrict.data_add.ipv6;
                                  item.mask = $scope.restrict.data_add.mask;
                                  item.ignore = $scope.restrict.data_add.ignore;
                                  item.nomodify = $scope.restrict.data_add.nomodify;
                                  item.noquery = $scope.restrict.data_add.noquery;
                                  item.noserve = $scope.restrict.data_add.noserve;
                                  item.notrap = $scope.restrict.data_add.notrap;
                              }
                          });

                          if (isDuplicate === false)
                              $scope.restrictlist.data.servers.push(pushData);
                          var postData = $scope.restrictlist.data.servers;

                          $scope.restrict.data_add.token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/ntp/restrict_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.restrict.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "添加restrict失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.restrict.data_add.token;
                                      tmpMsg.Callback = "addrestrictCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.restrict.refresh();
                                  });
                      },

                      close: function () {//clean input,close add div
                          $scope.restrict.data_add.clean_data();
                          $scope.restrict.addShown = false;
                      },

                      init: function () {
                          $scope.restrict.data_add.clean_data();
                      },

                      addrestrictCallBack:function (event, msg) {

                      }
                  };
              })(),

              delete_one: function (item) {
                  var tmpServerArr = [];

                  for(var i=0; i< $scope.restrictlist.data.servers.length;i++){
                      if ($scope.restrictlist.data.servers[i] !== item)
                          tmpServerArr.push($scope.restrictlist.data.servers[i]);
                  }

                  var postData = tmpServerArr;

                  $scope.restrict.data.delOneToken = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/utils/ntp/restrict_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.restrict.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除restrict"+ item +"失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.restrict.data.delOneToken;
                              tmpMsg.Callback = "delrestrictCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.restrict.refresh();
                          });
              },

              delrestrictCallBack:function (event, msg) {

              },

              data: (function () {
                  return {
                      showDetail: function (item, index) {
                          if ($scope.restrict.data_mod.bDetailShown === undefined) $scope.restrict.data_mod.bDetailShown = [];
                          if ($scope.restrict.data_mod.bDetailShown[index] === undefined) $scope.restrict.data_mod.bDetailShown[index] = false;
                          $scope.restrict.data_mod.bDetailShown[index] = !(true === $scope.restrict.data_mod.bDetailShown[index]);
                          if ($scope.restrict.data_mod.bDetailShown[index] === true) {//开
                              $scope.restrict.data_mod.init(item, index);
                          } else {

                          }                      }

                  };
              })(),

              data_mod: (function () {
                  return {
                      init: function (item, index) {
                          if ($scope.restrict.data_mod.bDetailShown[index] === true) {
                              if ($scope.restrict.data_mod.restrict_addr === undefined) $scope.restrict.data_mod.restrict_addr = [];
                              $scope.restrict.data_mod.restrict_addr[index] = item.restrict_addr;
                              if ($scope.restrict.data_mod.ipv6 === undefined) $scope.restrict.data_mod.ipv6 = [];
                              $scope.restrict.data_mod.ipv6[index] = item.ipv6;
                              if ($scope.restrict.data_mod.mask === undefined) $scope.restrict.data_mod.mask = [];
                              $scope.restrict.data_mod.mask[index] = item.mask;
                              if ($scope.restrict.data_mod.ignore === undefined) $scope.restrict.data_mod.ignore = [];
                              $scope.restrict.data_mod.ignore[index] = item.ignore;
                              if ($scope.restrict.data_mod.nomodify === undefined) $scope.restrict.data_mod.nomodify = [];
                              $scope.restrict.data_mod.nomodify[index] = item.nomodify;
                              if ($scope.restrict.data_mod.noquery === undefined) $scope.restrict.data_mod.noquery = [];
                              $scope.restrict.data_mod.noquery[index] = item.noquery;
                              if ($scope.restrict.data_mod.noserve === undefined) $scope.restrict.data_mod.noserve = [];
                              $scope.restrict.data_mod.noserve[index] = item.noserve;
                              if ($scope.restrict.data_mod.notrap === undefined) $scope.restrict.data_mod.notrap = [];
                              $scope.restrict.data_mod.notrap[index] = item.notrap;
                          }
                      },

                      submitForm: function (item, index) {
                          var tmpServerArr = [];

                          for(var i=0; i< $scope.restrictlist.data.servers.length;i++){
                              if (i !== index)
                                  tmpServerArr.push($scope.restrictlist.data.servers[i]);
                              else{
                                  var tmpModData = {
                                      restrict_addr: $scope.restrict.data_mod.restrict_addr[index],
                                      ipv6: $scope.restrict.data_mod.ipv6[index],
                                      mask: $scope.restrict.data_mod.mask[index],
                                      ignore: $scope.restrict.data_mod.ignore[index],
                                      nomodify: $scope.restrict.data_mod.nomodify[index],
                                      noquery: $scope.restrict.data_mod.noquery[index],
                                      noserve: $scope.restrict.data_mod.noserve[index],
                                      notrap: $scope.restrict.data_mod.notrap[index]
                                  };
                                  tmpServerArr.push(tmpModData);

                              }
                          }

                          var postData = tmpServerArr;

                          $scope.restrict.data_mod.Token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/ntp/restrict_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.restrict.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "修改restrict"+ item.restrict_addr +"失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.restrict.data_mod.Token;
                                      tmpMsg.Callback = "modrestrictCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.restrict.refresh();
                                  });
                      },

                      modrestrictCallBack:function (event, msg) {

                      },

                      destroy: function () {
                      }
                  };
              })()

          }
      })();

      $scope.restrictlist = (function () {
          return {
              toggle_all: function () {
                  if ($scope.restrictlist.checkAllBox === undefined) $scope.restrictlist.checkAllBox = false;
                  $scope.restrictlist.checkAllBox = !$scope.restrictlist.checkAllBox;
                  var nowCheckState = $scope.restrictlist.checkAllBox;
                  if ($scope.restrictlist.checkbox === undefined) $scope.restrictlist.checkbox = [];

                  angular.forEach($scope.restrictlist.data.servers, function (item, index, array) {
                      $scope.restrictlist.checkbox[index] = nowCheckState;
                  });

              },

              get: function () {//clean input,close add div
                  $scope.restrict.data_add.clean_data();
                  //$scope.restrict.addShown = false;
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/utils/ntp/restrict_list", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.restrictlist.data = {};
                              $scope.restrictlist.data.servers = response;
                          });
              }


          };
      })();

      $scope.peer = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.peerlist.get();
                  return true;
              },

              refresh: function () {
                  $scope.peer.show();
              }
          }
      })();

      $scope.peerlist = (function () {
          return {
              get: function () {
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/utils/ntp/peer_list", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.peerlist.data = response;
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
      $scope.$on('modserverCallBack', $scope.server.data_mod.modserverCallBack);
      $scope.$on('addserverCallBack', $scope.server.data_add.addserverCallBack);
      $scope.$on('delserverCallBack', $scope.server.delserverCallBack);
      $scope.$on('delMutiserverCallBack', $scope.server.delMutiserverCallBack);
      $scope.$on('modrestrictCallBack', $scope.restrict.data_mod.modrestrictCallBack);
      $scope.$on('addrestrictCallBack', $scope.restrict.data_add.addrestrictCallBack);
      $scope.$on('delrestrictCallBack', $scope.restrict.delrestrictCallBack);
      $scope.$on('delMutirestrictCallBack', $scope.restrict.delMutirestrictCallBack);







//init page data
/*
      var serverlist = (function () {
          return {
              init: function () {
                  $scope.destroy();
                  $scope.data.get();
                  return true;
              },

              destroy: function () {
              }
          };
      })();

      serverlist.init();
      */
  }]);
