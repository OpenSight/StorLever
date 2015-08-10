/*
 * /network/eth_list
 /network/eth_list/{port_name}
 /network/bond/bond_list
 /network/bond/bond_list/{port_name}
 /network/eth_list/{port_name}/op*/
app.register.controller('Interface', ['$scope', '$http', '$q', function ($scope, $http, $q) {

    $scope.data = (function () {
        return {
            get: function () {
                $scope.data.interfaces = undefined;
                $scope.state.data = undefined;
                $scope.config.data = undefined;

                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/network/eth_list", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.data.interfaces = response;
                        });
            },
            showDetail: function (item) {
                if (item.bDetailShown === undefined) item.bDetailShown = false;
                item.bDetailShown = !(true === item.bDetailShown);
                if (item.bDetailShown === true) {//开
                    if ($scope.state.freshState !== undefined && $scope.state.freshState[item.name] !== undefined && $scope.state.freshState[item.name].pause === true) {
                        $scope.state.init(item);
                    } else
                        $scope.config.init(item);
                } else {
                    //若状态在刷新就关闭
                    if ($scope.state.fresh !== undefined) {
                        angular.forEach($scope.state.fresh, function (data, index, array) {
                            if (data.name === item.name) {
                                if (data.on === true) {
                                    $scope.state.freshState[item.name].pause = true; //为了在行隐藏状态下点击直接展开状态栏继续刷
                                } else $scope.state.freshState[item.name].pause = false;
                                data.on = false;

                            }
                        });
                    }
                }
            },
            refresh: function () {
                angular.forEach($scope.data.interfaces, function (item, index, array) {
                    item.bDetailShown = false;
                });
                ethList.init();
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
                    $http.get("/storlever/api/v1/network/eth_list/" + item.name, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.config.data[item.name] = response;
                            $scope.config.data[item.name].enabled_bf = $scope.config.data[item.name].enabled;
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
                    //若状态在刷新就关闭
                    if ($scope.state.fresh !== undefined) {
                        angular.forEach($scope.state.fresh, function (data, index, array) {
                            if (data.name === item.name) {
                                data.on = false;
                            }
                        });
                    }
                }
            },

            submitForm: function (item) {
                var putData = {
                    ip: $scope.config.data[item.name].ip,
                    netmask: $scope.config.data[item.name].netmask,
                    gateway: $scope.config.data[item.name].gateway
                };

                $scope.aborter = $q.defer(),
                    $http.put("/storlever/api/v1/network/eth_list/" + $scope.config.data[item.name].name, putData, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {

                        }).error(function (response) {
                            alert("修改网络接口失败！");
                        });
//op
                if ($scope.config.data[item.name].enabled_bf !== $scope.config.data[item.name].enabled) {
                    var postData = {
                        opcode: ($scope.config.data[item.name].enabled === true) ? "enable" : "disable"
                    };
                    $scope.aborter = $q.defer(),
                        $http.post("/storlever/api/v1/network/eth_list/" + $scope.config.data[item.name].name + "/op", postData, {
                            timeout: $scope.aborter.promise
                        }).success(function (response) {

                            }).error(function (response) {
                                if ($scope.config.data.enabled === true)
                                    alert("启用网络接口失败！");
                                else alert("停用网络接口失败！");
                            });
                }

            },

            destroy: function () {
            }
        };
    })();

    $scope.state = (function () {
        return {
            get: function (item) {
                if ($scope.state.data === undefined) {
                    $scope.state.data = {};
                }
                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/network/eth_list/" + item.name + "/stat", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.state.data[item.name] = response;
                        });
            },
            init: function (item) {
                if (item.bDetailShown === true) {
                    $scope.destroy();
                    $scope.state.get(item);
                    if ($scope.state.fresh === undefined) {
                        $scope.state.fresh = [];
                    }
                    var found_fresh = false;
                    angular.forEach($scope.state.fresh, function (data, index, array) {
                        if (data.name === item.name) {
                            data.on = true;
                            found_fresh = true;
                        }
                    });
                    if (found_fresh === false) {
                        var tmpItem = {
                            name: item.name,
                            on: true
                        };
                        $scope.state.fresh.push(tmpItem);
                    }

                    $scope.state.startTimer();
                }
            },
            startTimer: function () {
                if (undefined !== $scope.state.timer) {
                    return;
                }
                $scope.state.timer = window.setInterval(function () {
                    angular.forEach($scope.state.fresh, function (data, index, array) {
                        if (data.on === true) {
                            $scope.state.getFreshState(data);
                        }
                    });
                }, 1000);
            },
            getFreshState: function (item) {
                if ($scope.state.freshState === undefined) {
                    $scope.state.freshState = [];
                }

                if ($scope.state.freshState[item.name] === undefined) {
                    $scope.state.freshState[item.name] = {};
                }

                if (undefined !== $scope.state.freshState[item.name].aborter) {
                    return;
                }
                $scope.state.freshState[item.name].aborter = $q.defer();
                $http.get("/storlever/api/v1/network/eth_list/" + item.name + "/stat", {
                    timeout: $scope.state.freshState[item.name].aborter.promise
                }).success(function (response) {
                        var tmpData = response;
                        if ($scope.state.data[item.name] === undefined ||
                            $scope.state.data[item.name].time === undefined ||
                            tmpData.time === undefined ||
                            tmpData.time - $scope.state.data[item.name].time <= 0) {
                            tmpData.rx_rate = 0;
                            tmpData.tx_rate = 0;
                        } else {
                            if (tmpData.rx_bytes - $scope.state.data[item.name].rx_bytes <= 0) tmpData.rx_rate = 0;
                            else {
                                tmpData.rx_rate =
                                    (tmpData.rx_bytes - $scope.state.data[item.name].rx_bytes) / (tmpData.time - $scope.state.data[item.name].time);
                            }
                            if (tmpData.tx_bytes - $scope.state.data[item.name].tx_bytes <= 0) tmpData.tx_rate = 0;
                            else {
                                tmpData.tx_rate =
                                    (tmpData.tx_bytes - $scope.state.data[item.name].tx_bytes) / (tmpData.time - $scope.state.data[item.name].time);
                            }
                        }
                        $scope.state.data[item.name] = tmpData;
                        delete $scope.state.freshState[item.name].aborter;
                    }).error(function () {
                        delete $scope.state.freshState[item.name].aborter;
                    });
            },
            destroy: function () {
            }
        };
    })();


    $scope.destroy = function () {
        if (undefined !== $scope.aborter) {
            $scope.aborter.resolve();
            delete $scope.aborter;
        }

        if (undefined !== $scope.state.timer) {
            window.clearInterval($scope.state.timer);
            delete $scope.state.timer;
        }
    };

    $scope.$on('$destroy', $scope.destroy);

    var ethList = (function () {
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

    ethList.init();
}]);
