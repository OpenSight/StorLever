(function(){
    controllers.controller('SystemInfo', ['$scope', '$http', '$q', function($scope, $http, $q){
        $scope.overview = (function(){
            return {
                cpu: {
                    series: ['Usage'],
                    labels: ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    data: [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
                    options:{
                        pointDot: false,
                        animation: false
                    }
                },
                memory: {
                    labels: ['Usage', 'Free'],
                    data: [100, 0],
                    options:{
                        pointDot: false,
                        animation: false
                    }
                },
                show: function() {
                    $scope.distory();
                    $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/system/localhost", {
                        timeout: $scope.aborter.promise
                    }).success(function(response) {
                        $scope.localhost = response;
                    });
                    $http.get("/storlever/api/v1/system/selinux", {
                        timeout: $scope.aborter.promise
                    }).success(function(response) {
                        $scope.selinux = response;
                    });
                    $http.get("/storlever/api/v1/system/cpu_list", {
                        timeout: $scope.aborter.promise
                    }).success(function(response) {
                        $scope.cpulist = response;
                    });

                    $http.get("/storlever/api/v1/system/cpu_list", {
                        timeout: $scope.aborter.promise
                    }).success(function(response) {
                        $scope.cpulist = response;
                    });
                    $scope.overview.startGetCPUTimes();
                    $scope.overview.getMemory();
                },
                saveHostname: function(){
                    $http.put("/storlever/api/v1/system/localhost", {
                        timeout: $scope.aborter.promise
                    }, JSON.stringify($scope.localhost));
                },
                setSELinuxState: function(state){
                    $http.put("/storlever/api/v1/system/selinux", {
                        timeout: $scope.aborter.promise
                    }, JSON.stringify({state: state}));
                },
                startGetCPUTimes: function(){
                    if (undefined !== $scope.overview.cpu.timer){
                        return;
                    }

                    $scope.overview.cpu.timer = window.setInterval(function(){
                        $scope.overview.getCPUTimes();
                    }, 1000);
                    // $scope.overview.getCPUTimes();
                    return;
                },
                getCPUTimes: function(){
                    if (undefined !== $scope.overview.cpu.aborter){
                        return;
                    }
                    $scope.overview.cpu.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/system/cpu_times", {
                        timeout: $scope.overview.cpu.aborter.promise
                    }).success(function(response) {
                        delete $scope.overview.cpu.aborter;
                        if (undefined === $scope.overview.cpu.pre) {
                            $scope.overview.cpu.pre = response;
                            return;
                        }
                        var present = $scope.overview.getCPUPrecent(response, $scope.overview.cpu.pre);

                        $scope.overview.cpu.data[0].push(present);
                        if (61 <= $scope.overview.cpu.data[0].length) {
                            $scope.overview.cpu.data[0].shift();
                        }
                        $scope.overview.cpu.pre = response;
                    }).error(function(){
                        delete $scope.overview.cpu.aborter;
                    });
                },
                getCPUPrecent: function(c, p){
                    var totle = 0, idle = 0;
                    for (var key in c){
                        totle += c[key] - p[key];
                    }
                    idle = c.idle - p.idle;
                    return Math.round((totle - idle) * 10000/ totle) / 100;
                },
                getMemory: function(){
                    $http.get("/storlever/api/v1/system/memory", {
                        timeout: $scope.aborter.promise
                    }).success(function(response) {
                        $scope.overview.memory.data[0] = Math.round(response.percent * 100) / 100;
                        $scope.overview.memory.data[1] = 100 - $scope.overview.memory.data[0];
                    });
                },
                releaseMemory: function(){
                    $http.post('/storlever/api/v1/system/flush_page_cache', {
                        timeout: $scope.aborter.promise
                    }).success(function(){
                        $scope.overview.getMemory();
                    });
                },
                distory: function(){
                    if (undefined !== $scope.overview.cpu.timer){
                        window.clearInterval($scope.overview.cpu.timer);
                        delete $scope.overview.cpu.timer;
                    }

                    if (undefined !== $scope.overview.cpu.aborter){
                        $scope.overview.cpu.resolve();
                        delete $scope.overview.cpu.aborter;
                    }

                    if (undefined !== $scope.aborter){
                        $scope.aborter.resolve();
                        delete $scope.aborter;
                    }
                }
            };
        })();

        $scope.config = function(){
            return {
                datetime:{
                    date:'',
                    time:'',
                    zone:'',
                    opened: false
                },
                show: function(){
                    $scope.distory();
                    $scope.aborter = $q.defer(),
                    $http.get("/storlever/api/v1/system/datetime", {
                        timeout: $scope.aborter.promise
                    }).success(function(response) {
                        $scope.datetime = response.datetime;
                        $scope.config.datetime.date = response.datetime.match(/[\d-]{10}/)[0];
                        $scope.config.datetime.time = response.datetime.match(/[\d:]{8}/)[0];
                        $scope.config.datetime.zone = response.datetime.match(/[+-][\d]{4}/)[0];
                    });
                },
                openDatepicker: function($event){
                    $event.preventDefault();
                    $event.stopPropagation();
                    $scope.datetime.opened = true;
                }
            };
        };
        $scope.selectMaintain = function(){
            alert('selectMaintain');
        };

        $scope.distory = function(){
            $scope.overview.distory();
            if (undefined !== $scope.aborter){
                    $scope.aborter.resolve();
                    delete $scope.aborter;
            }
        };
    }]);
})()