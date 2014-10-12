(function() {
    'use strict';

    /* Services */


    // Demonstrate how to register services
    // In this case it is a simple value service.
    angular.module('app.services', []).value('version', '0.1').factory('MenuListFac', function() {
        var list = window.menuList;

        var activeNode = function(id, lt, activeInfo, index) {
            var bIsFound = false;
            for (var i = 0, l = lt.length; i < l; i++) {
                if (id === lt[i].node_id) {
                    bIsFound = true;
                    activeFirstChildren(lt[i], activeInfo, index + 1);
                } else if (0 !== lt[i].sub_nodes) {
                    bIsFound = activeNode(id, lt[i].sub_nodes, activeInfo, index + 1);
                }
                if (true === bIsFound) {
                    activeInfo[index] = lt[i].node_id;
                    return bIsFound;
                }
            }
            return bIsFound;
        };

        var activeFirstChildren = function(node, activeInfo, index) {
            if (0 === node.sub_nodes.length) {
                return true;
            }
            activeInfo[index] = node.sub_nodes[0].node_id;
            activeFirstChildren(node.sub_nodes[0], activeInfo, index + 1);
            return true;
        };
        return {
            get: function() {
                return list;
            },
            activeNode: function(id) {
                var info = [];
                activeNode(id, list, info, 0);
                return info;
            }
        }
    });
})();