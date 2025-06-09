import json
from pathlib import Path
from typing import Literal, Optional

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

    root_class: str = "ace-editor "
    _classes: str = "rounded-md w-full h-56 resize-y"

    def __init__(
        self,
        name: Optional[str] = None,
        content: str = None,
        lang: Literal["sql", "python"] = "python",
        sql_options: Optional[SqlOptions] = None,
        ace_options: Optional[AceOptions] = None,
    ) -> None:
        """Ace Editor

        Use the Ace Editor to edit code in a textarea element.

        Example:
        .. code-block:: python
        
            from uiwiz import ui

            ui.ace(name="editor")

        :param name: The name of the textarea element to be submitted with a form
        :param content: The initial content of the editor
        :param lang: The language mode to use. One of "sql" or "python"
        :param sql_options: Options for the SQL language mode. Tables and columns to be used for autocompletion
        :param ace_options: Options for the Ace Editor
        """
        hidden_text = Element("textarea")
        hidden_text.attributes["hidden"] = "true"
        hidden_text.attributes["name"] = name
        hidden_text.content = content or ""

        super().__init__()
        self.options = ace_options or Ace.default_options
        self.sql_options = sql_options or {}
        hidden_text.attributes["hx-ace-editor-id"] = self.id

        self.classes(Ace._classes)
        self.attributes["hx-ace-editor-lang"] = lang
        self.attributes["hx-ace-editor-hidden-input"] = hidden_text.id
        self.attributes["hx-ace-editor-form"] = self.__find_parent_form__()
        self.attributes["hx-ace-editor-content"] = content


        self.attributes["hx-ace-editor-options"] = json.dumps(humps.camelize(self.options))
        self.attributes["hx-ace-editor-sql-options"] = json.dumps(self.sql_options)

    def __find_parent_form__(self) -> Optional[str]:
        parent = self.parent_element
        while parent:
            if isinstance(parent, Form):
                return parent.id
            parent = parent.parent_element
        return None
