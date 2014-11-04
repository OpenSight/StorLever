(function(){
    controllers.controller('SystemInfo', ['$scope', '$http', '$q', function($scope, $http, $q){
        $scope.overview = (function(){
            return {
                show: function() {
                    $scope.distory();
                    
                    $http.get("/storlever/api/v1/system/localhost").success(function(response) {
                        $scope.localhost = response;
                    });
                    $http.get("/storlever/api/v1/system/selinux").success(function(response) {
                        $scope.selinux = response;
                    });
                    $http.get("/storlever/api/v1/system/cpu_list").success(function(response) {
                        $scope.cpulist = response;
                    });

                    $http.get("/storlever/api/v1/system/cpu_list").success(function(response) {
                        $scope.cpulist = response;
                    });

                    $scope.overview.startGetCPUTimes();
                    $scope.overview.getMemory();
                },
                cpu: {
                    series: ['Usage'],
                    labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    data: [[0,0,0,0,0,0,0,0,0,0,0]],
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
                        if (11 <= $scope.overview.cpu.data[0].length) {
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
                    $http.get("/storlever/api/v1/system/memory").success(function(response) {
                        $scope.overview.memory.data[0] = Math.round(response.percent * 100) / 100;
                        $scope.overview.memory.data[1] = 100 - $scope.overview.memory.data[0];
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
                }
            };
        })();

        $scope.selectConfig = function(){
            alert('selectConfig');
        };
        $scope.selectMaintain = function(){
            alert('selectMaintain');
        };

        $scope.distory = function(){
            $scope.overview.distory();
        };
    }]);
})()