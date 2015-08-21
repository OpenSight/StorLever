/*
 * /network/eth_list
 /network/eth_list/{port_name}
 /network/bond/bond_list
 /network/bond/bond_list/{port_name}
 /network/eth_list/{port_name}/op*/
app.register.controller('Bond', ['$scope', '$http', '$q', function ($scope, $http, $q) {
    $scope.staticData = [];
    $scope.staticData.bondModeOptionsData = [
        {
            key: "balance-rr",
            value: 0
        },
        {
            key: "active-backup",
            value: 1
        },
        {
            key: "balance-xor",
            value: 2
        },
        {
            key: "broadcast",
            value: 3
        },
        {
            key: "802.3ad",
            value: 4
        },
        {
            key: "balance-tlb",
            value: 5
        },
        {
            key: "balance-alb",
            value: 6
        }
    ];

    $scope.data = (function () {
        return {
            get: function () {
                $scope.data.bondlist = undefined;
                $scope.config.data = undefined;

                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/network/bond/bond_list", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.data.bondlist = response;
                        });
            },
            showDetail: function (item) {
                if (item.bDetailShown === undefined) item.bDetailShown = false;
                item.bDetailShown = !(true === item.bDetailShown);
                if (item.bDetailShown === true) {//开
                   $scope.config.init(item);
                } else {
                }
            },
            refresh: function () {
                angular.forEach($scope.data.interfaces, function (item, index, array) {
                    item.bDetailShown = false;
                });
                bondList.init();
            },
            add: function () {
                if ($scope.addShown === undefined) $scope.addShown = false;
                $scope.addShown = !$scope.addShown;
                if ($scope.addShown === true)
                    $scope.bond.init();
            },
            delete: function (item) {
                $scope.data.delete_err_msg = " ";
                $scope.aborter = $q.defer(),
                    $http.delete("/storlever/api/v1/network/bond/bond_list/"+item.name, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {

                    }).error(function (response) {
                            $scope.data.delete_err_msg += (item.name + " ");
                    });

            },
            delete_one: function (item) {
                $scope.data.delete(item);
                if (delete_err_msg.length > 1) alert("删除Bond接口" + $scope.data.delete_err_msg + "失败");
                $scope.data.refresh();
            },
            delete_all: function () {
                angular.forEach($scope.data.bondlist, function (item, index, array) {
                    if ($scope.bondlist !== undefined && $scope.bondlist.checkbox !== undefined
                        && $scope.bondlist.checkbox[item.name] === true)
                        $scope.data.delete(item);
                });
                if (delete_err_msg.length > 1) alert("删除Bond接口" + $scope.data.delete_err_msg + "失败");
               $scope.data.refresh();
            }
        };
    })();

    $scope.config = (function () {
        return {
            get: function (item) {
                if ($scope.config.data === undefined) {
                    $scope.config.data = {};
                }

                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/network/bond/bond_list/" + item.name, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.config.data[item.name] = response;
                            $http.get("/storlever/api/v1/network//eth_list/" + item.name, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                    $scope.config.data[item.name].ip = response.ip;
                                    $scope.config.data[item.name].gateway = response.gateway;
                                    $scope.config.data[item.name].netmask = response.netmask;
                            });
                    });
            },

            init: function (item) {
                if (item.bDetailShown === true) {

                    if (undefined !== $scope.aborter) {
                        $scope.aborter.resolve();
                        delete $scope.aborter;
                    }
                    //初始化重新拿
                    $scope.config.get(item);
                }
            },

            submitForm: function (item) {
                var putData = {
                    miimon: $scope.config.data[item.name].miimon,
                    mode: $scope.config.data[item.name].mode
                };

                $scope.aborter = $q.defer(),
                    $http.put("/storlever/api/v1/network/bond/bond_list/" + $scope.config.data[item.name].name, putData, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {

                    }).error(function (response) {
                            alert("修改bond接口失败！");
                    });
            },

            destroy: function () {
            }
        };
    })();

    $scope.bond = (function () {
        return {
            clean_data: function () {//clean one bond
                if ($scope.bond.data === undefined)
                    $scope.bond.data = {};
                $scope.bond.data.ip = "";
                $scope.bond.data.netmask = "";
                $scope.bond.data.gateway = "";
                $scope.bond.data.mode = 0;
                $scope.bond.data.ifs = "";
                $scope.bond.data.miimon = "";
                $scope.bond.phylist = [];
                $scope.bond.tmpIfs = [];
            },

            submitForm: function (item) {//add one bond
                angular.forEach($scope.bond.phylist, function (data, index, array) {//get choosen physical eth port
                    if ($scope.bond.tmpIfs[data] === true) {
                        if ($scope.bond.data.ifs.length > 0)
                            $scope.bond.data.ifs += ",";
                        $scope.bond.data.ifs += data;
                    }
                });

                var postData = {
                    ip: $scope.bond.data.ip,
                    netmask: $scope.bond.data.netmask,
                    gateway: $scope.bond.data.gateway,
                    mode: $scope.bond.data.mode,
                    miimon: $scope.bond.data.miimon,
                    ifs: $scope.bond.data.ifs
                };

                $scope.aborter = $q.defer(),
                    $http.post("/storlever/api/v1/network/bond/bond_list", postData, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {

                        }).error(function (response) {
                            alert("添加bond接口失败！");
                        });
            },

            close: function () {//clean input,close add div
               $scope.bond.clean_data();
               $scope.addShown = false;
            },

            init: function () {//get ethlist for choose
                $scope.bond.clean_data();

                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/network/eth_list", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.bond.ethInterfaces = response;
                });

                angular.forEach($scope.bond.ethInterfaces, function (data, index, array) {
                    if (data.is_bond_slave === false && data.is_bond_master === false) {//physical
                        $scope.bond.phylist.push(data.name);

                    }
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

    var bondList = (function () {
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

    bondList.init();
}]);
