  app.register.controller('Md', ['$scope', '$http', '$q', function($scope, $http, $q){
      $scope.staticData = [];
      $scope.staticData.levelOptionsData = [
          {
              key: "raid0",
              value: 0
          },
          {
              key: "raid1",
              value: 1
          },
          {
              key: "raid5",
              value: 5
          },
          {
              key: "raid10",
              value: 10
          },
          {
              key: "raid6",
              value: 6
          }
      ];

      $scope.md = (function () {
          return {
              show: function () {
                  $scope.destroy();
                  $scope.mdlist.get();
                  return true;
              },
              
              refresh: function () {
                  angular.forEach($scope.mdlist.data.servers, function (item, index, array) {
                         if ($scope.md.data_mod.bDetailShown && $scope.md.data_mod.bDetailShown[index] !== undefined)
                          $scope.md.data_mod.bDetailShown[index]  = false;
                  });

                  $scope.md.show();
              },
              
              add: function () {
                  if ($scope.md.addShown === undefined) $scope.md.addShown = false;
                  $scope.md.addShown = !$scope.md.addShown;
                  if ($scope.md.addShown === true)
                      $scope.md.data_add.init();
              },

              data_add: (function () {
                  return {
                      clean_data: function () {//clean add field
                          if ($scope.md.data_add === undefined)
                              $scope.md.data_add = {};
                          $scope.md.data_add.name = "";
                          $scope.md.data_add.level = 1;
                          $scope.md.data_add.dev = "";
                      },

                      submitForm: function () {//add one md
                          var postData = {
                              name: $scope.md.data_add.name,
                              level: $scope.md.data_add.level,
                              dev: $scope.md.data_add.dev
                          };

                          $scope.md.data_add.token = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.post("/storlever/api/v1/block/md_list", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.md.refresh();
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "添加md失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.md.data_add.token;
                                      tmpMsg.Callback = "addMdCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.md.refresh();
                                  });
                      },

                      close: function () {//clean input,close add div
                          //$scope.md.data_add.clean_data();
                          //$scope.md.addShown = false;
                          $scope.md.add();
                      },

                      init: function () {
                          $scope.md.data_add.clean_data();
                      },

                      addMdCallBack:function (event, msg) {

                      }
                  };
              })(),

              delete_one: function (item) {
                  $scope.md.data.delOneToken = Math.random();
                  $scope.aborter = $q.defer(),
                      $http.delete("/storlever/api/v1/block/md_list/"+item.name, {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.md.refresh();
                          }).error(function (response) {
                              var tmpMsg = {};
                              tmpMsg.Label = "错误";
                              tmpMsg.ErrorContent = "删除md"+ item.name +"失败";
                              tmpMsg.ErrorContentDetail = response;
                              tmpMsg.SingleButtonShown = true;
                              tmpMsg.MutiButtonShown = false;
                              tmpMsg.Token =  $scope.md.data.delOneToken;
                              tmpMsg.Callback = "delMdCallBack";
                              $scope.$emit("Ctr1ModalShow", tmpMsg);
                              $scope.md.refresh();
                          });
              },

              delMdCallBack:function (event, msg) {

              },

              data: (function () {
                  return {
                      showDetail: function (item, index) {
                          if ($scope.md.data_mod.bDetailShown === undefined) $scope.md.data_mod.bDetailShown = [];
                          if ($scope.md.data_mod.bDetailShown[index] === undefined) $scope.md.data_mod.bDetailShown[index] = false;
                          $scope.md.data_mod.bDetailShown[index] = !(true === $scope.md.data_mod.bDetailShown[index]);
                          if ($scope.md.data_mod.bDetailShown[index] === true) {//开
                              $scope.md.data_mod.initDetail(item,index);
                          } else {
                              
                          }
                      }
                  };
              })(),

              data_mod: (function () {
                  return {
                      initData: function(item,index) {
                          if ($scope.md.data_mod.bDetailShown[index] === true) {
                              if ($scope.md.data_mod.name === undefined) $scope.md.data_mod.name = [];
                              $scope.md.data_mod.name[index] = item.name;
                              if ($scope.md.data_mod.dev_file === undefined) $scope.md.data_mod.dev_file = [];
                              $scope.md.data_mod.dev_file[index] = item.dev_file;
                              if ($scope.md.data_mod.spare_devices === undefined) $scope.md.data_mod.spare_devices = [];
                              $scope.md.data_mod.spare_devices[index] = item.spare_devices;
                              if ($scope.md.data_mod.array_size === undefined) $scope.md.data_mod.array_size = [];
                              $scope.md.data_mod.array_size[index] = item.array_size;
                              if ($scope.md.data_mod.used_dev_size === undefined) $scope.md.data_mod.used_dev_size = [];
                              $scope.md.data_mod.used_dev_size[index] = item.used_dev_size;
                              if ($scope.md.data_mod.active_device === undefined) $scope.md.data_mod.active_device = [];
                              $scope.md.data_mod.active_device[index] = item.active_device;
                              if ($scope.md.data_mod.total_devices === undefined) $scope.md.data_mod.total_devices = [];
                              $scope.md.data_mod.total_devices[index] = item.total_devices;
                              if ($scope.md.data_mod.creation_time === undefined) $scope.md.data_mod.creation_time = [];
                              $scope.md.data_mod.creation_time[index] = item.creation_time;
                              if ($scope.md.data_mod.raid_level === undefined) $scope.md.data_mod.raid_level = [];
                              $scope.md.data_mod.raid_level[index] = item.raid_level;
                              if ($scope.md.data_mod.update_time === undefined) $scope.md.data_mod.update_time = [];
                              $scope.md.data_mod.update_time[index] = item.update_time;
                              if ($scope.md.data_mod.state === undefined) $scope.md.data_mod.state = [];
                              $scope.md.data_mod.state[index] = item.state;
                              if ($scope.md.data_mod.raid_devices === undefined) $scope.md.data_mod.raid_devices = [];
                              $scope.md.data_mod.raid_devices[index] = item.raid_devices;
                              if ($scope.md.data_mod.full_name === undefined) $scope.md.data_mod.full_name = [];
                              $scope.md.data_mod.full_name[index] = item.full_name;
                              if ($scope.md.data_mod.working_device === undefined) $scope.md.data_mod.working_device = [];
                              $scope.md.data_mod.working_device[index] = item.working_device;
                              if ($scope.md.data_mod.resync_status === undefined) $scope.md.data_mod.resync_status = [];
                              $scope.md.data_mod.resync_status[index] = item.resync_status;
                              if ($scope.md.data_mod.failed_devices === undefined) $scope.md.data_mod.failed_devices = [];
                              $scope.md.data_mod.failed_devices[index] = item.failed_devices;
                              if ($scope.md.data_mod.persistence === undefined) $scope.md.data_mod.persistence = [];
                              $scope.md.data_mod.persistence[index] = item.persistence;
                              if ($scope.md.data_mod.uuid === undefined) $scope.md.data_mod.uuid = [];
                              $scope.md.data_mod.uuid[index] = item.uuid;
                              if ($scope.md.data_mod.members === undefined) $scope.md.data_mod.members = [];
                              $scope.md.data_mod.members[index] = item.members;
                          }
                      },

                      initDetail: function (item, index) {
                          if ($scope.md.data_mod.bDetailShown === undefined
                              || $scope.md.data_mod.bDetailShown[index] === undefined
                              || $scope.md.data_mod.bDetailShown[index] === false)
                            return;

                          $scope.aborter = $q.defer(),
                              $http.get("/storlever/api/v1/block/md_list/"+item.name, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.md.data_mod.initData(response,index);
                                  });
                      },

                      initMembers: function (item, index) {
                          $scope.aborter = $q.defer(),
                              $http.get("/storlever/api/v1/block/md_list/"+item.name, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.md.data_mod.initData(response,index);
                                  });
                      },

                      addHotSp: function (item, index) {
                          var postData =  {
                              dev: $scope.md.data_mod.devs[index],
                              opt: "add"
                              //sum: $scope.md.data_mod.spare_devices[index],
                          };

                          $scope.md.data_mod.addHotSpToken = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.post("/storlever/api/v1/block/md_list/"+item.name+"/op", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.md.data_mod.hotRefresh(item, index);
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "md"+ item.name +"添加热备失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.md.data_mod.addHotSpToken;
                                      tmpMsg.Callback = "modMdCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.md.data_mod.hotRefresh(item, index);
                                  });
                      },

                      delete_one: function (item,device, index) {
                          var postData =  {
                              dev: device,
                              opt: "remove"
                              //sum: $scope.md.data_mod.spare_devices[index],
                          };

                          $scope.md.data_mod.rmHotSpToken = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.post("/storlever/api/v1/block/md_list/"+item.name+"/op", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.md.data_mod.hotRefresh(item, index);
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "md"+ item.name +"删除热备失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.md.data_mod.rmHotSpToken;
                                      tmpMsg.Callback = "modMdCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.md.data_mod.hotRefresh(item, index);
                                  });
                      },

                      hotRefresh: function (item, index) {
                          var postData =  {
                              opt: "refresh"
                              //sum: $scope.md.data_mod.spare_devices[index],
                          };

                          $scope.md.data_mod.freshHotSpToken = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.post("/storlever/api/v1/block/md_list/"+item.name+"/op", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.md.data_mod.initMembers(item, index);
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "md"+ item.name +"刷新失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.md.data_mod.freshHotSpToken;
                                      tmpMsg.Callback = "modMdCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.md.data_mod.initMembers(item, index);
                                  });
                      },

                      grow: function (item, index) {
                          var postData =  {
                              opt: "grow",
                              sum: ""
                          };

                          $scope.md.data_mod.growToken = Math.random();
                          $scope.aborter = $q.defer(),
                              $http.post("/storlever/api/v1/block/md_list/"+item.name+"/op", postData, {
                                  timeout: $scope.aborter.promise
                              }).success(function (response) {
                                      $scope.md.data_mod.hotRefresh(item, index);
                                  }).error(function (response) {
                                      var tmpMsg = {};
                                      tmpMsg.Label = "错误";
                                      tmpMsg.ErrorContent = "md"+ item.name +"刷新失败";
                                      tmpMsg.ErrorContentDetail = response;
                                      tmpMsg.SingleButtonShown = true;
                                      tmpMsg.MutiButtonShown = false;
                                      tmpMsg.Token =  $scope.md.data_mod.growToken;
                                      tmpMsg.Callback = "modMdCallBack";
                                      $scope.$emit("Ctr1ModalShow", tmpMsg);
                                      $scope.md.data_mod.hotRefresh(item, index);
                                  });
                      },

                      hotAdd: function (item, index) {
                          if ($scope.md.data_mod.hotAddShown === undefined) $scope.md.data_mod.hotAddShown = [];
                          if ($scope.md.data_mod.hotAddShown[index] === undefined) $scope.md.data_mod.hotAddShown[index] = false;
                          $scope.md.data_mod.hotAddShown[index] = !$scope.md.data_mod.hotAddShown[index];
                          if ($scope.md.data_mod.hotAddShown[index] === true){
                              $scope.md.data_mod.devs = [];
                              $scope.md.data_mod.devs[index] = "";
                          }

                      },

                      close: function (item,index) {//close add div
                          $scope.md.data_mod.hotAddShown[index] = false;
                      },

                      modMdCallBack:function (event, msg) {

                      },

                      destroy: function () {
                      }
                  };
              })()

          }
      })();      
      
      $scope.mdlist = (function () {
          return {
              get: function () {//clean input,close add div
                  $scope.md.data_add.clean_data();
                  //$scope.md.addShown = false;
                  $scope.aborter = $q.defer(),
                      $http.get("/storlever/api/v1/block/md_list", {
                          timeout: $scope.aborter.promise
                      }).success(function (response) {
                              $scope.mdlist.data = {};
                              $scope.mdlist.data.servers = response;
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
      $scope.$on('modMdCallBack', $scope.md.data_mod.modMdCallBack);
      $scope.$on('addMdCallBack', $scope.md.data_add.addMdCallBack);
      $scope.$on('delMdCallBack', $scope.md.delMdCallBack);

//init md list
      $scope.md.show();


  }]);
