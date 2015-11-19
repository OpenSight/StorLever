  app.register.controller('Mail', ['$scope', '$http', '$q', function($scope, $http, $q){
      $scope.mailConf = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.mailConf.get();
                  return true;
              },

              data_add: (function () {
                  return {
                      clean_data: function () {//clean add field
                          if ($scope.mailConf.data_add === undefined)
                              $scope.mailConf.data_add = {};
                          $scope.mailConf.data_add.email_addr = "";
                          $scope.mailConf.data_add.smtp_server = "";
                          $scope.mailConf.data_add.password = "";
                      },

                      submitForm: function () {//add one mailConf
                          var putData = {
                              email_addr: $scope.mailConf.data_add.email_addr,
                              smtp_server: $scope.mailConf.data_add.smtp_server,
                              password: $scope.mailConf.data_add.password
                          };

                          $scope.mailConf.data_add.token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.put("/storlever/api/v1/utils/mail/conf", putData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {

                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "设置mail失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.mailConf.data_add.token;
                                      tmpMsg.Callback = "addmailConfCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.mailConf.show();
                                  });
                      },

                      init: function () {
                          $scope.mailConf.data_add.clean_data();
                      },

                      addmailConfCallBack:function (event, msg) {

                      }
                  };
              })(),

              get: function () {//clean input,get new
                  $scope.mailConf.data_add.clean_data();
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/utils/mail/conf", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.mailConf.data_add.email_addr = response.email_addr;
                              $scope.mailConf.data_add.smtp_server = response.smtp_server;
                              $scope.mailConf.data_add.password = response.password;
                          });
              }
          }
      })();

      $scope.mailSend = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.mailSend.data_add.clean_data();
                  return true;
              },

              data_add: (function () {
                  return {
                      clean_data: function () {//clean add field
                          if ($scope.mailSend.data_add === undefined)
                              $scope.mailSend.data_add = {};
                          $scope.mailSend.data_add.to = "";
                          $scope.mailSend.data_add.subject = "";
                          $scope.mailSend.data_add.content = "";
                          $scope.mailSend.data_add.debug = false;
                      },

                      submitForm: function () {//add one mailSend
                          var postData = {
                              to: $scope.mailSend.data_add.to,
                              subject: $scope.mailSend.data_add.subject,
                              content: $scope.mailSend.data_add.content,
                              debug: $scope.mailSend.data_add.debug
                          };

                          $scope.mailSend.data_add.token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.post("/storlever/api/v1/utils/mail/send_mail", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {

                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "发送mail失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.mailSend.data_add.token;
                                      tmpMsg.Callback = "addmailSendCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                  });
                      },

                      init: function () {
                          $scope.mailSend.data_add.clean_data();
                      },

                      addmailSendCallBack:function (event, msg) {

                      }
                  };
              })()
          }
      })();

      $scope.destroy = function () {
          if (undefined !== $scope.aborter) {
              $scope.aborter.resolve();
              delete $scope.aborter;
          }
      };

      $scope.$on('$destroy', $scope.destroy);

//add all callback
      $scope.$on('addmailConfCallBack', $scope.mailConf.data_add.addmailConfCallBack);
      $scope.$on('addmailSendCallBack', $scope.mailSend.data_add.addmailSendCallBack);

  }]);
