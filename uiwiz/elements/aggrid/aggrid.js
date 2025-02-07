
htmx.defineExtension("hx-aggrid", {
    onEvent: function (name, evt) {
        if (name === "htmx:afterSettle") {
            if (!hasAttribute(element, "hx-aggrid"))
                return; // Not an aggrid element target
            
            const response = JSON.parse(evt.detail.xhr.response);
            const cols = response["cols"];
            const rows = response["rows"];
            const element = evt.target;
            _uiWizardGrids[element.id].updateGrid(cols, rows);
        }
    }
});

function gridHandler(element, cols, rows) {
    if (!hasAttribute(element, "hx-aggrid"))
        return;

    createOrGetCurrentGrid(element, cols, rows)
}

var _uiWizardGrids = {}





class WizGrid {
    constructor(element) {
        this.element = element;
        this.cols = JSON.parse(getAttributeFromElement(element, "hx-aggrid-cols"));
        this.rows = JSON.parse(getAttributeFromElement(element, "hx-aggrid-rows"));

        this.createGrid();
    }

    createGrid() {
        const gridOptions = {
            defaultColDef: {
                resizable: true,
            },
            columnDefs: this.cols,
            rowData: this.rows,
            domLayout: 'autoHeight',
            onFirstDataRendered: "autoSizeAll",
        };

        this.gridApi = agGrid.createGrid(this.element, gridOptions);
    }

    updateGrid(cols, rows) {
        this.gridApi.setGridOption('columnDefs', cols);
        this.gridApi.setGridOption('rowData', rows);
    }
}

elements = document.querySelectorAll("[hx-aggrid]").forEach((element) => {
    _uiWizardGrids[element.id] = new WizGrid(element);
});