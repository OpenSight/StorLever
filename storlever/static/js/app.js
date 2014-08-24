/* Simple JavaScript Inheritance
 * By John Resig http://ejohn.org/
 * MIT Licensed.
 */
// Inspired by base2 and Prototype
(function(){
  var initializing = false, fnTest = /xyz/.test(function(){xyz;}) ? /\b_super\b/ : /.*/;
 
  // The base Class implementation (does nothing)
  this.Class = function(){};
 
  // Create a new Class that inherits from this class
  Class.extend = function(prop) {
    var _super = this.prototype;
   
    // Instantiate a base class (but only create the instance,
    // don't run the init constructor)
    initializing = true;
    var prototype = new this();
    initializing = false;
   
    // Copy the properties over onto the new prototype
    for (var name in prop) {
      // Check if we're overwriting an existing function
      prototype[name] = typeof prop[name] == "function" &&
        typeof _super[name] == "function" && fnTest.test(prop[name]) ?
        (function(name, fn){
          return function() {
            var tmp = this._super;
           
            // Add a new ._super() method that is the same method
            // but on the super-class
            this._super = _super[name];
           
            // The method only need to be bound temporarily, so we
            // remove it when we're done executing
            var ret = fn.apply(this, arguments);        
            this._super = tmp;
           
            return ret;
          };
        })(name, prop[name]) :
        prop[name];
    }
   
    // The dummy class constructor
    function Class() {
      // All construction is actually done in the init method
      if ( !initializing && this.init )
        this.init.apply(this, arguments);
    }
   
    // Populate our constructed prototype object
    Class.prototype = prototype;
   
    // Enforce the constructor to be what we expect
    Class.prototype.constructor = Class;
 
    // And make this class extendable
    Class.extend = arguments.callee;
   
    return Class;
  };
})();

var app = angular.module('app',[]);

var MenuList = Class.extend({
    data: [{
        sub_nodes: [{
            sub_nodes: []
        }]
    }],
    prefix: '.menu-list-',
    type: ['root', 'intermediate', 'leaf'],
    activedClass: 'active',
    content: '#contentContainer',
    init: function(){
        _this = this;
        app.controller('MenuList', function($scope, $http) {
            $http.get("/menu_list").success(function(data, status, headers, config) {
                _this.data = data;
                $scope.roots = data;
                // scope.roots = data;
                _this.activeFirstChild(data);
                _this.scope.intermediates = data[0].sub_nodes;
            });
        });

        app.controller('MenuListInter', function($scope, $http) {
            _this.scope = $scope;
            _this.http = $http;
        });

        this.on();
        return this;
    },
    on: function(){
        // var selector = this.prefix + this.type.join(',' + this.prefix);
        $('#menuList').on('click', 'li', this, function(e){
            e.data.active(this);
        });
        $('#menuListIntermediate').on('click', 'li', this, function(e){
            e.data.active(this);
            e.stopPropagation();
        });
        return this;
    },
    active: function(el){
        var id = $(el).attr('id');
        var node = this.findNode(id, this.data);
        if (null === node){
            return this;
        }
        // if ('root' === node.node_type){
        //     this.scope.intermediates = node.sub_nodes;
        // }        

        var cls = this.prefix + node.node_type;
        $(this.prefix + node.node_type).removeClass(this.activedClass);
        $(el).addClass(this.activedClass);

        this.laod(node).activeFirstChild(node.sub_nodes);

        return this;
    },
    activeRoot: function(el){

    },
    activeFirstChild: function(nodes){
        if (0 === nodes.length){
            return this;
        }
        _this = this;
        setTimeout(function() {
            _this.active('#' + nodes[0].node_id);
        }, 0);
        return this;
    },
    findNode: function(id, data){
        var node = null;
        for (var i = 0, l = data.length; i < l; i++){
            if (data[i].node_id === id){
                return data[i];
            }
            node = this.findNode(id, data[i].sub_nodes);
            if (null !== node){
                return node;
            }
        }
        return node;
    },
    laod: function(node){
        if ('' === node.uri){
            return this;
        }
        this.http.get(node.uri).success(function(data){
            $('#contentContainer').html(data);
        });
        return this;
    }
});

new MenuList();

'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
  'myApp.filters',
  'myApp.services',
  'myApp.directives',
  'myApp.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {templateUrl: 'partials/partial1.html', controller: 'MyCtrl1'});
  $routeProvider.when('/view2', {templateUrl: 'partials/partial2.html', controller: 'MyCtrl2'});
  $routeProvider.otherwise({redirectTo: '/view1'});
}]);
