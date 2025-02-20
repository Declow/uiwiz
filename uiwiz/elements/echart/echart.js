// var echarts = require('echarts');

var chartDom = document.getElementById('echart');
var myChart = echarts.init(chartDom);
var option;

var option = {
    tooltip: {
        trigger: "axis",  // Shows tooltip when hovering over points along the axis
        axisPointer: {
            type: "line", // Use "line" for a vertical tooltip guide
        }
    },
    xAxis: {
        type: "category",
        data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    },
    yAxis: {
        type: "value"
    },
    series: [{
        name: "Sales",
        type: "line",
        data: [150, 230, 224, 218, 135, 147, 260]
    }]
};

myChart.setOption(option);

window.addEventListener("resize", function () {
    myChart.resize();
});