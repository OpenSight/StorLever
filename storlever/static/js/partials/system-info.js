(function(){
    controllers.controller('SystemInfo', ['$scope', '$http', function($scope, $http){
        $scope.selectOverview = function(){
            $http.get("/storlever/api/v1/system/localhost").success(function(response) {
                $scope.localhost = response;
            });
            $http.get("/storlever/api/v1/system/cpu_list").success(function(response) {
                $scope.cpulist = response;
            });
        };
        $scope.selectConfig = function(){
            alert('selectConfig');
        };
        $scope.selectMaintain = function(){
            alert('selectMaintain');
        };
    }]);
})()