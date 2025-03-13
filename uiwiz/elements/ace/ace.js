document.querySelectorAll("script").forEach(script => {
    if (script.src.includes("ace.js")) {
        let aceBasePath = script.src.replace(/\/ace\.js$/, ""); // Remove "/ace.js" to get the base path
        ace.config.set("basePath", aceBasePath);
    }
});

ace.require("ace/ext/language_tools");

class AceEditor {
    constructor(element) {
        this.element = element;
        this.lang = getAttributeFromElement(element, "hx-ace-editor-lang");
        this.hidden_input = document.getElementById(getAttributeFromElement(element, "hx-ace-editor-hidden-input"));
        this.form = document.getElementById(getAttributeFromElement(element, "hx-ace-editor-form"));
        this.content = getAttributeFromElement(element, "hx-ace-editor-content");
        this.editor = ace.edit(this.element);

        this.editor.setOptions({
            enableBasicAutocompletion: true,  // Ctrl+Space triggers suggestions
            enableLiveAutocompletion: true,   // Live suggestions while typing
            enableSnippets: true              // Enable code snippets
        });

        this.init();
    }

    init() {
        this.editor.session.setMode(`ace/mode/${this.lang}`);
        this.custom_auto_complete();
        this.editor.setValue(this.content);

        this.element.addEventListener("input", () => {
            this.hidden_input.value = this.editor.getValue();
        });

        this.editor.container.addEventListener("keydown", (event) => {
            if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
                this.hidden_input.value = this.editor.getValue();
                htmx.trigger(this.form, "submit");
            }
        });
    }

    update() {
        this.element.textContent = `Click count: ${this.count}`;
    }

    custom_auto_complete() {
        // // Define custom SQL tables and columns
        // var sqlKeywords = [
        //     { name: "SELECT", value: "SELECT", score: 1000, meta: "Keyword" },
        //     { name: "FROM", value: "FROM", score: 1000, meta: "Keyword" },
        //     { name: "WHERE", value: "WHERE", score: 1000, meta: "Keyword" },
        //     { name: "INSERT", value: "INSERT", score: 1000, meta: "Keyword" },
        //     { name: "UPDATE", value: "UPDATE", score: 1000, meta: "Keyword" },
        //     { name: "DELETE", value: "DELETE", score: 1000, meta: "Keyword" }
        // ];

        // var sqlTables = [
        //     { name: "cars", value: "cars", score: 900, meta: "Table" }
        // ];

        // var sqlColumns = [
        //     { name: "reg", value: "reg", score: 800, meta: "Column" },
        //     { name: "vin", value: "vin", score: 800, meta: "Column" },
        //     { name: "make", value: "make", score: 800, meta: "Column" },
        //     { name: "model", value: "model", score: 800, meta: "Column" },
        //     { name: "created_at", value: "created_at", score: 800, meta: "Column" }
        // ];

        // // Custom Autocomplete Completer
        // var sqlCompleter = {
        //     getCompletions: function (editor, session, pos, prefix, callback) {
        //         if (prefix.length === 0) {
        //             return callback(null, []);
        //         }
        //         var suggestions = [...sqlKeywords, ...sqlTables, ...sqlColumns];
        //         callback(null, suggestions);
        //     }
        // };

        // // Register the Completer
        // // editor.completers = [sqlCompleter];
    }
}


document.querySelectorAll(".ace-editor").forEach(function (el) {
    new AceEditor(el);
});