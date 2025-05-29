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
        this.element.style.visibility = "hidden";

        this.lang = getAttributeFromElement(element, "hx-ace-editor-lang");
        this.hidden_input = document.getElementById(getAttributeFromElement(element, "hx-ace-editor-hidden-input"));
        this.form = document.getElementById(getAttributeFromElement(element, "hx-ace-editor-form"));
        this.content = getAttributeFromElement(element, "hx-ace-editor-content");

        this.sqlOptions = JSON.parse(getAttributeFromElement(element, "hx-ace-editor-sql-options"));
        this.aceOptions = JSON.parse(getAttributeFromElement(element, "hx-ace-editor-options"));

        this.editor = ace.edit(this.element, this.aceOptions);
        this.editor.clearSelection();
        setTimeout(() => {
            this.editor.selection.clearSelection(); // Deselect text
            this.editor.moveCursorTo(this.editor.session.getLength(), 0); // Move cursor to end
            this.element.style.visibility = "visible";
        }, 0);

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
            if (this.editor.isFocused() && (event.metaKey || event.ctrlKey) && event.key === "Enter") {
                this.hidden_input.value = this.editor.getValue();
                if (this.form) {
                    this.form.requestSubmit();
                }
            }
        });
    }

    update() {
        this.element.textContent = `Click count: ${this.count}`;
    }

    custom_auto_complete() {
        this.sqlCompleter();
    }

    sqlCompleter() {
        if (this.lang !== "sql" || Object.keys(this.sqlOptions).length === 0) {
            return;
        }

        // Define custom SQL tables and columns
        var sqlKeywords = [
            { name: "SELECT", value: "SELECT", score: 1000, meta: "Keyword" },
            { name: "FROM", value: "FROM", score: 1000, meta: "Keyword" },
            { name: "WHERE", value: "WHERE", score: 1000, meta: "Keyword" },
            { name: "INSERT", value: "INSERT", score: 1000, meta: "Keyword" },
            { name: "UPDATE", value: "UPDATE", score: 1000, meta: "Keyword" },
            { name: "DELETE", value: "DELETE", score: 1000, meta: "Keyword" },
            { name: "LIMIT", value: "LIMIT", score: 1000, meta: "Keyword" },
            { name: "ORDER", value: "ORDER", score: 1000, meta: "Keyword" },
            { name: "BY", value: "BY", score: 1000, meta: "Keyword" },
            { name: "AND", value: "AND", score: 1000, meta: "Keyword" },
            { name: "CASE", value: "CASE", score: 1000, meta: "Keyword" },
            { name: "COLUMN", value: "COLUMN", score: 1000, meta: "Keyword" },
            { name: "CONSTRAINT", value: "CONSTRAINT", score: 1000, meta: "Keyword" },
            { name: "GROUP", value: "GROUP", score: 1000, meta: "Keyword" },
            { name: "HAVING", value: "HAVING", score: 1000, meta: "Keyword" },
            { name: "VALUES", value: "VALUES", score: 1000, meta: "Keyword" }
        ];

        this.sqlOptions.tables.forEach(option => {
            sqlKeywords.push({ name: option, value: option, score: 900, meta: "table" });
        });
        this.sqlOptions.columns.forEach(option => {
            sqlKeywords.push({ name: option, value: option, score: 800, meta: "column" });
        });

        // Custom Autocomplete Completer
        var sqlCompleter = {
            getCompletions: function (editor, session, pos, prefix, callback) {
                if (prefix.length === 0) {
                    return callback(null, []);
                }
                var suggestions = sqlKeywords;
                callback(null, suggestions);
            }
        };

        // Register the Completer
        this.editor.completers = [sqlCompleter];
    }
}


document.querySelectorAll(".ace-editor").forEach(function (el) {
    new AceEditor(el);
});