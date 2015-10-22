  app.register.controller('SystemInfo', ['$scope', '$http', '$q', function($scope, $http, $q){
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
          labels: ['已占用', '空闲', '缓存'],
          data: [100, 0, 0],
          options:{
            pointDot: false,
            animation: false,
            showTooltips: true,
            tooltipTemplate: '<%if (label){%><%=label%>: <%}%><%= value %>%'
          }
        },
        show: function() {
          $scope.destroy();
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
          // $scope.overview.startGetCPUTimes();
          $scope.overview.startTimer();
          // $scope.overview.getMemory();
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
        startTimer: function(){
          if (undefined !== $scope.overview.timer){
            return;
          }
          $scope.overview.timer = window.setInterval(function(){
            $scope.overview.getCPUTimes();
            $scope.overview.getMemory();
          }, 1000);
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
          $scope.overview.cpu.aborter = $q.defer();
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
          if (undefined !== $scope.overview.memory.aborter){
            return;
          }
          $scope.overview.memory.aborter = $q.defer();
          $http.get("/storlever/api/v1/system/memory", {
            timeout: $scope.overview.memory.aborter.promise
          }).success(function(response) {
            delete $scope.overview.memory.aborter;
            $scope.overview.memory.total = response.total;
            $scope.overview.memory.free = response.free;
            $scope.overview.memory.cached = response.cached + response.buffers;
            $scope.overview.memory.used = response.used - response.cached - response.buffers;
            $scope.overview.memory.data[0] = Math.round($scope.overview.memory.used * 10000 / response.total) / 100;
            $scope.overview.memory.data[1] = Math.round($scope.overview.memory.free * 10000 / response.total) / 100;
            $scope.overview.memory.data[2] = Math.round((100 - $scope.overview.memory.data[0] - $scope.overview.memory.data[1]) * 100) / 100;
          }).error(function(){
            delete $scope.overview.memory.aborter;
          });
        },
        releaseMemory: function(){
          $http.post('/storlever/api/v1/system/flush_page_cache', {
            timeout: $scope.aborter.promise
          }).success(function(){
            $scope.overview.getMemory();
          });
        },
        destroy: function(){
          if (undefined !== $scope.overview.timer){
            window.clearInterval($scope.overview.timer);
            delete $scope.overview.timer;
          }

          if (undefined !== $scope.overview.cpu.aborter){
            $scope.overview.cpu.resolve();
            delete $scope.overview.cpu.aborter;
          }

          if (undefined !== $scope.overview.memory.aborter){
            $scope.overview.memory.resolve();
            delete $scope.overview.memory.aborter;
          }

          if (undefined !== $scope.aborter){
            $scope.aborter.resolve();
            delete $scope.aborter;
          }
        }
      };
    })();

    $scope.config = (function() {
      return {
        datetime: {
          date: '',
          time: '',
          zone: '',
          opened: true
        },

        show: function() {
          $scope.destroy();
          
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
        open: function($event) {
          $event.preventDefault();
          $event.stopPropagation();
          $scope.config.datetime.opened = true;
        }
      };
    })();

    $scope.config.passwd = (function() {
      return {
        submitForm: function() {
            if ($scope.config.passwd.old === undefined || $scope.config.passwd.old === "" ||
                $scope.config.passwd.new === undefined || $scope.config.passwd.new ==="" || $scope.config.passwd.new.length < 6) {
                return;
            }
            var postData = {
                login: "admin",
                old_password: sjcl.codec.hex.fromBits(sjcl.misc.pbkdf2($scope.config.passwd.old, "OpenSight2013")),
                new_password: sjcl.codec.hex.fromBits(sjcl.misc.pbkdf2($scope.config.passwd.new, "OpenSight2013"))
            };
            $scope.destroy();
            $scope.aborter = $q.defer(),
                $http.post("/storlever/api/v1/system/web_password",  postData, {
                    timeout: $scope.aborter.promise
                    }).success(function(response) {
                        $scope.config.passwd.submitFinished = true;
                        $scope.config.passwd.submitSucceed = true;
                    }).error(function (response) {
                        $scope.config.passwd.submitFinished = true;
                        $scope.config.passwd.submitSucceed = false;
                    });
        }
      };
    })();



      $scope.maintain = (function() {
      return {
        datetime: {
          date: '',
          time: '',
          zone: '',
          opened: false
        },
        show: function() {
          $scope.destroy();
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
        openDatepicker: function($event) {
          $event.preventDefault();
          $event.stopPropagation();
          $scope.datetime.opened = true;
        }
      };
    })();

    $scope.destroy = function(){
      $scope.overview.destroy();
      if (undefined !== $scope.aborter){
          $scope.aborter.resolve();
          delete $scope.aborter;
      }
    };

    $scope.$on('$destroy', $scope.destroy);
  }]);
