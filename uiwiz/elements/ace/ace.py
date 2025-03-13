from pathlib import Path
from typing import Optional

from uiwiz.element import Element
from uiwiz.elements.form import Form

LIB_PATH = Path(__file__).parent / "ace.min.js"
MODE_PYTHON = Path(__file__).parent / "mode-python.js"
SNIPPETS_PYTHON = Path(__file__).parent / "snippets/python.js"
SNIPPETS_SQL = Path(__file__).parent / "snippets/sql.js"
MODE_SQL = Path(__file__).parent / "mode-sql.js"
LIB_LANG_TOOL_PATH = Path(__file__).parent / "ace-lang-tool.min.js"
CSS_PATH = Path(__file__).parent / "acetheme.css"
JS_PATH = Path(__file__).parent / "ace.js"

class Ace(Element, extensions=[CSS_PATH, LIB_PATH, LIB_LANG_TOOL_PATH, MODE_PYTHON, SNIPPETS_PYTHON, SNIPPETS_SQL, MODE_SQL, JS_PATH]):

    def __init__(self, name: str, form: Optional[Form], content:str = None, lang:str = "python") -> None:
        hidden_text = Element("textarea")
        hidden_text.attributes["hidden"] = "true"
        hidden_text.attributes["name"] = name
        super().__init__()
        hidden_text.attributes["hx-ace-editor-id"] = self.id

        self.classes("ace-editor w-full h-96")
        self.attributes["hx-ace-editor-lang"] = lang
        self.attributes["hx-ace-editor-hidden-input"] = hidden_text.id
        self.attributes["hx-ace-editor-form"] = form.id if form else None
        self.attributes["hx-ace-editor-content"] = content
