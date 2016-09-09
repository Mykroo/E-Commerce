
// angular.module('BlankApp', ['ngMaterial']);
// var app = angular.module('app', []);
var app=angular.module('toolbarDemo1', ['ngMaterial']).controller('AppCtrl', function($scope,$timeout, $mdSidenav) {
	$scope.toggleLeft = buildToggler('left');
    $scope.toggleRight = buildToggler('right');

    function buildToggler(componentId) {
      return function() {
        $mdSidenav(componentId).toggle();
      }
    }
  });

app.controller('sideBar', function ($scope, $timeout) {
    
  });
// Declare the directive
$(document).ready(function() {
	$('#fullpage').fullpage();
});