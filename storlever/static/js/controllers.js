(function() {
    'use strict';
    /* Controllers */
    angular.module('app.controllers', []).controller('MyCtrl', ['$scope',
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
        }
    ]);
})();