  app.register.controller('Smart', ['$scope', '$http', '$q', function($scope, $http, $q){
      $scope.smart = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.smartlist.get();
                  return true;
              },
              
              refresh: function () {
                     angular.forEach($scope.smartlist.data.smarts, function (item, index, array) {
                         if ($scope.smart.data_mod.bDetailShown && $scope.smart.data_mod.bDetailShown[index] !== undefined)
                          $scope.smart.data_mod.bDetailShown[index]  = false;
                         if ($scope.smartlist.checkbox !== undefined
                              && ($scope.smartlist.checkbox[index] !== undefined ))//push unchecked for submit
                         {
                             $scope.smartlist.checkbox[index] = false;
                         }
                      });

                  if ($scope.smartlist !==undefined && $scope.smartlist.checkAllBox!==undefined)
                      $scope.smartlist.checkAllBox = false;
                  $scope.smart.show();
              },
              
              add: function () {
                  if ($scope.smart.addShown === undefined) $scope.smart.addShown = false;
                  $scope.smart.addShown = !$scope.smart.addShown;
                  if ($scope.smart.addShown === true)
                      $scope.smart.data_add.init();
              },
              
              delete_all: function () {
                 // $scope.smart.data.delToken = Math.random();
                  $scope.smart.data.delArr = [];

                  angular.forEach($scope.smartlist.data.smarts, function (item, index, array) {
                      if ($scope.smartlist !== undefined && $scope.smartlist.checkbox !== undefined
                          && ($scope.smartlist.checkbox[index] === false || $scope.smartlist.checkbox[index] === undefined))//push unchecked for submit
                      {
                        $scope.smart.data.delArr.push(item);
                      }
                  });

                  $scope.smart.data_del($scope.smart.data.delArr);
              },

              data_del: function (submitArr) {
                  // $scope.smart.data.delToken = Math.random();
                  var postData =  submitArr;

                  $scope.smart.data_del.token = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/utils/smartd/monitor_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.smart.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除smart失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.smart.data_del.token;
                              tmpMsg.Callback = "delMutismartCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.smart.refresh();
                          });
              },

              delMutismartCallBack:function (event, msg) {

              },

              data_add: (function () {
                  return {
                      clean_data: function () {//clean add field
                          if ($scope.smart.data_add === undefined)
                              $scope.smart.data_add = {};
                          $scope.smart.data_add.dev = "";
                          $scope.smart.data_add.mail_to = "";
                          $scope.smart.data_add.mail_test = false;
                          $scope.smart.data_add.mail_exec = "";
                          $scope.smart.data_add.schedule_regexp = "";
                      },

                      submitForm: function () {//add one smart
                          var isDuplicate = false;
                          var pushData = {
                              dev: $scope.smart.data_add.dev,
                              mail_to: $scope.smart.data_add.mail_to,
                              mail_test: $scope.smart.data_add.mail_test,
                              mail_exec: $scope.smart.data_add.mail_exec,
                              schedule_regexp: $scope.smart.data_add.schedule_regexp
                          };

                          angular.forEach($scope.smartlist.data.smarts, function (item, index, array) {
                                  if (item.dev.toString() === $scope.smart.data_add.dev.toString())
                                  {
                                      isDuplicate = true;
                                      item.dev = $scope.smart.data_add.dev;
                                      item.mail_to = $scope.smart.data_add.mail_to;
                                      item.mail_test = $scope.smart.data_add.mail_test;
                                      item.mail_exec = $scope.smart.data_add.mail_exec;
                                      item.schedule_regexp = $scope.smart.data_add.schedule_regexp;
                                  }
                          });

                          if (isDuplicate === false)
                              $scope.smartlist.data.smarts.push(pushData);


                          var postData = $scope.smartlist.data.smarts;

                          $scope.smart.data_add.token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/smartd/monitor_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.smart.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "添加smart失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.smart.data_add.token;
                                      tmpMsg.Callback = "addsmartCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.smart.refresh();
                                  });
                      },

                      close: function () {//clean input,close add div
                          $scope.smart.data_add.clean_data();
                          $scope.smart.addShown = false;
                      },

                      init: function () {
                          $scope.smart.data_add.clean_data();
                      },

                      addsmartCallBack:function (event, msg) {

                      }
                  };
              })(),

              delete_one: function (item) {
                  var tmpsmartArr = [];

                  for(var i=0; i< $scope.smartlist.data.smarts.length;i++){
                      if ($scope.smartlist.data.smarts[i] !== item)
                          tmpsmartArr.push($scope.smartlist.data.smarts[i]);
                  }

                  var postData =  tmpsmartArr;

                  $scope.smart.data.delOneToken = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.put("/storlever/api/v1/utils/smartd/monitor_list", postData, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.smart.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除smart"+ item.dev +"失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.smart.data.delOneToken;
                              tmpMsg.Callback = "delsmartCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.smart.refresh();
                          });
              },

              delsmartCallBack:function (event, msg) {

              },

              data: (function () {
                  return {
                      showDetail: function (item, index) {
                          if ($scope.smart.data_mod.bDetailShown === undefined) $scope.smart.data_mod.bDetailShown = [];
                          if ($scope.smart.data_mod.bDetailShown[index] === undefined) $scope.smart.data_mod.bDetailShown[index] = false;
                          $scope.smart.data_mod.bDetailShown[index] = !(true === $scope.smart.data_mod.bDetailShown[index]);
                          if ($scope.smart.data_mod.bDetailShown[index] === true) {//开
                              $scope.smart.data_mod.init(item,index);
                          } else {
                              
                          }
                      }
                  };
              })(),

              data_mod: (function () {
                  return {
                      init: function (item, index) {
                          if ($scope.smart.data_mod.bDetailShown[index] === true) {
                              if ($scope.smart.data_mod.dev === undefined) $scope.smart.data_mod.dev = [];
                              $scope.smart.data_mod.dev[index] = item.dev;
                              if ($scope.smart.data_mod.mail_to === undefined) $scope.smart.data_mod.mail_to = [];
                              $scope.smart.data_mod.mail_to[index] = item.mail_to;
                              if ($scope.smart.data_mod.mail_test === undefined) $scope.smart.data_mod.mail_test = [];
                              $scope.smart.data_mod.mail_test[index] = item.mail_test;
                              if ($scope.smart.data_mod.mail_exec === undefined) $scope.smart.data_mod.mail_exec = [];
                              $scope.smart.data_mod.mail_exec[index] = item.mail_exec;
                              if ($scope.smart.data_mod.schedule_regexp === undefined) $scope.smart.data_mod.schedule_regexp = [];
                              $scope.smart.data_mod.schedule_regexp[index] = item.schedule_regexp;
                          }
                      },

                      submitForm: function (item, index) {
                          var tmpsmartArr = [];

                          for(var i=0; i< $scope.smartlist.data.smarts.length;i++){
                              if (i !== index)
                                  tmpsmartArr.push($scope.smartlist.data.smarts[i]);
                              else{
                                  var tmpModData = {
                                      dev: $scope.smart.data_mod.dev[index],
                                      mail_to: $scope.smart.data_mod.mail_to[index],
                                      mail_test: $scope.smart.data_mod.mail_test[index],
                                      mail_exec: $scope.smart.data_mod.mail_exec[index],
                                      schedule_regexp: $scope.smart.data_mod.schedule_regexp[index]
                                  };
                                  tmpsmartArr.push(tmpModData);

                              }
                          }

                          var postData = tmpsmartArr;
                          $scope.smart.data_mod.Token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/smartd/monitor_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.smart.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "修改smart"+ item.dev +"失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.smart.data_mod.Token;
                                      tmpMsg.Callback = "modsmartCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.smart.refresh();
                                  });
                      },

                      modsmartCallBack:function (event, msg) {

                      },

                      destroy: function () {
                      }
                  };
              })()

          }
      })();      
      
      $scope.smartlist = (function () {
          return {
              toggle_all: function () {
                  if ($scope.smartlist.checkAllBox === undefined) $scope.smartlist.checkAllBox = false;
                  $scope.smartlist.checkAllBox = !$scope.smartlist.checkAllBox;
                  var nowCheckState = $scope.smartlist.checkAllBox;
                  if ($scope.smartlist.checkbox === undefined) $scope.smartlist.checkbox = [];

                  angular.forEach($scope.smartlist.data.smarts, function (item, index, array) {
                      $scope.smartlist.checkbox[index] = nowCheckState;
                  });

              },

              get: function () {//clean input,close add div
                  $scope.smart.data_add.clean_data();
                  //$scope.smart.addShown = false;
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/utils/smartd/monitor_list", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.smartlist.data = {};
                              $scope.smartlist.data.smarts = response;
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
      $scope.$on('modsmartCallBack', $scope.smart.data_mod.modsmartCallBack);
      $scope.$on('addsmartCallBack', $scope.smart.data_add.addsmartCallBack);
      $scope.$on('delsmartCallBack', $scope.smart.delsmartCallBack);
      $scope.$on('delMutismartCallBack', $scope.smart.delMutismartCallBack);

      $scope.smart.show();


  }]);
