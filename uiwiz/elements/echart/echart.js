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

document.body.addEventListener("uiwizUpdateEChart", function(evt){
    console.log(evt)
})

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

dataEChartElements = document.querySelectorAll(`[${dataEChartName}]`);
console.log(dataEChartElements);

dataEChartElements.forEach((element) => {
    eChartHandler(element);
    window.addEventListener("resize", function () {
        element.resize();
    });
});