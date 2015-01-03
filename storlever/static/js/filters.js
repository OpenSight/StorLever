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
      if (capacity < 0){
        return capacity + unit[0];
      }
      for (var i = 0, l = unit.length; i < l && capacity > 0; i++){
        capacity = capacity / step;
      }
      var tmp = Math.pow(10, bit);
      capacity = Math.round(capacity * step * tmp) / tmp;
      return capacity + unit[i - 1];
    };
  }]);
})();
