var controllers = (function() {
    'use strict';
    /* Controllers */

    return angular.module('app.controllers', []).controller('MyCtrl', ['$scope',
        function($scope) {

        }
    ]).controller('MenuList', ['$scope', 'MenuListFac', 
        function($scope, MenuListFac) {
            $scope.roots = MenuListFac.get();

            $scope.activeNode = function(id, $event){
                $scope.activeInfo = MenuListFac.activeNode(id);
                if (undefined !== $event){
                    $event.stopPropagation();
                }
                return false;
            };

            $scope.activeNode($scope.roots[0].node_id);
            $scope.inited = true;

            $scope.$on("Ctr1NameChange",
                 function (event, msg) {
                         console.log("parent", msg);
                         $scope.$broadcast("Ctr1NameChangeFromParrent", msg);
                 }
            );

            $scope.$on("Ctr1ModalShow",
                function (event, errMsg) {
                    $scope.gModal = {};

                    $scope.gModal.Label = errMsg.Label;
                    $scope.gModal.ErrorContent = errMsg.ErrorContent;
                    $scope.gModal.ErrorContentDetail = JSON.stringify(errMsg.ErrorContentDetail, null, "\t");
                    $scope.gModal.DetailShown = false;
                    $scope.gModal.SingleButtonShown = errMsg.SingleButtonShown;
                    $scope.gModal.MutiButtonShown = errMsg.MutiButtonShown;
                    $scope.gModal.Token = errMsg.Token;
                    $scope.gModal.Callback = errMsg.Callback;

                    $scope.gModal.goOn = function () {
                        var tmpMsg = {};
                        tmpMsg.Token = $scope.gModal.Token;
                        tmpMsg.Stop = false;
                        $scope.$broadcast($scope.gModal.Callback, tmpMsg);
                        $('#myErrorModal').modal('hide');
                    };
                    $scope.gModal.stop = function () {
                        var tmpMsg = {};
                        tmpMsg.Token = $scope.gModal.Token;
                        tmpMsg.Stop = true;
                        $scope.$broadcast($scope.gModal.Callback, tmpMsg);
                        $('#myErrorModal').modal('hide');
                    };

                    $('#myErrorModal').modal();
                }
            );
        }
    ]);
})();

