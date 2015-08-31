var app = angular.module('app', [
    'ngRoute',
    'app.filters',
    'app.services',
    'app.directives',
    'app.controllers',
    'ui.bootstrap',
    'chart.js',
    'angular-loading-bar',
    'ngAnimate'
 //   'isteven-multi-select'
]);

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

    var asyncjs = function (js) {
        return ["$q", "$route", "$rootScope", function ($q, $route, $rootScope) {
            var deferred = $q.defer();
            var dependencies = js;


            $script(dependencies, function () {
                $rootScope.$apply(function () {
                    deferred.resolve();
                });
            });
            return deferred.promise;
        }];
    };

    var setRoute = function($routeProvider, list){
        for (var i = 0, l = list.length; i < l; i++){
            if ('leaf' === list[i].node_type && '' !== list[i].uri){
                $routeProvider.when('/' + list[i].node_id, {
                    templateUrl: list[i].uri,
                    controller: 'MyCtrl',
                    resolve: {
                        load: asyncjs(list[i].require_js)
                    }
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





    app.config(function($controllerProvider, $compileProvider, $filterProvider, $provide, $routeProvider) {
        app.register = {
            controller: $controllerProvider.register,
            directive: $compileProvider.directive,
            filter: $filterProvider.register,
            factory: $provide.factory,
            service: $provide.service
        };

        setRoute($routeProvider, window.menuList);
    });
})();
