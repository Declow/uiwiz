const dataEChartName = "data-wz-echart";
var _uiWizardECharts = {};

htmx.defineExtension(dataEChartName, {
    onEvent: function (name, evt) {
        if (name === "htmx:afterSettle") {
            console.log(JSON.parse(evt.detail.xhr.response));
            //gridHandler(evt.target, cols, rows);
        }
    }
});

function eChartHandler(element) {
    console.log(element);
    if (!hasAttribute(element, dataEChartName))
        return;

    updateEChart(element);
}

function updateEChart(element) {
    console.log(element);
    _uiWizardECharts[element.id] = echarts.init(element);
    const chartOptions = JSON.parse(getAttributeFromElement(element, `${dataEChartName}-options`));
    console.log(chartOptions);
    _uiWizardECharts[element.id].setOption(chartOptions);
}


// var chartDom = document.getElementById('echart');
// var myChart = echarts.init(chartDom);
// var option;

// var option = {
//     tooltip: {
//         trigger: "axis",  // Shows tooltip when hovering over points along the axis
//         axisPointer: {
//             type: "line", // Use "line" for a vertical tooltip guide
//         }
//     },
//     xAxis: {
//         type: "category",
//         data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
//     },
//     yAxis: {
//         type: "value"
//     },
//     series: [{
//         name: "Sales",
//         type: "line",
//         data: [150, 230, 224, 218, 135, 147, 260]
//     }]
// };

// myChart.setOption(option);

dataEChartElements = document.querySelectorAll(`[${dataEChartName}]`);
console.log(dataEChartElements);

dataEChartElements.forEach((element) => {
    window.addEventListener("resize", function () {
        element.resize();
    });
    eChartHandler(element);
});