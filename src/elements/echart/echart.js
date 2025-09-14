import { registerEChartsTheme } from "./echart.theme.js";

registerEChartsTheme()
const dataEChartName = "data-wz-echart";

class UIWizardEChart {
    constructor(element, options) {
        this.element = element;
        this.chart = echarts.init(element, "westeros");
        this.options = options;
        this.setOptions(options);
        this.addListeners();
        // Listen for attribute changes on the chart element (e.g., theme changes)
        this.obs = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                console.log("Mutation")
                if (mutation.type === "attributes" && mutation.attributeName === "data-theme") {
                    registerEChartsTheme();
                    this.recreate();
                }
            });
        });
        this.obs.observe(document.getElementById("html"), { attributes: true });
    }
    setOptions(options) {
        this.chart.setOption(options);
    }
    addListeners() {
        window.addEventListener("resize", () => {
            this.chart.resize();
        });
    }
    recreate() {
        console.log("Recreating ECharts instance");
        echarts.dispose(this.element);
        this.element._uiWizardEChart = null;
        this.chart = echarts.init(this.element, "westeros");
        this.element._uiWizardEChart = this;
        this.setOptions(this.options);
        this.addListeners();
    }
}

// events

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
    element._uiWizardEChart = new UIWizardEChart(element, chartOptions);
}

function updateEChart(element, chartOptions) {
    if (element._uiWizardEChart) {
        element._uiWizardEChart.setOptions(chartOptions);
    }
}

var dataEChartElements = document.querySelectorAll(`[${dataEChartName}]`);

dataEChartElements.forEach((element) => {
    eChartHandler(element);
});