const dataEChartName = "data-wz-echart";
var _uiWizardECharts = {};

htmx.defineExtension(dataEChartName, {
    onEvent: function (name, evt) {
        if (name === "htmx:afterSettle") {
            updateEChart(evt.target, JSON.parse(evt.detail.xhr.response));
        }
    }
});

function eChartHandler(element) {
    if (!hasAttribute(element, dataEChartName))
        return;
    const chartOptions = JSON.parse(getAttributeFromElement(element, `${dataEChartName}-options`));
    _uiWizardECharts[element.id] = echarts.init(element);
    updateEChart(element, chartOptions);
}

function updateEChart(element, chartOptions) {
    _uiWizardECharts[element.id].setOption(chartOptions);
}

dataEChartElements = document.querySelectorAll(`[${dataEChartName}]`);

dataEChartElements.forEach((element) => {
    eChartHandler(element);
    window.addEventListener("resize", function () {
        element.resize();
    });
});