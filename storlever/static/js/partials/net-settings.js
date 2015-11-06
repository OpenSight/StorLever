  app.register.controller('NetSettings', ['$scope', '$http', '$q', function($scope, $http, $q){
      $scope.dns = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.dnslist.get();
                  return true;
              },
              
              refresh: function () {
                  if ($scope.dns.data_mod.bDetailShown !== undefined)
                      angular.forEach($scope.dnslist.data.servers, function (item, index, array) {
                          $scope.dns.data_mod.bDetailShown[item]  = false;
                      });
                  $scope.dns.show();
              },
              
              add: function () {
                  if ($scope.dns.addShown === undefined) $scope.dns.addShown = false;
                  $scope.dns.addShown = !$scope.dns.addShown;
                  if ($scope.dns.addShown === true)
                      $scope.dns.data_add.init();
              },
              
              delete_all: function () {
                 // $scope.dns.data.delToken = Math.random();
                  $scope.dns.data.delArr = [];

                  angular.forEach($scope.dnslist.data.servers, function (item, index, array) {
                      if ($scope.dnslist !== undefined && $scope.dnslist.checkbox !== undefined
                          && ($scope.dnslist.checkbox[item] === false || $scope.dnslist.checkbox[item] === undefined))//push unchecked for submit
                      {
                        $scope.dns.data.delArr.push(item);
                      }
                  });

                  $scope.dns.data_del($scope.dns.data.delArr);
              },

              data_del: function (submitArr) {
                  // $scope.dns.data.delToken = Math.random();
                  var postData = {
                      servers: submitArr
                  };

                  $scope.dns.data_del.token = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/network/dns", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.dns.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除dns失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.dns.data_del.token;
                              tmpMsg.Callback = "delMutiDnsCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.dns.refresh();
                          });
              },

              delMutiDnsCallBack:function (event, msg) {

              },

              data_add: (function () {
                  return {
                      clean_data: function () {//clean add field
                          if ($scope.dns.data_add === undefined)
                              $scope.dns.data_add = {};
                          $scope.dns.data_add.server = "";
                      },

                      submitForm: function () {//add one dns
                          if ($scope.dns.data_add.server === "")
                          {
                             // return;
                          }else{
                              $scope.dnslist.data.servers.push($scope.dns.data_add.server);
                          }

                          var postData = {
                              servers: $scope.dnslist.data.servers
                          };

                          $scope.dns.data_add.token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/network/dns", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.dns.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "添加dns失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.dns.data_add.token;
                                      tmpMsg.Callback = "addDnsCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.dns.refresh();
                                  });
                      },

                      close: function () {//clean input,close add div
                          $scope.dns.data_add.clean_data();
                          $scope.dns.addShown = false;
                      },

                      init: function () {
                          $scope.dns.data_add.clean_data();
                      },

                      addDnsCallBack:function (event, msg) {

                      }
                  };
              })(),

              delete_one: function (item) {
                  var tmpServerArr = [];

                  for(var i=0; i< $scope.dnslist.data.servers.length;i++){
                      if ($scope.dnslist.data.servers[i] !== item)
                          tmpServerArr.push($scope.dnslist.data.servers[i]);
                  }

                  var postData = {
                      servers: tmpServerArr
                  };

                  $scope.dns.data.delOneToken = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/network/dns", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.dns.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除dns"+ item +"失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.dns.data.delOneToken;
                              tmpMsg.Callback = "delDnsCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.dns.refresh();
                          });
              },

              delDnsCallBack:function (event, msg) {

              },

              data: (function () {
                  return {
                      showDetail: function (item) {
                          if ($scope.dns.data_mod.bDetailShown === undefined) $scope.dns.data_mod.bDetailShown = [];
                          if ($scope.dns.data_mod.bDetailShown[item] === undefined) $scope.dns.data_mod.bDetailShown[item] = false;
                          $scope.dns.data_mod.bDetailShown[item] = !(true === $scope.dns.data_mod.bDetailShown[item]);
                          if ($scope.dns.data_mod.bDetailShown[item] === true) {//开
                              $scope.dns.data_mod.init(item);
                          } else {
                              
                          }
                      }
                  };
              })(),

              data_mod: (function () {
                  return {
                      init: function (item) {
                          if ($scope.dns.data_mod.bDetailShown[item] === true) {
                              if ($scope.dns.data_mod.server === undefined) $scope.dns.data_mod.server = [];
                              $scope.dns.data_mod.server[item] = item;
                          }
                      },

                      submitForm: function (item) {
                          var tmpServerArr = [];

                          for(var i=0; i< $scope.dnslist.data.servers.length;i++){
                              if ($scope.dnslist.data.servers[i] !== item)
                                 tmpServerArr.push($scope.dnslist.data.servers[i]);
                              else
                                 tmpServerArr.push($scope.dns.data_mod.server[item]);
                          }

                          var postData = {
                              servers: tmpServerArr
                          };

                          $scope.dns.data_mod.Token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/network/dns", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.dns.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "修改dns"+ item +"失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.dns.data_mod.Token;
                                      tmpMsg.Callback = "modDnsCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.dns.refresh();
                                  });
                      },

                      modDnsCallBack:function (event, msg) {

                      },

                      destroy: function () {
                      }
                  };
              })()

          }
      })();      
      
      $scope.dnslist = (function () {
          return {
              toggle_all: function () {
                  if ($scope.dnslist.checkAllBox === undefined) $scope.dnslist.checkAllBox = false;
                  $scope.dnslist.checkAllBox = !$scope.dnslist.checkAllBox;
                  var nowCheckState = $scope.dnslist.checkAllBox;
                  if ($scope.dnslist.checkbox === undefined) $scope.dnslist.checkbox = [];

                  angular.forEach($scope.dnslist.data.servers, function (item, index, array) {
                      $scope.dnslist.checkbox[item] = nowCheckState;
                  });

              },

              get: function () {//clean input,close add div
                  $scope.dns.data_add.clean_data();
                  //$scope.dns.addShown = false;
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/network/dns", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.dnslist.data = response;
                      });
              }


          };
      })();

      $scope.host = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.hostlist.get();
                  return true;
              },

              refresh: function () {
                  if ($scope.host.data_mod.bDetailShown !== undefined)
                      angular.forEach($scope.hostlist.data.servers, function (item, index, array) {
                          $scope.host.data_mod.bDetailShown[item]  = false;
                      });
                  $scope.host.show();
              },

              add: function () {
                  if ($scope.host.addShown === undefined) $scope.host.addShown = false;
                  $scope.host.addShown = !$scope.host.addShown;
                  if ($scope.host.addShown === true)
                      $scope.host.data_add.init();
              },

              delete_all: function () {
                  // $scope.host.data.delToken = Math.random();
                  $scope.host.data.delArr = [];

                  angular.forEach($scope.hostlist.data.servers, function (item, index, array) {
                      if ($scope.hostlist !== undefined && $scope.hostlist.checkbox !== undefined
                          && ($scope.hostlist.checkbox[item] === false || $scope.hostlist.checkbox[item] === undefined))//push unchecked for submit
                      {
                          $scope.host.data.delArr.push(item);
                      }
                  });

                  $scope.host.data_del($scope.host.data.delArr);
              },

              data_del: function (submitArr) {
                  // $scope.host.data.delToken = Math.random();
                  var postData = {
                      servers: submitArr
                  };

                  $scope.host.data_del.token = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/network/host_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.host.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除host失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.host.data_del.token;
                              tmpMsg.Callback = "delMutihostCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.host.refresh();
                          });
              },

              delMutihostCallBack:function (event, msg) {

              },

              data_add: (function () {
                  return {
                      clean_data: function () {//clean add field
                          if ($scope.host.data_add === undefined)
                              $scope.host.data_add = {};
                          $scope.host.data_add.addr = "";
                          $scope.host.data_add.hostname = "";
                          $scope.host.data_add.alias = "";
                      },

                      submitForm: function () {//add one host
                          var pushData = {
                              addr: $scope.host.data_add.addr,
                              hostname: $scope.host.data_add.hostname,
                              alias: $scope.host.data_add.alias
                          };

                          if ($scope.hostlist.data.servers === undefined)
                              $scope.hostlist.data.servers = [];
                          $scope.hostlist.data.servers.push(pushData);


                          var postData = $scope.hostlist.data.servers;


                          $scope.host.data_add.token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/network/host_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.host.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "添加host失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.host.data_add.token;
                                      tmpMsg.Callback = "addhostCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.host.refresh();
                                  });
                      },

                      close: function () {//clean input,close add div
                          $scope.host.data_add.clean_data();
                          $scope.host.addShown = false;
                      },

                      init: function () {
                          $scope.host.data_add.clean_data();
                      },

                      addhostCallBack:function (event, msg) {

                      }
                  };
              })(),

              delete_one: function (item) {
                  var tmpServerArr = [];

                  for(var i=0; i< $scope.hostlist.data.servers.length;i++){
                      if ($scope.hostlist.data.servers[i] !== item)
                          tmpServerArr.push($scope.hostlist.data.servers[i]);
                  }

                  var postData = {
                      servers: tmpServerArr
                  };

                  $scope.host.data.delOneToken = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/network/host_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.host.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除host"+ item +"失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.host.data.delOneToken;
                              tmpMsg.Callback = "delhostCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.host.refresh();
                          });
              },

              delhostCallBack:function (event, msg) {

              },

              data: (function () {
                  return {
                      showDetail: function (item) {
                          if ($scope.host.data_mod.bDetailShown === undefined) $scope.host.data_mod.bDetailShown = [];
                          if ($scope.host.data_mod.bDetailShown[item] === undefined) $scope.host.data_mod.bDetailShown[item] = false;
                          $scope.host.data_mod.bDetailShown[item] = !(true === $scope.host.data_mod.bDetailShown[item]);
                          if ($scope.host.data_mod.bDetailShown[item] === true) {//开
                              $scope.host.data_mod.init(item);
                          } else {

                          }
                      }
                  };
              })(),

              data_mod: (function () {
                  return {
                      init: function (item) {
                          if ($scope.host.data_mod.bDetailShown[item] === true) {
                              if ($scope.host.data_mod.server === undefined) $scope.host.data_mod.server = [];
                              $scope.host.data_mod.server[item] = item;
                          }
                      },

                      submitForm: function (item) {
                          var tmpServerArr = [];

                          for(var i=0; i< $scope.hostlist.data.servers.length;i++){
                              if ($scope.hostlist.data.servers[i] !== item)
                                  tmpServerArr.push($scope.hostlist.data.servers[i]);
                              else
                                  tmpServerArr.push($scope.host.data_mod.server[item]);
                          }

                          var postData = {
                              servers: tmpServerArr
                          };

                          $scope.host.data_mod.Token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/network/host_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.host.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "修改host"+ item +"失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.host.data_mod.Token;
                                      tmpMsg.Callback = "modhostCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.host.refresh();
                                  });
                      },

                      modhostCallBack:function (event, msg) {

                      },

                      destroy: function () {
                      }
                  };
              })()

          }
      })();

      $scope.hostlist = (function () {
          return {
              toggle_all: function () {
                  if ($scope.hostlist.checkAllBox === undefined) $scope.hostlist.checkAllBox = false;
                  $scope.hostlist.checkAllBox = !$scope.hostlist.checkAllBox;
                  var nowCheckState = $scope.hostlist.checkAllBox;
                  if ($scope.hostlist.checkbox === undefined) $scope.hostlist.checkbox = [];

                  angular.forEach($scope.hostlist.data.servers, function (item, index, array) {
                      $scope.hostlist.checkbox[item] = nowCheckState;
                  });

              },

              get: function () {//clean input,close add div
                  $scope.host.data_add.clean_data();
                  //$scope.host.addShown = false;
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/network/host_list", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.hostlist.data = response;
                          });
              }


          };
      })();

      $scope.router4 = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.router4list.get();
                  return true;
              },

              refresh: function () {
                  $scope.router4.show();
              }
          }
      })();

      $scope.router4list = (function () {
          return {
              get: function () {
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/network/route_tab", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.router4list.data = response;
                          });
              }


          };
      })();

      $scope.router6 = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.router6list.get();
                  return true;
              },

              refresh: function () {
                  $scope.router6.show();
              }
          }
      })();

      $scope.router6list = (function () {
          return {
              get: function () {
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/network/route_tab6", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.router6list.data = response;
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
      $scope.$on('modDnsCallBack', $scope.dns.data_mod.modDnsCallBack);
      $scope.$on('addDnsCallBack', $scope.dns.data_add.addDnsCallBack);
      $scope.$on('delDnsCallBack', $scope.dns.delDnsCallBack);
      $scope.$on('delMutiDnsCallBack', $scope.dns.delMutiDnsCallBack);
      $scope.$on('modHostCallBack', $scope.host.data_mod.modHostCallBack);
      $scope.$on('addHostCallBack', $scope.host.data_add.addHostCallBack);
      $scope.$on('delHostCallBack', $scope.host.delHostCallBack);
      $scope.$on('delMutiHostCallBack', $scope.host.delMutiHostCallBack);







//init page data
/*
      var dnslist = (function () {
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

      dnslist.init();
      */
  }]);
