(function(){
    controllers.controller('SystemInfo', ['$scope', '$http', function($scope, $http){
        $scope.selectOverview = function(){
            $http.get("/storlever/api/v1/system/localhost")
                .success(function(response) {
                    $scope.localhost = response;
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