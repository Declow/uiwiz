
htmx.defineExtension("hx-aggrid", {
    onEvent: function (name, evt) {
        if (name === "htmx:afterSettle") {
            const response = JSON.parse(evt.detail.xhr.response);
            const cols = response["cols"];
            const rows = response["rows"];
            gridHandler(evt.target, cols, rows);
        }
    }
});

function gridHandler(element, cols, rows) {
    if (!hasAttribute(element, "hx-aggrid"))
        return;

    createOrGetCurrentGrid(element, cols, rows)
}

var _uiWizardGrids = {}

function getGridOptions(cols, rows) {
    const gridOptions = {
        defaultColDef: {
            resizable: true,
        },
        columnDefs: cols,
        rowData: rows,
        domLayout: 'autoHeight',
        onFirstDataRendered: "autoSizeAll",
    };
    return gridOptions;
}

function createOrGetCurrentGrid(element, cols, rows) {
    var gridApi = null;
    if (element.id in _uiWizardGrids) {
        gridApi = _uiWizardGrids[element.id]
        gridApi.setGridOption('columnDefs', cols);
        gridApi.setGridOption('rowData', rows);
    } else {
        const cols = JSON.parse(getAttributeFromElement(element, "hx-aggrid-cols"));
        const rows = JSON.parse(getAttributeFromElement(element, "hx-aggrid-rows"));

        gridApi = agGrid.createGrid(element, getGridOptions(cols, rows));
        _uiWizardGrids[element.id] = gridApi;
    }
    return gridApi;
}

var elements = document.querySelectorAll("[hx-aggrid]");

elements.forEach((element) => {
    gridHandler(element, null, null);
});