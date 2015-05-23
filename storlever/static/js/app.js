(function(){
    'use strict';

    $.ajax({
        async: false,
        dataType: 'json',
        url: '/menu_list',
        success: function(d){
            window.menuList = d;
        }
    });

    var setRoute = function($routeProvider, list){
        for (var i = 0, l = list.length; i < l; i++){
            if ('leaf' === list[i].node_type && '' !== list[i].uri){
                $routeProvider.when('/' + list[i].node_id, {
                    templateUrl: list[i].uri,
                    controller: 'MyCtrl'
                });
            } else {
                setRoute($routeProvider, list[i].sub_nodes);
            }
        }
        $routeProvider.otherwise({
            redirectTo: '/' + menuList[0].sub_nodes[0].sub_nodes[0].node_id
        });
        return true;
    };

    var app = angular.module('app', [
        'ngRoute',
        'app.filters',
        'app.services',
        'app.directives',
        'app.controllers',
        'ui.bootstrap',
        'chart.js'
        // ,
        // 'isteven-multi-select'
    ]).config(['$routeProvider',
        function($routeProvider) {
            setRoute($routeProvider, window.menuList);
        }
    ]);
})();
