
$.get('/topVentas', function(data, textStatus, xhr) {
    /*optional stuff to do after success */
    topVentasDat = [{"country": "USA","visits": 2025,"color": "#FF0F00"}, {"country": "China","visits": 1882,"color": "#FF6600"}, {"country": "Japan","visits": 1809,"color": "#FF9E01"}, {"country": "Germany","visits": 1322,"color": "#FCD202"}, {"country": "UK","visits": 1122,"color": "#F8FF01"}, {"country": "France","visits": 1114,"color": "#B0DE09"}, {"country": "India","visits": 984,"color": "#04D215"}, {"country": "Spain","visits": 711,"color": "#0D8ECF"}, {"country": "Netherlands","visits": 665,"color": "#0D52D1"}, {"country": "Russia","visits": 580,"color": "#2A0CD0"}, {"country": "South Korea","visits": 443,"color": "#8A0CCF"}, {"country": "Canada","visits": 441,"color": "#CD0D74"}, {"country": "Brazil","visits": 395,"color": "#754DEB"}, {"country": "Italy","visits": 386,"color": "#DDDDDD"}, {"country": "Taiwan","visits": 338,"color": "#333333"}]
    console.log(topVentasDat)
    console.log("**********************")

    topVentasDat = JSON.parse(data)
    console.log(topVentasDat)
    var topVentas = AmCharts.makeChart("topVentas", {
        "language":"es",
        "theme": "patterns",
        "type": "serial",
        "startDuration": 3,
        "dataProvider": topVentasDat,
        "valueAxes": [{
            "position": "left",
            "axisAlpha":0,
            "gridAlpha":0
        }],
        "graphs": [{
            "balloonText": "[[category]]: <b>[[value]]</b>",
            "colorField": "color",
            "fillAlphas": 0.85,
            "lineAlpha": 0.1,
            "type": "column",
            "topRadius":1,
            "valueField": "visits"
        }],
        "depth3D": 40,
        "angle": 40,
        "chartCursor": {
            "categoryBalloonEnabled": false,
            "cursorAlpha": 0,
            "zoomable": false
        },
        "categoryField": "country",
        "categoryAxis": {
            "gridPosition": "start",
            "axisAlpha":0,
            "gridAlpha":0

        },
        "export": {
            "enabled": true,
            "language": "es"
        }
    }, 0);
});
//******************************************top Ventas **********************************************
var chartData = generateChartData();
var ventasMensuales = AmCharts.makeChart("ventasMensuales", {
    "type": "serial",
    "language":"es",
    "theme": "dark",
    "marginRight": 80,
    "autoMarginOffset": 20,
    "marginTop": 7,
    "dataProvider": chartData,
    "valueAxes": [{
        "axisAlpha": 0.2,
        "dashLength": 1,
        "position": "left"
    }],
    "mouseWheelZoomEnabled": true,
    "graphs": [{
        "id": "g1",
        "balloonText": "[[value]]",
        "bullet": "round",
        "bulletBorderAlpha": 1,
        "bulletColor": "#FFFFFF",
        "hideBulletsCount": 50,
        "title": "red line",
        "valueField": "visits",
        "useLineColorForBulletBorder": true,
        "balloon":{
            "drop":true
        }
    }],
    "chartScrollbar": {
        "autoGridCount": true,
        "graph": "g1",
        "scrollbarHeight": 40
    },
    "chartCursor": {
       "limitToGraph":"g1"
   },
   "categoryField": "date",
   "categoryAxis": {
    "parseDates": true,
    "axisColor": "#DADADA",
    "dashLength": 1,
    "minorGridEnabled": true
},
"export": {
    "enabled": true,
    "menu": [ {
      "class": "export-main",
      "menu": [ {
        "label": "Descargar",
        "menu": [ "PNG", "JPG", "CSV" ]
      }, {
        "label": "Anotaciones",
        "action": "draw",
        "menu": [ {
          "class": "export-drawing",
          "menu": [ "PNG", "JPG" ]
        } ]
      } ]
    } ]

}
});
ventasMensuales.addListener("rendered", zoomChart);
zoomChart();

// this method is called when chart is first inited as we listen for "rendered" event
function zoomChart() {
    // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
    ventasMensuales.zoomToIndexes(chartData.length - 40, chartData.length - 1);
}
// generate some random data, quite different range
function generateChartData() {
    var chartData = [];
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 5);

    for (var i = 0; i < 1000; i++) {
        // we create date objects here. In your data, you can have date strings
        // and then set format of your dates using chart.dataDateFormat property,
        // however when possible, use date objects, as this will speed up chart rendering.
        var newDate = new Date(firstDate);
        newDate.setDate(newDate.getDate() + i);

        var visits = Math.round(Math.random() * (40 + i / 5)) + 20 + i;

        chartData.push({
            date: newDate,
            visits: visits
        });
    }
    return chartData;
}
//***************************** mensuales********************************************

var ganancias = AmCharts.makeChart("ganancias", {
  "language":"es",
  "theme": "dark",
  "type": "gauge",
  "axes": [{
    "topTextFontSize": 20,
    "topTextYOffset": 70,
    "axisColor": "#31d6ea",
    "axisThickness": 1,
    "endValue": 100,
    "gridInside": true,
    "inside": true,
    "radius": "50%",
    "valueInterval": 10,
    "tickColor": "#67b7dc",
    "startAngle": -90,
    "endAngle": 90,
    "unit": "mdd",
    "bandOutlineAlpha": 0,
    "bands": [{
      "color": "#0080ff",
      "endValue": 100,
      "innerRadius": "105%",
      "radius": "170%",
      "gradientRatio": [0.5, 0, -0.5],
      "startValue": 0
  }, {
      "color": "#3cd3a3",
      "endValue": 0,
      "innerRadius": "105%",
      "radius": "170%",
      "gradientRatio": [0.5, 0, -0.5],
      "startValue": 0
  }]
}],
"arrows": [{
    "alpha": 1,
    "innerRadius": "35%",
    "nailRadius": 0,
    "radius": "170%"
}]
});
setInterval(randomValue, 2000);
// set random value
function randomValue() {
  var value = Math.round(Math.random() * 100);
  ganancias.arrows[0].setValue(value);
  ganancias.axes[0].setTopText("$ "+value + "mdd");
  // adjust darker band to new value
  ganancias.axes[0].bands[1].setEndValue(value);
}
//***************************** ganancias ********************************************
$.get('/ventas_edos', function(data) {
    //pieData = [ {"estado": "Aguascalientes","value": 260}, {"estado": "México","value": 201}, {"estado": "Durango","value": 65}, {"estado": "Guanajuato","value": 39}, {"estado": "Nuevo Leon","value": 19}, {"estado": "Jalisco","value": 10} ]
    pieData = JSON.parse(data);
    var chart = AmCharts.makeChart( "regiones", {
      "type": "pie",
      "language":"es",
      "theme": "dark",
      "dataProvider": pieData,
    "valueField": "value",
    "titleField": "estado",
    "outlineAlpha": 0.4,
    "depth3D": 25,
    "innerRadius": 80,
    "balloonText": "[[title]]<br><span style='font-size:14px'><b>[[value]]</b> ([[percents]]%)</span>",
    "angle": 50,
    "export": {
        "enabled": true
    }
} );

});
//***************************** ganancias ********************************************
