import json
from pathlib import Path
from typing import Optional

import humps

from uiwiz.element import Element
from uiwiz.elements.ace import AceOptions, SqlOptions
from uiwiz.elements.form import Form

LIB_PATH = Path(__file__).parent / "ace.min.js"
MODE_PYTHON = Path(__file__).parent / "mode-python.js"
SNIPPETS_PYTHON = Path(__file__).parent / "snippets/python.js"
SNIPPETS_SQL = Path(__file__).parent / "snippets/sql.js"
MODE_SQL = Path(__file__).parent / "mode-sql.js"
LIB_LANG_TOOL_PATH = Path(__file__).parent / "ace-lang-tool.min.js"
CSS_PATH = Path(__file__).parent / "acetheme.css"
JS_PATH = Path(__file__).parent / "ace.js"


class Ace(
    Element,
    extensions=[
        CSS_PATH,
        LIB_PATH,
        LIB_LANG_TOOL_PATH,
        MODE_PYTHON,
        SNIPPETS_PYTHON,
        SNIPPETS_SQL,
        MODE_SQL,
        JS_PATH,
    ],
):
    default_options = AceOptions(
        enable_basic_autocompletion=True,
        enable_live_autocompletion=True,
        enable_snippets=True,
        selection_style="text",
        highlight_active_line=False,
        highlight_gutter_line=False,
        print_margin_column=False,
        show_print_margin=False,
    )

    def __init__(
        self,
        name: Optional[str] = None,
        content: str = None,
        lang: str = "python",
        sql_options: Optional[SqlOptions] = None,
        ace_options: Optional[AceOptions] = None,
    ) -> None:
        hidden_text = Element("textarea")
        hidden_text.attributes["hidden"] = "true"
        hidden_text.attributes["name"] = name

        super().__init__()
        hidden_text.attributes["hx-ace-editor-id"] = self.id

        self.classes("ace-editor rounded-md w-full h-96")
        self.attributes["hx-ace-editor-lang"] = lang
        self.attributes["hx-ace-editor-hidden-input"] = hidden_text.id
        self.attributes["hx-ace-editor-form"] = self.find_parent_form()
        self.attributes["hx-ace-editor-content"] = content

        self.attributes["hx-ace-editor-options"] = (
            json.dumps(humps.camelize(ace_options)) if ace_options else json.dumps(humps.camelize(Ace.default_options))
        )
        self.attributes["hx-ace-editor-sql-options"] = json.dumps(sql_options) if sql_options else "{}"

    def find_parent_form(self) -> Optional[str]:
        parent = self.parent_element
        while parent:
            if isinstance(parent, Form):
                return parent.id
            parent = parent.parent_element
        return None
