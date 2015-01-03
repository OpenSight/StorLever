(function(){
  'use strict';

/* Filters */

  angular.module('app.filters', []).filter('interpolate', ['version', function(version) {
    return function(text) {
      return String(text).replace(/\%VERSION\%/mg, version);
    };
  }]).filter('KB', [function() {
    var step = 1024;
    var unit = ['KB', 'MB', 'GB', 'TB'];
    return function(capacity, bit) {
      for (var i = 0, l = unit.length; i < l; i++){
        capacity = capacity / step;
        if (capacity < 0){
          break;
        }
      }
      var tmp = Math.pow(10, bit);
      capacity = Math.round(capacity * step * tmp) / tmp;
      return String(text).replace(/\%VERSION\%/mg, version);
    };
  }]);
})();