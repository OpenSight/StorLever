app.register.controller('Block', ['$scope', '$http', '$q', function($scope, $http, $q){
    $scope.block = (function () {
        return {
            show: function () {
                $scope.destroy();
                $scope.blocklist.get();
                return true;
            },

            refresh: function () {
                angular.forEach($scope.blocklist.data.servers, function (item, index, array) {
                    if ($scope.block.data_mod.bDetailShown !== undefined && $scope.block.data_mod.bDetailShown[index] !== undefined)
                        $scope.block.data_mod.bDetailShown[index]  = false;                    
                });                
                $scope.block.show();
            },     

            data: (function () {
                return {
                    showDetail: function (item, index) {
                        if ($scope.block.data_mod.bDetailShown === undefined) $scope.block.data_mod.bDetailShown = [];
                        if ($scope.block.data_mod.bDetailShown[index] === undefined) $scope.block.data_mod.bDetailShown[index] = false;
                        $scope.block.data_mod.bDetailShown[index] = !(true === $scope.block.data_mod.bDetailShown[index]);
                        if ($scope.block.data_mod.bDetailShown[index] === true) {//开
                            $scope.block.data_mod.init(item, index);
                        } else {

                        }                      }

                };
            })(),

            data_mod: (function () {
                return {
                    init: function (item, index) {
                        if ($scope.block.data_mod.bDetailShown[index] === true) {
                            if ($scope.block.data_mod.name === undefined) $scope.block.data_mod.name = [];
                            $scope.block.data_mod.name[index] = item.name;
                            if ($scope.block.data_mod.major === undefined) $scope.block.data_mod.major = [];
                            $scope.block.data_mod.major[index] = item.major;
                            if ($scope.block.data_mod.minor === undefined) $scope.block.data_mod.minor = [];
                            $scope.block.data_mod.minor[index] = item.minor;
                            if ($scope.block.data_mod.size === undefined) $scope.block.data_mod.size = [];
                            $scope.block.data_mod.size[index] = item.size;
                            if ($scope.block.data_mod.fs_type === undefined) $scope.block.data_mod.fs_type = [];
                            $scope.block.data_mod.fs_type[index] = item.fs_type;
                            if ($scope.block.data_mod.type === undefined) $scope.block.data_mod.type = [];
                            $scope.block.data_mod.type[index] = item.type;
                            if ($scope.block.data_mod.mount_point === undefined) $scope.block.data_mod.mount_point = [];
                            $scope.block.data_mod.mount_point[index] = item.mount_point;
                            if ($scope.block.data_mod.read_only === undefined) $scope.block.data_mod.read_only = [];
                            $scope.block.data_mod.read_only[index] = item.read_only;
                        }
                    },

                    clean_meta: function (item, index) {
                        var postData = {
                            opt: "clean_meta"
                        };

                        $scope.block.data_mod.clean_meta.Token = Math.random();
                        $scope.aborter = $q.defer(),
                            $http.put("/storlever/api/v1/block/block_list/"+$scope.block.data_mod.name[index], postData, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                    $scope.block.refresh();
                                }).error(function (response) {
                                    var tmpMsg = {};
                                    tmpMsg.Label = "错误";
                                    tmpMsg.ErrorContent = "clean_meta block"+ $scope.block.data_mod.name[index] +"失败";
                                    tmpMsg.ErrorContentDetail = response;
                                    tmpMsg.SingleButtonShown = true;
                                    tmpMsg.MutiButtonShown = false;
                                    tmpMsg.Token =  $scope.block.data_mod.clean_meta.Token;
                                    tmpMsg.Callback = "clean_metaBlockCallBack";
                                    $scope.$emit("Ctr1ModalShow", tmpMsg);
                                    $scope.block.refresh();
                                });
                    },

                    clean_metaBlockCallBack:function (event, msg) {

                    },

                    flush_buf: function (item, index) {
                        var postData = {
                            opt: "flush_buf"
                        };

                        $scope.block.data_mod.flush_buf.Token = Math.random();
                        $scope.aborter = $q.defer(),
                            $http.put("/storlever/api/v1/block/block_list/"+$scope.block.data_mod.name[index], postData, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                    $scope.block.refresh();
                                }).error(function (response) {
                                    var tmpMsg = {};
                                    tmpMsg.Label = "错误";
                                    tmpMsg.ErrorContent = "flush_buf block"+ $scope.block.data_mod.name[index] +"失败";
                                    tmpMsg.ErrorContentDetail = response;
                                    tmpMsg.SingleButtonShown = true;
                                    tmpMsg.MutiButtonShown = false;
                                    tmpMsg.Token =  $scope.block.data_mod.flush_buf.Token;
                                    tmpMsg.Callback = "flush_bufBlockCallBack";
                                    $scope.$emit("Ctr1ModalShow", tmpMsg);
                                    $scope.block.refresh();
                                });
                    },

                    flush_bufBlockCallBack:function (event, msg) {

                    },

                    destroy: function () {
                    }
                };
            })()

        }
    })();

    $scope.blocklist = (function () {
        return {
            get: function () {//clean input,close add div
                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/block/block_list", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.blocklist.data = {};
                            $scope.blocklist.data.servers = response;
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

    $scope.block.show();

    $scope.$on('$destroy', $scope.destroy);

//add all callback
    
    $scope.$on('flush_bufBlockCallBack', $scope.block.data_mod.flush_bufBlockCallBack);
    $scope.$on('clean_metaBlockCallBack', $scope.block.data_mod.clean_metaBlockCallBack);

}]);
