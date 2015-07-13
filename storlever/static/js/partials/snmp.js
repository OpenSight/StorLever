app.register.controller('Snmp', ['$scope', 'SnmpFac',
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




(function() {
    'use strict';

    /* Services */


    // Demonstrate how to register services
    // In this case it is a simple value service.
    angular.module('app.services').factory('SnmpRes', function($resource) {
        return $resource('../rest/snmp.php/:id'); // Note the full endpoint address
    });
})();