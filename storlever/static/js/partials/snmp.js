app.register.controller('Snmp', ['$scope', '$http', '$q', function($scope, $http, $q){
    $scope.snmpConf = (function () {
        return {
            show: function () {
                $scope.destroy();
                $scope.snmpConf.get();
                return true;
            },

            data_add: (function () {
                return {
                    clean_data: function () {//clean add field
                        if ($scope.snmpConf.data_add === undefined)
                            $scope.snmpConf.data_add = {};
                        $scope.snmpConf.data_add.sys_location = "";
                        $scope.snmpConf.data_add.sys_contact = "";
                        $scope.snmpConf.data_add.sys_name = "";
                        $scope.snmpConf.data_add.agent_address = "";
                        $scope.snmpConf.data_add.iquery_sec_name = "";
                        $scope.snmpConf.data_add.link_up_down_notifications = false;
                        $scope.snmpConf.data_add.default_monitors = false;
                        $scope.snmpConf.data_add.load_max = 0.0;
                        $scope.snmpConf.data_add.swap_min = 0;
                        $scope.snmpConf.data_add.disk_min_percent = 0;
                    },

                    submitForm: function () {//add one snmpConf
                        var putData = {
                            sys_location: $scope.snmpConf.data_add.sys_location,
                            sys_contact: $scope.snmpConf.data_add.sys_contact,
                            sys_name: $scope.snmpConf.data_add.sys_name,
                            agent_address: $scope.snmpConf.data_add.agent_address,
                            iquery_sec_name: $scope.snmpConf.data_add.iquery_sec_name,
                            link_up_down_notifications: $scope.snmpConf.data_add.link_up_down_notifications,
                            default_monitors: $scope.snmpConf.data_add.default_monitors,
                            load_max: $scope.snmpConf.data_add.load_max,
                            swap_min: $scope.snmpConf.data_add.swap_min,
                            disk_min_percent: $scope.snmpConf.data_add.disk_min_percent
                        };

                        $scope.snmpConf.data_add.token = Math.random();
                        $scope.aborter = $q.defer(),
                            $http.put("/storlever/api/v1/utils/snmp_agent/conf", putData, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {

                                }).error(function (response) {
                                    var tmpMsg = {};
                                    tmpMsg.Label = "错误";
                                    tmpMsg.ErrorContent = "设置snmp失败";
                                    tmpMsg.ErrorContentDetail = response;
                                    tmpMsg.SingleButtonShown = true;
                                    tmpMsg.MutiButtonShown = false;
                                    tmpMsg.Token =  $scope.snmpConf.data_add.token;
                                    tmpMsg.Callback = "addSnmpConfCallBack";
                                    $scope.$emit("Ctr1ModalShow", tmpMsg);
                                    $scope.snmpConf.show();
                                });
                    },

                    init: function () {
                        $scope.snmpConf.data_add.clean_data();
                    },

                    addSnmpConfCallBack:function (event, msg) {

                    }
                };
            })(),

            get: function () {//clean input,get new
                $scope.snmpConf.data_add.clean_data();
                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/utils/snmp_agent/conf", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.snmpConf.data_add.sys_location = response.sys_location;
                            $scope.snmpConf.data_add.sys_contact = response.sys_contact;
                            $scope.snmpConf.data_add.sys_name = response.sys_name;
                            $scope.snmpConf.data_add.agent_address = response.agent_address;
                            $scope.snmpConf.data_add.iquery_sec_name = response.iquery_sec_name;
                            $scope.snmpConf.data_add.link_up_down_notifications = response.link_up_down_notifications;
                            $scope.snmpConf.data_add.default_monitors = response.default_monitors;
                            $scope.snmpConf.data_add.load_max = response.load_max;
                            $scope.snmpConf.data_add.swap_min = response.swap_min;;
                            $scope.snmpConf.data_add.disk_min_percent = response.disk_min_percent;
                        });
            }
        }
    })();

    $scope.community = (function () {
        return {
            show: function () {
                $scope.destroy();
                $scope.communitylist.get();
                return true;
            },

            refresh: function () {
                angular.forEach($scope.communitylist.data.servers, function (item, index, array) {
                    if ($scope.community.data_mod.bDetailShown !== undefined && $scope.community.data_mod.bDetailShown[index] !== undefined)
                        $scope.community.data_mod.bDetailShown[index]  = false;
                    if ($scope.communitylist.checkbox !== undefined
                        && ($scope.communitylist.checkbox[index] !== undefined ))//push unchecked for submit
                    {
                        $scope.communitylist.checkbox[index] = false;
                    }
                });
                if ($scope.communitylist !== undefined && $scope.communitylist.checkAllBox!==undefined)
                    $scope.communitylist.checkAllBox = false;

                $scope.community.show();
            },

            add: function () {
                if ($scope.community.addShown === undefined) $scope.community.addShown = false;
                $scope.community.addShown = !$scope.community.addShown;
                if ($scope.community.addShown === true)
                    $scope.community.data_add.init();
            },
            
            
            
            delete_one: function (item) {
                $scope.community.delOneToken = Math.random();
                $scope.aborter = $q.defer(),
                    $http.delete("/storlever/api/v1/utils/snmp_agent/community_list/"+item.community_name, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.community.refresh();
                        }).error(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Label = "错误";
                            tmpMsg.ErrorContent = "删除community "+item.community_name+" 失败";
                            tmpMsg.ErrorContentDetail = response;
                            tmpMsg.SingleButtonShown = true;
                            tmpMsg.MutiButtonShown = false;
                            tmpMsg.Token = $scope.community.delOneToken;
                            tmpMsg.Callback = "delCommunityCallBack";
                            $scope.$emit("Ctr1ModalShow", tmpMsg);
                            $scope.community.refresh();
                        });
            },

            delCommunityCallBack:function (event, msg) {

            },

            delete_all: function () {
                $scope.community.delMoreToken = Math.random();
                $scope.community.delArr = [];

//get select
                angular.forEach($scope.communitylist.data.servers, function (item, index, array) {
                    if ($scope.communitylist !== undefined && $scope.communitylist.checkbox !== undefined
                        && ($scope.communitylist.checkbox[index] === true))//push unchecked for submit
                    {
                        $scope.community.delArr.push(item.community_name);
                    }
                });

                var tmpMsg = {};
                tmpMsg.Token = $scope.community.delMoreToken;
                tmpMsg.Stop = false;
                $scope.community.delMoreCommunityCallBack(null, tmpMsg);
            },

            delMoreCommunityCallBack:function (event, msg) {
                var tmpDel = null;

                if (msg.Token != $scope.community.delMoreToken || msg.Stop === true) return;
                if ($scope.community.delArr.length > 0){
                    tmpDel = $scope.community.delArr[$scope.community.delArr.length-1];
                    $scope.community.delArr.pop();
                }else return;

                $scope.aborter = $q.defer(),
                    $http.delete("/storlever/api/v1/utils/snmp_agent/community_list/"+tmpDel, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Token = $scope.community.delMoreToken;
                            tmpMsg.Stop = false;

                            $scope.community.refresh();
                            if ($scope.community.delArr.length > 0)
                                $scope.community.delMoreCommunityCallBack(null, tmpMsg);
                            else return;
                        }).error(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Label = "错误";
                            tmpMsg.ErrorContent = "删除community "+tmpDel+" 失败";
                            tmpMsg.ErrorContentDetail = response;
                            tmpMsg.SingleButtonShown = true;
                            tmpMsg.MutiButtonShown = false;
                            tmpMsg.Token = $scope.community.delMoreToken;
                            tmpMsg.Callback = "delMoreCommunityCallBack";

                            var tmpJobCount = 0;
                            tmpJobCount += $scope.community.delArr.length;

                            if (tmpJobCount > 0){
                                tmpMsg.ErrorContent = "删除community "+tmpDel+" 失败,仍有"+tmpJobCount+"个任务在队列中，是否继续";
                                tmpMsg.SingleButtonShown = false;
                                tmpMsg.MutiButtonShown = true;
                            }

                            $scope.$emit("Ctr1ModalShow", tmpMsg);
                            $scope.community.refresh();
                        });
            },


            data_add: (function () {
                return {
                    clean_data: function () {//clean add field
                        if ($scope.community.data_add === undefined)
                            $scope.community.data_add = {};
                        $scope.community.data_add.community_name = "";
                        $scope.community.data_add.ipv6 = false;
                        $scope.community.data_add.source = "";
                        $scope.community.data_add.oid = "";
                        $scope.community.data_add.read_only = false;
                    },

                    submitForm: function () {//add one community
                        var postData =  {
                            community_name: $scope.community.data_add.community_name,
                            ipv6: $scope.community.data_add.ipv6,
                            source: $scope.community.data_add.source,
                            oid: $scope.community.data_add.oid,
                            read_only: $scope.community.data_add.read_only
                        };

                        $scope.community.data_add.token = Math.random();
                        $scope.aborter = $q.defer(),
                            $http.post("/storlever/api/v1/utils/snmp_agent/community_list", postData, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                    $scope.community.refresh();
                                }).error(function (response) {
                                    var tmpMsg = {};
                                    tmpMsg.Label = "错误";
                                    tmpMsg.ErrorContent = "添加community失败";
                                    tmpMsg.ErrorContentDetail = response;
                                    tmpMsg.SingleButtonShown = true;
                                    tmpMsg.MutiButtonShown = false;
                                    tmpMsg.Token =  $scope.community.data_add.token;
                                    tmpMsg.Callback = "addCommunityCallBack";
                                    $scope.$emit("Ctr1ModalShow", tmpMsg);
                                    $scope.community.refresh();
                                });
                    },

                    close: function () {//clean input,close add div
                        $scope.community.data_add.clean_data();
                        $scope.community.addShown = false;
                    },

                    init: function () {
                        $scope.community.data_add.clean_data();
                    },

                    addCommunityCallBack:function (event, msg) {

                    }
                };
            })(),            

            data: (function () {
                return {
                    showDetail: function (item, index) {
                        if ($scope.community.data_mod.bDetailShown === undefined) $scope.community.data_mod.bDetailShown = [];
                        if ($scope.community.data_mod.bDetailShown[index] === undefined) $scope.community.data_mod.bDetailShown[index] = false;
                        $scope.community.data_mod.bDetailShown[index] = !(true === $scope.community.data_mod.bDetailShown[index]);
                        if ($scope.community.data_mod.bDetailShown[index] === true) {//开
                            $scope.community.data_mod.init(item, index);
                        } else {

                        }                      }

                };
            })(),

            data_mod: (function () {
                return {
                    init: function (item, index) {
                        if ($scope.community.data_mod.bDetailShown[index] === true) {
                            if ($scope.community.data_mod.community_name === undefined) $scope.community.data_mod.community_name = [];
                            $scope.community.data_mod.community_name[index] = item.community_name;
                            if ($scope.community.data_mod.ipv6 === undefined) $scope.community.data_mod.ipv6 = [];
                            $scope.community.data_mod.ipv6[index] = item.ipv6;
                            if ($scope.community.data_mod.source === undefined) $scope.community.data_mod.source = [];
                            $scope.community.data_mod.source[index] = item.source;
                            if ($scope.community.data_mod.oid === undefined) $scope.community.data_mod.oid = [];
                            $scope.community.data_mod.oid[index] = item.oid;
                            if ($scope.community.data_mod.read_only === undefined) $scope.community.data_mod.read_only = [];
                            $scope.community.data_mod.read_only[index] = item.read_only;
                        }
                    },

                    submitForm: function (item, index) {
                        var postData = {
                            community_name: $scope.community.data_mod.community_name[index],
                            ipv6: $scope.community.data_mod.ipv6[index],
                            source: $scope.community.data_mod.source[index],
                            oid: $scope.community.data_mod.oid[index],
                            read_only: $scope.community.data_mod.read_only[index]
                        };

                        $scope.community.data_mod.Token = Math.random();
                        $scope.aborter = $q.defer(),
                            $http.put("/storlever/api/v1/utils/snmp_agent/community_list/"+$scope.community.data_mod.community_name[index], postData, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                    $scope.community.refresh();
                                }).error(function (response) {
                                    var tmpMsg = {};
                                    tmpMsg.Label = "错误";
                                    tmpMsg.ErrorContent = "修改community"+ $scope.community.data_mod.community_name[index] +"失败";
                                    tmpMsg.ErrorContentDetail = response;
                                    tmpMsg.SingleButtonShown = true;
                                    tmpMsg.MutiButtonShown = false;
                                    tmpMsg.Token =  $scope.community.data_mod.Token;
                                    tmpMsg.Callback = "modCommunityCallBack";
                                    $scope.$emit("Ctr1ModalShow", tmpMsg);
                                    $scope.community.refresh();
                                });
                    },

                    modCommunityCallBack:function (event, msg) {

                    },

                    destroy: function () {
                    }
                };
            })()

        }
    })();

    $scope.communitylist = (function () {
        return {
            toggle_all: function () {
                if ($scope.communitylist.checkAllBox === undefined) $scope.communitylist.checkAllBox = false;
                $scope.communitylist.checkAllBox = !$scope.communitylist.checkAllBox;
                var nowCheckState = $scope.communitylist.checkAllBox;
                if ($scope.communitylist.checkbox === undefined) $scope.communitylist.checkbox = [];

                angular.forEach($scope.communitylist.data.servers, function (item, index, array) {
                    $scope.communitylist.checkbox[index] = nowCheckState;
                });

            },

            get: function () {//clean input,close add div
                $scope.community.data_add.clean_data();
                //$scope.community.addShown = false;
                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/utils/snmp_agent/community_list", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.communitylist.data = {};
                            $scope.communitylist.data.servers = response;
                        });
            }


        };
    })();


    $scope.monitor = (function () {
        return {
            show: function () {
                $scope.destroy();
                $scope.monitorlist.get();
                return true;
            },

            refresh: function () {
                angular.forEach($scope.monitorlist.data.servers, function (item, index, array) {
                    if ($scope.monitor.data_mod.bDetailShown !== undefined && $scope.monitor.data_mod.bDetailShown[index] !== undefined)
                        $scope.monitor.data_mod.bDetailShown[index]  = false;
                    if ($scope.monitorlist.checkbox !== undefined
                        && ($scope.monitorlist.checkbox[index] !== undefined ))//push unchecked for submit
                    {
                        $scope.monitorlist.checkbox[index] = false;
                    }
                });
                if ($scope.monitorlist !== undefined && $scope.monitorlist.checkAllBox!==undefined)
                    $scope.monitorlist.checkAllBox = false;

                $scope.monitor.show();
            },

            add: function () {
                if ($scope.monitor.addShown === undefined) $scope.monitor.addShown = false;
                $scope.monitor.addShown = !$scope.monitor.addShown;
                if ($scope.monitor.addShown === true)
                    $scope.monitor.data_add.init();
            },



            delete_one: function (item) {
                $scope.monitor.delOneToken = Math.random();
                $scope.aborter = $q.defer(),
                    $http.delete("/storlever/api/v1/utils/snmp_agent/monitor_list/"+item.monitor_name, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.monitor.refresh();
                        }).error(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Label = "错误";
                            tmpMsg.ErrorContent = "删除monitor "+item.monitor_name+" 失败";
                            tmpMsg.ErrorContentDetail = response;
                            tmpMsg.SingleButtonShown = true;
                            tmpMsg.MutiButtonShown = false;
                            tmpMsg.Token = $scope.monitor.delOneToken;
                            tmpMsg.Callback = "delMonitorCallBack";
                            $scope.$emit("Ctr1ModalShow", tmpMsg);
                            $scope.monitor.refresh();
                        });
            },

            delMonitorCallBack:function (event, msg) {

            },

            delete_all: function () {
                $scope.monitor.delMoreToken = Math.random();
                $scope.monitor.delArr = [];

//get select
                angular.forEach($scope.monitorlist.data.servers, function (item, index, array) {
                    if ($scope.monitorlist !== undefined && $scope.monitorlist.checkbox !== undefined
                        && ($scope.monitorlist.checkbox[index] === true))//push unchecked for submit
                    {
                        $scope.monitor.delArr.push(item.monitor_name);
                    }
                });

                var tmpMsg = {};
                tmpMsg.Token = $scope.monitor.delMoreToken;
                tmpMsg.Stop = false;
                $scope.monitor.delMoreMonitorCallBack(null, tmpMsg);
            },

            delMoreMonitorCallBack:function (event, msg) {
                var tmpDel = null;

                if (msg.Token != $scope.monitor.delMoreToken || msg.Stop === true) return;
                if ($scope.monitor.delArr.length > 0){
                    tmpDel = $scope.monitor.delArr[$scope.monitor.delArr.length-1];
                    $scope.monitor.delArr.pop();
                }else return;

                $scope.aborter = $q.defer(),
                    $http.delete("/storlever/api/v1/utils/snmp_agent/monitor_list/"+tmpDel, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Token = $scope.monitor.delMoreToken;
                            tmpMsg.Stop = false;

                            $scope.monitor.refresh();
                            if ($scope.monitor.delArr.length > 0)
                                $scope.monitor.delMoreMonitorCallBack(null, tmpMsg);
                            else return;
                        }).error(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Label = "错误";
                            tmpMsg.ErrorContent = "删除monitor "+tmpDel+" 失败";
                            tmpMsg.ErrorContentDetail = response;
                            tmpMsg.SingleButtonShown = true;
                            tmpMsg.MutiButtonShown = false;
                            tmpMsg.Token = $scope.monitor.delMoreToken;
                            tmpMsg.Callback = "delMoreMonitorCallBack";

                            var tmpJobCount = 0;
                            tmpJobCount += $scope.monitor.delArr.length;

                            if (tmpJobCount > 0){
                                tmpMsg.ErrorContent = "删除monitor "+tmpDel+" 失败,仍有"+tmpJobCount+"个任务在队列中，是否继续";
                                tmpMsg.SingleButtonShown = false;
                                tmpMsg.MutiButtonShown = true;
                            }

                            $scope.$emit("Ctr1ModalShow", tmpMsg);
                            $scope.monitor.refresh();
                        });
            },


            data_add: (function () {
                return {
                    clean_data: function () {//clean add field
                        if ($scope.monitor.data_add === undefined)
                            $scope.monitor.data_add = {};
                        $scope.monitor.data_add.monitor_name = "";
                        $scope.monitor.data_add.option = "";
                        $scope.monitor.data_add.expression = "";
                    },

                    submitForm: function () {//add one monitor
                        var postData =  {
                            monitor_name: $scope.monitor.data_add.monitor_name,
                            option: $scope.monitor.data_add.option,
                            expression: $scope.monitor.data_add.expression
                        };

                        $scope.monitor.data_add.token = Math.random();
                        $scope.aborter = $q.defer(),
                            $http.post("/storlever/api/v1/utils/snmp_agent/monitor_list", postData, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                    $scope.monitor.refresh();
                                }).error(function (response) {
                                    var tmpMsg = {};
                                    tmpMsg.Label = "错误";
                                    tmpMsg.ErrorContent = "添加monitor失败";
                                    tmpMsg.ErrorContentDetail = response;
                                    tmpMsg.SingleButtonShown = true;
                                    tmpMsg.MutiButtonShown = false;
                                    tmpMsg.Token =  $scope.monitor.data_add.token;
                                    tmpMsg.Callback = "addMonitorCallBack";
                                    $scope.$emit("Ctr1ModalShow", tmpMsg);
                                    $scope.monitor.refresh();
                                });
                    },

                    close: function () {//clean input,close add div
                        $scope.monitor.data_add.clean_data();
                        $scope.monitor.addShown = false;
                    },

                    init: function () {
                        $scope.monitor.data_add.clean_data();
                    },

                    addMonitorCallBack:function (event, msg) {

                    }
                };
            })(),

            data: (function () {
                return {
                    showDetail: function (item, index) {
                        if ($scope.monitor.data_mod.bDetailShown === undefined) $scope.monitor.data_mod.bDetailShown = [];
                        if ($scope.monitor.data_mod.bDetailShown[index] === undefined) $scope.monitor.data_mod.bDetailShown[index] = false;
                        $scope.monitor.data_mod.bDetailShown[index] = !(true === $scope.monitor.data_mod.bDetailShown[index]);
                        if ($scope.monitor.data_mod.bDetailShown[index] === true) {//开
                            $scope.monitor.data_mod.init(item, index);
                        } else {

                        }                      }

                };
            })(),

            data_mod: (function () {
                return {
                    init: function (item, index) {
                        if ($scope.monitor.data_mod.bDetailShown[index] === true) {
                            if ($scope.monitor.data_mod.monitor_name === undefined) $scope.monitor.data_mod.monitor_name = [];
                            $scope.monitor.data_mod.monitor_name[index] = item.monitor_name;
                            if ($scope.monitor.data_mod.option === undefined) $scope.monitor.data_mod.option = [];
                            $scope.monitor.data_mod.option[index] = item.option;
                            if ($scope.monitor.data_mod.expression === undefined) $scope.monitor.data_mod.expression = [];
                            $scope.monitor.data_mod.expression[index] = item.expression;
                        }
                    },

                    submitForm: function (item, index) {
                        var postData = {
                            monitor_name: $scope.monitor.data_mod.monitor_name[index],
                            option: $scope.monitor.data_mod.option[index],
                            expression: $scope.monitor.data_mod.expression[index]
                        };

                        $scope.monitor.data_mod.Token = Math.random();
                        $scope.aborter = $q.defer(),
                            $http.put("/storlever/api/v1/utils/snmp_agent/monitor_list/"+$scope.monitor.data_mod.monitor_name[index], postData, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                    $scope.monitor.refresh();
                                }).error(function (response) {
                                    var tmpMsg = {};
                                    tmpMsg.Label = "错误";
                                    tmpMsg.ErrorContent = "修改monitor"+ $scope.monitor.data_mod.monitor_name[index] +"失败";
                                    tmpMsg.ErrorContentDetail = response;
                                    tmpMsg.SingleButtonShown = true;
                                    tmpMsg.MutiButtonShown = false;
                                    tmpMsg.Token =  $scope.monitor.data_mod.Token;
                                    tmpMsg.Callback = "modMonitorCallBack";
                                    $scope.$emit("Ctr1ModalShow", tmpMsg);
                                    $scope.monitor.refresh();
                                });
                    },

                    modMonitorCallBack:function (event, msg) {

                    },

                    destroy: function () {
                    }
                };
            })()

        }
    })();

    $scope.monitorlist = (function () {
        return {
            toggle_all: function () {
                if ($scope.monitorlist.checkAllBox === undefined) $scope.monitorlist.checkAllBox = false;
                $scope.monitorlist.checkAllBox = !$scope.monitorlist.checkAllBox;
                var nowCheckState = $scope.monitorlist.checkAllBox;
                if ($scope.monitorlist.checkbox === undefined) $scope.monitorlist.checkbox = [];

                angular.forEach($scope.monitorlist.data.servers, function (item, index, array) {
                    $scope.monitorlist.checkbox[index] = nowCheckState;
                });

            },

            get: function () {//clean input,close add div
                $scope.monitor.data_add.clean_data();
                //$scope.monitor.addShown = false;
                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/utils/snmp_agent/monitor_list", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.monitorlist.data = {};
                            $scope.monitorlist.data.servers = response;
                        });
            }


        };
    })();
    $scope.staticData = {};
    $scope.staticData.trap_sinkModeOptionsData = [
        {
            key: "SNMPv1 TRAPs",
            value: "trap"
        },
        {
            key: "SNMPv2c TRAP2s",
            value: "trap2"
        },
        {
            key: "SNMPv2 INFORM",
            value: "inform"
        }
    ];

    $scope.trap_sink = (function () {
        return {
            show: function () {
                $scope.destroy();
                $scope.trap_sinklist.get();
                return true;
            },

            refresh: function () {
                angular.forEach($scope.trap_sinklist.data.servers, function (item, index, array) {
                    if ($scope.trap_sink.data_mod.bDetailShown !== undefined && $scope.trap_sink.data_mod.bDetailShown[index] !== undefined)
                        $scope.trap_sink.data_mod.bDetailShown[index]  = false;
                    if ($scope.trap_sinklist.checkbox !== undefined
                        && ($scope.trap_sinklist.checkbox[index] !== undefined ))//push unchecked for submit
                    {
                        $scope.trap_sinklist.checkbox[index] = false;
                    }
                });
                if ($scope.trap_sinklist !== undefined && $scope.trap_sinklist.checkAllBox!==undefined)
                    $scope.trap_sinklist.checkAllBox = false;

                $scope.trap_sink.show();
            },

            add: function () {
                if ($scope.trap_sink.addShown === undefined) $scope.trap_sink.addShown = false;
                $scope.trap_sink.addShown = !$scope.trap_sink.addShown;
                if ($scope.trap_sink.addShown === true)
                    $scope.trap_sink.data_add.init();
            },

            delete_all: function () {
                // $scope.trap_sink.data.delToken = Math.random();
                $scope.trap_sink.data.delArr = [];

                angular.forEach($scope.trap_sinklist.data.servers, function (item, index, array) {
                    if ($scope.trap_sinklist !== undefined && $scope.trap_sinklist.checkbox !== undefined
                        && ($scope.trap_sinklist.checkbox[index] === false || $scope.trap_sinklist.checkbox[index] === undefined))//push unchecked for submit
                    {
                        $scope.trap_sink.data.delArr.push(item);
                    }
                });

                $scope.trap_sink.data_del($scope.trap_sink.data.delArr);
            },

            data_del: function (submitArr) {
                // $scope.trap_sink.data.delToken = Math.random();
                var postData = submitArr;

                $scope.trap_sink.data_del.token = Math.random();
                $scope.aborter = $q.defer(),
                    $http.put("/storlever/api/v1/utils/snmp_agent/trap_sink_list", postData, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.trap_sink.refresh();
                        }).error(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Label = "错误";
                            tmpMsg.ErrorContent = "删除trap_sink失败";
                            tmpMsg.ErrorContentDetail = response;
                            tmpMsg.SingleButtonShown = true;
                            tmpMsg.MutiButtonShown = false;
                            tmpMsg.Token =  $scope.trap_sink.data_del.token;
                            tmpMsg.Callback = "delMutiTrap_sinkCallBack";
                            $scope.$emit("Ctr1ModalShow", tmpMsg);
                            $scope.trap_sink.refresh();
                        });
            },

            delMutiTrap_sinkCallBack:function (event, msg) {

            },

            data_add: (function () {
                return {
                    clean_data: function () {//clean add field
                        if ($scope.trap_sink.data_add === undefined)
                            $scope.trap_sink.data_add = {};
                        $scope.trap_sink.data_add.host = "";
                        $scope.trap_sink.data_add.type = "trap";
                        $scope.trap_sink.data_add.community = "public";
                    },

                    submitForm: function () {//add one trap_sink
                        var isDuplicate = false;
                        var pushData =  {
                            host: $scope.trap_sink.data_add.host,
                            type: $scope.trap_sink.data_add.type,
                            community: $scope.trap_sink.data_add.community
                        };


                        if ($scope.trap_sinklist.data.servers === undefined)
                            $scope.trap_sinklist.data.servers = [];

                        angular.forEach($scope.trap_sinklist.data.servers, function (item, index, array) {
                            if (item.host.toString() === $scope.trap_sink.data_add.host.toString())
                            {
                                isDuplicate = true;
                                item.host = $scope.trap_sink.data_add.host;
                                item.type = $scope.trap_sink.data_add.type;
                                item.community = $scope.trap_sink.data_add.community;
                            }
                        });

                        if (isDuplicate === false)
                            $scope.trap_sinklist.data.servers.push(pushData);
                        var postData = $scope.trap_sinklist.data.servers;

                        $scope.trap_sink.data_add.token = Math.random();
                        $scope.aborter = $q.defer(),
                            $http.put("/storlever/api/v1/utils/snmp_agent/trap_sink_list", postData, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                    $scope.trap_sink.refresh();
                                }).error(function (response) {
                                    var tmpMsg = {};
                                    tmpMsg.Label = "错误";
                                    tmpMsg.ErrorContent = "添加trap_sink失败";
                                    tmpMsg.ErrorContentDetail = response;
                                    tmpMsg.SingleButtonShown = true;
                                    tmpMsg.MutiButtonShown = false;
                                    tmpMsg.Token =  $scope.trap_sink.data_add.token;
                                    tmpMsg.Callback = "addtrap_sinkCallBack";
                                    $scope.$emit("Ctr1ModalShow", tmpMsg);
                                    $scope.trap_sink.refresh();
                                });
                    },

                    close: function () {//clean input,close add div
                        $scope.trap_sink.data_add.clean_data();
                        $scope.trap_sink.addShown = false;
                    },

                    init: function () {
                        $scope.trap_sink.data_add.clean_data();
                    },

                    addTrap_sinkCallBack:function (event, msg) {

                    }
                };
            })(),

            delete_one: function (item) {
                var tmpServerArr = [];

                for(var i=0; i< $scope.trap_sinklist.data.servers.length;i++){
                    if ($scope.trap_sinklist.data.servers[i] !== item)
                        tmpServerArr.push($scope.trap_sinklist.data.servers[i]);
                }

                var postData = tmpServerArr;

                $scope.trap_sink.data.delOneToken = Math.random();
                $scope.aborter = $q.defer(),
                    $http.put("/storlever/api/v1/utils/snmp_agent/trap_sink_list", postData, {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.trap_sink.refresh();
                        }).error(function (response) {
                            var tmpMsg = {};
                            tmpMsg.Label = "错误";
                            tmpMsg.ErrorContent = "删除trap_sink"+ item +"失败";
                            tmpMsg.ErrorContentDetail = response;
                            tmpMsg.SingleButtonShown = true;
                            tmpMsg.MutiButtonShown = false;
                            tmpMsg.Token =  $scope.trap_sink.data.delOneToken;
                            tmpMsg.Callback = "delTrap_sinkCallBack";
                            $scope.$emit("Ctr1ModalShow", tmpMsg);
                            $scope.trap_sink.refresh();
                        });
            },

            delTrap_sinkCallBack:function (event, msg) {

            },

            data: (function () {
                return {
                    showDetail: function (item, index) {
                        if ($scope.trap_sink.data_mod.bDetailShown === undefined) $scope.trap_sink.data_mod.bDetailShown = [];
                        if ($scope.trap_sink.data_mod.bDetailShown[index] === undefined) $scope.trap_sink.data_mod.bDetailShown[index] = false;
                        $scope.trap_sink.data_mod.bDetailShown[index] = !(true === $scope.trap_sink.data_mod.bDetailShown[index]);
                        if ($scope.trap_sink.data_mod.bDetailShown[index] === true) {//开
                            $scope.trap_sink.data_mod.init(item, index);
                        } else {

                        }                      }

                };
            })(),

            data_mod: (function () {
                return {
                    init: function (item, index) {
                        if ($scope.trap_sink.data_mod.bDetailShown[index] === true) {
                            if ($scope.trap_sink.data_mod.host === undefined) $scope.trap_sink.data_mod.host = [];
                            $scope.trap_sink.data_mod.host[index] = item.host;
                            if ($scope.trap_sink.data_mod.type === undefined) $scope.trap_sink.data_mod.type = [];
                            $scope.trap_sink.data_mod.type[index] = item.type;
                            if ($scope.trap_sink.data_mod.community === undefined) $scope.trap_sink.data_mod.community = [];
                            $scope.trap_sink.data_mod.community[index] = item.community;
                        }
                    },

                    submitForm: function (item, index) {
                        var tmpServerArr = [];

                        for(var i=0; i< $scope.trap_sinklist.data.servers.length;i++){
                            if (i !== index)
                                tmpServerArr.push($scope.trap_sinklist.data.servers[i]);
                            else{
                                var tmpModData = {
                                    host: $scope.trap_sink.data_mod.host[index],
                                    type: $scope.trap_sink.data_mod.type[index],
                                    community: $scope.trap_sink.data_mod.community[index]
                                };

                                tmpServerArr.push(tmpModData);
                            }
                        }

                        var postData = tmpServerArr;

                        $scope.trap_sink.data_mod.Token = Math.random();
                        $scope.aborter = $q.defer(),
                            $http.put("/storlever/api/v1/utils/snmp_agent/trap_sink_list", postData, {
                                timeout: $scope.aborter.promise
                            }).success(function (response) {
                                    $scope.trap_sink.refresh();
                                }).error(function (response) {
                                    var tmpMsg = {};
                                    tmpMsg.Label = "错误";
                                    tmpMsg.ErrorContent = "修改trap_sink"+ item.host +"失败";
                                    tmpMsg.ErrorContentDetail = response;
                                    tmpMsg.SingleButtonShown = true;
                                    tmpMsg.MutiButtonShown = false;
                                    tmpMsg.Token =  $scope.trap_sink.data_mod.Token;
                                    tmpMsg.Callback = "modTrap_sinkCallBack";
                                    $scope.$emit("Ctr1ModalShow", tmpMsg);
                                    $scope.trap_sink.refresh();
                                });
                    },

                    modTrap_sinkCallBack:function (event, msg) {

                    },

                    destroy: function () {
                    }
                };
            })()

        }
    })();

    $scope.trap_sinklist = (function () {
        return {
            toggle_all: function () {
                if ($scope.trap_sinklist.checkAllBox === undefined) $scope.trap_sinklist.checkAllBox = false;
                $scope.trap_sinklist.checkAllBox = !$scope.trap_sinklist.checkAllBox;
                var nowCheckState = $scope.trap_sinklist.checkAllBox;
                if ($scope.trap_sinklist.checkbox === undefined) $scope.trap_sinklist.checkbox = [];

                angular.forEach($scope.trap_sinklist.data.servers, function (item, index, array) {
                    $scope.trap_sinklist.checkbox[index] = nowCheckState;
                });

            },

            get: function () {//clean input,close add div
                $scope.trap_sink.data_add.clean_data();
                //$scope.trap_sink.addShown = false;
                $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/utils/snmp_agent/trap_sink_list", {
                        timeout: $scope.aborter.promise
                    }).success(function (response) {
                            $scope.trap_sinklist.data = {};
                            $scope.trap_sinklist.data.servers = response;
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
    $scope.$on('addSnmpConfCallBack', $scope.snmpConf.data_add.addSnmpConfCallBack);
    $scope.$on('modCommunityCallBack', $scope.community.data_mod.modCommunityCallBack);
    $scope.$on('addCommunityCallBack', $scope.community.data_add.addCommunityCallBack);
    $scope.$on('delCommunityCallBack', $scope.community.delCommunityCallBack);
    $scope.$on('delMutiCommunityCallBack', $scope.community.delMutiCommunityCallBack);
    $scope.$on('modMonitorCallBack', $scope.monitor.data_mod.modMonitorCallBack);
    $scope.$on('addMonitorCallBack', $scope.monitor.data_add.addMonitorCallBack);
    $scope.$on('delMonitorCallBack', $scope.monitor.delMonitorCallBack);
    $scope.$on('delMutiMonitorCallBack', $scope.monitor.delMutiMonitorCallBack);
    $scope.$on('modTrap_sinkCallBack', $scope.monitor.data_mod.modTrap_sinkCallBack);
    $scope.$on('addTrap_sinkCallBack', $scope.monitor.data_add.addTrap_sinkCallBack);
    $scope.$on('delTrap_sinkCallBack', $scope.monitor.delTrap_sinkCallBack);
    $scope.$on('delMutiTrap_sinkCallBack', $scope.monitor.delMutiTrap_sinkCallBack);


}]);
