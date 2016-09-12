
// angular.module('BlankApp', ['ngMaterial']);
// var app = angular.module('app', []);
var app=angular.module('eCommerce', ['ngMaterial'])
.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue-grey')
    .accentPalette('orange');
});

// Declare the directive
$(document).ready(function() {
  $('#fullpage').fullpage();
});
app.controller('AppCtrl', function($scope, $mdDialog,$mdSidenav,$timeout) {
  $scope.toggleLeft = buildToggler('left');
    $scope.toggleRight = buildToggler('right');

    function buildToggler(componentId) {
      return function() {
        $mdSidenav(componentId).toggle();
      }
    }
  $scope.status = '  ';
  $scope.customFullscreen = false;

  $scope.showAdvanced = function(ev) {
    $mdDialog.show({
      controller: DialogController,
      templateUrl: 'login.tmpl.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true,
      fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
    })
    .then(function(answer) {
      $scope.user = answer + '';
    }, function() {
      $scope.user = 'You cancelled the dialog.';
    });
  };
  function DialogController($scope, $mdDialog) {
    $scope.hide = function() {
      $mdDialog.hide();
    };

    $scope.cancel = function() {
      $mdDialog.cancel();
    };

    $scope.answer = function(answer) {
      $mdDialog.hide(answer);
    };
  }});
app.controller('sideBar', function ($scope, $timeout) {
    
  });
app.controller('myCtrl', function($scope, $mdTheming) {
    var removeFunction = $mdTheming.setBrowserColor({
      theme: 'myTheme', // Default is 'default'
      palette: 'accent', // Default is 'primary', any basic material palette and extended palettes are available
      hue: '200' // Default is '800'
    });

    $scope.$on('$destroy', function () {
      removeFunction(); // COMPLETELY removes the browser color
    })
  });
app.controller('productosCtrl', function($scope){
  $scope.relojes=items;
  // console.log($scope.relojes);
});


var items={
  "relojes": [
  {
  "nombre":"Reloj 1",
  "img_src":"/img/relojes/1.jpg",
  "catego":"Sport",
  "precio":45.22,
  "desc":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, ea maiores, at, nostrum tempora culpa dolores repudiandae commodi dignissimos atque.",
  "ventas":456,
  "calif":5},
  {
  "nombre":"Reloj 1",
  "img_src":"/img/relojes/1.jpg",
  "catego":"Sport",
  "precio":45.22,
  "desc":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, ea maiores, at, nostrum tempora culpa dolores repudiandae commodi dignissimos atque.",
  "ventas":456,
  "calif":5},
  {
  "nombre":"Reloj 1",
  "img_src":"/img/relojes/1.jpg",
  "catego":"Sport",
  "precio":45.22,
  "desc":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, ea maiores, at, nostrum tempora culpa dolores repudiandae commodi dignissimos atque.",
  "ventas":456,
  "calif":5},
  {
  "nombre":"Reloj 1",
  "img_src":"/img/relojes/1.jpg",
  "catego":"Sport",
  "precio":45.22,
  "desc":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, ea maiores, at, nostrum tempora culpa dolores repudiandae commodi dignissimos atque.",
  "ventas":456,
  "calif":5}]
}