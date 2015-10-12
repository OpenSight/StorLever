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
            key: "0(balance-rr)",
            value: 0
        },
        {
            key: "1(active-backup)",
            value: 1
        },
        {
            key: "2(balance-xor)",
            value: 2
        },
        {
            key: "3(broadcast)",
            value: 3
        },
        {
            key: "4(802.3ad)",
            value: 4
        },
        {
            key: "5(balance-tlb)",
            value: 5
        },
        {
            key: "6(balance-alb)",
            value: 6
        }
    ];

    $scope.staticData.deleteTask = [];

    $scope.bondlist = (function () {
        return {
            toggle_all: function () {
                if ($scope.bondlist.checkAllBox === undefined) $scope.bondlist.checkAllBox = false;
                $scope.bondlist.checkAllBox = !$scope.bondlist.checkAllBox;
                var nowCheckState = $scope.bondlist.checkAllBox;
                if ($scope.bondlist.checkbox === undefined) $scope.bondlist.checkbox = [];

                angular.forEach($scope.data.bondlist, function (item, index, array) {
                    $scope.bondlist.checkbox[item.name] = nowCheckState;
                });

            }
        };
    })();


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

            delete_one: function (item) {
                $scope.data.delOneToken = Math.random();
                $scope.aborter = $q.defer(),
                    $http.delete("/storlever/api/v1/network/bond/bond_list/"+item.name, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.data.refresh();
                        }).error(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Label = "错误";
                            tmpMsg.ErrorContent = "删除Bond "+item.name+" 失败";
                            tmpMsg.ErrorContentDetail = response;
                            tmpMsg.SingleButtonShown = true;
                            tmpMsg.MutiButtonShown = false;
                            tmpMsg.Token = $scope.data.delOneToken;
                            tmpMsg.Callback = "delOneBondCallBack";
                            $scope.$emit("Ctr1ModalShow", tmpMsg);
                            $scope.data.refresh();
                        });
            },

            delOneBondCallBack:function (event, msg) {

            },

            delete_all: function () {
                $scope.data.delMoreToken = Math.random();
                $scope.data.delArr = [];

//get select
                angular.forEach($scope.data.bondlist, function (item, index, array) {
                    if ($scope.bondlist !== undefined && $scope.bondlist.checkbox !== undefined
                        && $scope.bondlist.checkbox[item.name] === true)
                    {
                        if (item.name === "bond0") $scope.staticData.deleteBond0 = true;
                        else  $scope.data.delArr.push(item.name);
                    }
                });

                var tmpMsg = {};
                tmpMsg.Token = $scope.data.delMoreToken;
                tmpMsg.Stop = false;
                $scope.data.delMoreBondCallBack(null, tmpMsg);
            },

            delMoreBondCallBack:function (event, msg) {
                var tmpDel = null;

                if (msg.Token != $scope.data.delMoreToken || msg.Stop === true) return;
                if ($scope.data.delArr.length > 0){
                    tmpDel = $scope.data.delArr[$scope.data.delArr.length-1];
                    $scope.data.delArr.pop();
                }else if ($scope.staticData.deleteBond0 === true){
                    $scope.staticData.deleteBond0 = false;
                    tmpDel = "bond0";
                }else return;

                $scope.aborter = $q.defer(),
                    $http.delete("/storlever/api/v1/network/bond/bond_list/"+tmpDel, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Token = $scope.data.delMoreToken;
                            tmpMsg.Stop = false;

                            $scope.data.refresh();
                            if ($scope.data.delArr.length > 0 || $scope.staticData.deleteBond0 === true)
                                $scope.data.delMoreBondCallBack(null, tmpMsg);
                            else return;
                        }).error(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Label = "错误";
                            tmpMsg.ErrorContent = "删除Bond "+tmpDel+" 失败";
                            tmpMsg.ErrorContentDetail = response;
                            tmpMsg.SingleButtonShown = true;
                            tmpMsg.MutiButtonShown = false;
                            tmpMsg.Token = $scope.data.delMoreToken;
                            tmpMsg.Callback = "delMoreBondCallBack";

                            var tmpJobCount = 0;
                            tmpJobCount += $scope.data.delArr.length;
                            if ($scope.staticData.deleteBond0 === true)
                                tmpJobCount++;
                            if (tmpJobCount > 0){
                                tmpMsg.ErrorContent = "删除Bond "+tmpDel+" 失败,仍有"+tmpJobCount+"个任务在队列中，是否继续";
                                tmpMsg.SingleButtonShown = false;
                                tmpMsg.MutiButtonShown = true;
                            }

                            $scope.$emit("Ctr1ModalShow", tmpMsg);
                            $scope.data.refresh();
                        });
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
                            $http.get("/storlever/api/v1/network/eth_list/" + item.name, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                    $scope.config.data[item.name].ip = response.ip;
                                    $scope.config.data[item.name].gateway = response.gateway;
                                    $scope.config.data[item.name].netmask = response.netmask;
                            });
                    });
            },

            init: function (item) {
                $scope.config.Token = Math.random();
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
                    mode: $scope.config.data[item.name].mode+""
                };

                $scope.aborter = $q.defer(),
                    $http.put("/storlever/api/v1/network/bond/bond_list/" + $scope.config.data[item.name].name, putData, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.data.refresh();
                    }).error(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Label = "错误";
                            tmpMsg.ErrorContent = "修改bond接口失败";
                            tmpMsg.ErrorContentDetail = response;
                            tmpMsg.SingleButtonShown = true;
                            tmpMsg.MutiButtonShown = false;
                            tmpMsg.Token = $scope.config.Token;
                            tmpMsg.Callback = "modBondCallBack";
                            $scope.$emit("Ctr1ModalShow", tmpMsg);
                    });
            },

            modBondCallBack:function (event, msg) {

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
                $scope.bond.data.ifs = "";
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
                            $scope.data.refresh();
                        }).error(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Label = "错误";
                            tmpMsg.ErrorContent = "添加bond接口失败";
                            tmpMsg.ErrorContentDetail = response;
                            tmpMsg.SingleButtonShown = true;
                            tmpMsg.MutiButtonShown = false;
                            tmpMsg.Token = $scope.bond.Token;
                            tmpMsg.Callback = "addBondCallBack";
                            $scope.$emit("Ctr1ModalShow", tmpMsg);
                        });
            },

            close: function () {//clean input,close add div
               $scope.bond.clean_data();
               $scope.addShown = false;
            },

            init: function () {//get ethlist for choose
                $scope.bond.clean_data();
                $scope.bond.Token = Math.random();

                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/network/eth_list", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.bond.ethInterfaces = response;
                            angular.forEach($scope.bond.ethInterfaces, function (data, index, array) {
                                if (data.is_bond_slave === false && data.is_bond_master === false) {//physical
                                    $scope.bond.phylist.push(data.name);

                                }
                            });
                });
            },

            addBondCallBack:function (event, msg) {

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

    $scope.$on('modBondCallBack', $scope.config.modBondCallBack);
    $scope.$on('addBondCallBack', $scope.bond.addBondCallBack);
    $scope.$on('delOneBondCallBack', $scope.bond.delOneBondCallBack);
    $scope.$on('delMoreBondCallBack', $scope.data.delMoreBondCallBack);

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
