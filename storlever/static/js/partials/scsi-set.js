app.register.controller('Scsi', ['$scope', '$http', '$q', function($scope, $http, $q){
    $scope.scan = (function () {
        return {
            show: function () {
                $scope.destroy();
                $scope.scan.data_add.clean_data();
                return true;
            },

            data_add: (function () {
                return {
                    clean_data: function () {//clean add field
                        if ($scope.scan.data_add === undefined)
                            $scope.scan.data_add = {};
                        $scope.scan.data_add.host = "";
                        $scope.scan.data_add.channels = "";
                        $scope.scan.data_add.targets = "";
                        $scope.scan.data_add.luns = "";
                        $scope.scan.data_add.remove = false;
                        $scope.scan.data_add.force_rescan = false;
                        $scope.scan.data_add.force_remove = false;
                    },

                    submitForm: function () {//add one scan
                        var postData = {
                            opt: "re_scan",
                            host: $scope.scan.data_add.host,
                            channels: $scope.scan.data_add.channels,
                            targets: $scope.scan.data_add.targets,
                            luns: $scope.scan.data_add.luns,
                            remove: $scope.scan.data_add.remove,
                            force_rescan: $scope.scan.data_add.force_rescan,
                            force_remove: $scope.scan.data_add.force_remove
                        };

                        $scope.scan.data_add.token = Math.random();
                        $scope.aborter = $q.defer(),
                            $http.put("/storlever/api/v1/block/scsi/scan_bus", postData, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {

                                }).error(function (response) {
                                    var tmpMsg = {};
                                    tmpMsg.Label = "错误";
                                    tmpMsg.ErrorContent = "rescan失败";
                                    tmpMsg.ErrorContentDetail = response;
                                    tmpMsg.SingleButtonShown = true;
                                    tmpMsg.MutiButtonShown = false;
                                    tmpMsg.Token =  $scope.scan.data_add.token;
                                    tmpMsg.Callback = "addscanCallBack";
                                    $scope.$emit("Ctr1ModalShow", tmpMsg);
                                });
                    },

                    init: function () {
                        $scope.scan.data_add.clean_data();
                    },

                    addscanCallBack:function (event, msg) {

                    }
                };
            })()
        }
    })();

    $scope.dev = (function () {
        return {
            show: function () {
                $scope.destroy();
                $scope.devlist.get();
                return true;
            },

            refresh: function () {
                angular.forEach($scope.devlist.data.servers, function (item, index, array) {
                    if ($scope.dev.data_mod.bDetailShown !== undefined && $scope.dev.data_mod.bDetailShown[index] !== undefined)
                        $scope.dev.data_mod.bDetailShown[index]  = false;                    
                });                
                $scope.dev.show();
            },     

            data: (function () {
                return {
                    showDetail: function (item, index) {
                        if ($scope.dev.data_mod.bDetailShown === undefined) $scope.dev.data_mod.bDetailShown = [];
                        if ($scope.dev.data_mod.bDetailShown[index] === undefined) $scope.dev.data_mod.bDetailShown[index] = false;
                        $scope.dev.data_mod.bDetailShown[index] = !(true === $scope.dev.data_mod.bDetailShown[index]);
                        if ($scope.dev.data_mod.bDetailShown[index] === true) {//开
                            $scope.dev.data_mod.init(item, index);
                        } else {

                        }                      }

                };
            })(),

            data_mod: (function () {
                return {
                    init: function (item, index) {
                        if ($scope.dev.data_mod.bDetailShown[index] === true) {
                            if ($scope.dev.data_mod.scsi_id === undefined) $scope.dev.data_mod.scsi_id = [];
                            $scope.dev.data_mod.scsi_id[index] = item.scsi_id;
                            if ($scope.dev.data_mod.scsi_type === undefined) $scope.dev.data_mod.scsi_type = [];
                            $scope.dev.data_mod.scsi_type[index] = item.scsi_type;
                            if ($scope.dev.data_mod.dev_file === undefined) $scope.dev.data_mod.dev_file = [];
                            $scope.dev.data_mod.dev_file[index] = item.dev_file;
                            if ($scope.dev.data_mod.sg_file === undefined) $scope.dev.data_mod.sg_file = [];
                            $scope.dev.data_mod.sg_file[index] = item.sg_file;
                            if ($scope.dev.data_mod.vendor === undefined) $scope.dev.data_mod.vendor = [];
                            $scope.dev.data_mod.vendor[index] = item.vendor;
                            if ($scope.dev.data_mod.model === undefined) $scope.dev.data_mod.model = [];
                            $scope.dev.data_mod.model[index] = item.model;
                            if ($scope.dev.data_mod.rev === undefined) $scope.dev.data_mod.rev = [];
                            $scope.dev.data_mod.rev[index] = item.rev;
                            if ($scope.dev.data_mod.state === undefined) $scope.dev.data_mod.state = [];
                            $scope.dev.data_mod.state[index] = item.state;
                            $scope.dev.data_mod.getSmartInfo(item, index);
                        }
                    },


                    getSmartInfo: function (item, index) {
                        if ($scope.dev.data_mod.smart === undefined) $scope.dev.data_mod.smart = [];
                        $scope.dev.data_mod.smart[index] = false;
                        if ($scope.dev.data_mod.offline_auto === undefined) $scope.dev.data_mod.offline_auto = [];
                        $scope.dev.data_mod.offline_auto[index] = false;
                        if ($scope.dev.data_mod.detail === undefined) $scope.dev.data_mod.detail = [];
                        $scope.dev.data_mod.detail[index] = "";

                        $scope.aborter = $q.defer(),
                            $http.get("/storlever/api/v1/block/scsi/dev_list/"+item.scsi_id+"/smart", {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                $scope.dev.data_mod.smart[index] = response.smart;
                                $scope.dev.data_mod.offline_auto[index] = response.offline_auto;
                                $scope.dev.data_mod.detail[index] = response.detail;
                            });
                    },

                    submitForm: function (item, index) {
                        var postData = {
                            smart:$scope.dev.data_mod.smart[index],
                            offline_auto: $scope.dev.data_mod.offline_auto[index]
                        };

                        $scope.dev.data_mod.submitForm.Token = Math.random();
                        $scope.aborter = $q.defer(),
                            $http.put("/storlever/api/v1/block/scsi/dev_list/"+item.scsi_id+"/smart", postData, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                    $scope.dev.refresh();
                                }).error(function (response) {
                                    var tmpMsg = {};
                                    tmpMsg.Label = "错误";
                                    tmpMsg.ErrorContent = "修改"+ $scope.dev.data_mod.scsi_id[index] +"smart信息失败";
                                    tmpMsg.ErrorContentDetail = response;
                                    tmpMsg.SingleButtonShown = true;
                                    tmpMsg.MutiButtonShown = false;
                                    tmpMsg.Token =  $scope.dev.data_mod.submitForm.Token;
                                    tmpMsg.Callback = "modBlockCallBack";
                                    $scope.$emit("Ctr1ModalShow", tmpMsg);
                                    $scope.dev.refresh();
                                });
                    },

                    modBlockCallBack:function (event, msg) {

                    },

                    destroy: function () {
                    }
                };
            })()

        }
    })();

    $scope.devlist = (function () {
        return {
            get: function () {//clean input,close add div
                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/block/scsi/dev_list", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.devlist.data = {};
                            $scope.devlist.data.servers = response;
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
                $scope.host.show();
            }
        }
    })();

    $scope.hostlist = (function () {
        return {
            get: function () {
                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/block/scsi/host_list", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.hostlist.data = {};
                            $scope.hostlist.data.servers = response;
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
    
    $scope.$on('addscanCallBack', $scope.scan.data_add.addscanCallBack);
    $scope.$on('modBlockCallBack', $scope.dev.data_mod.modBlockCallBack);

}]);
