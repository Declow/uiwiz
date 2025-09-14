import pytest

from docs.pages.docs.extract_doc import extract_text
from src import ui


@pytest.mark.parametrize("docstring, expected_code_snippet", [
    (ui.ace.__init__.__doc__, 'ui.ace(name="editor")'),
    (ui.upload.__init__.__doc__, 'ui.upload("file")'),
    (ui.button.__init__.__doc__, 'button'),
    (ui.textarea.__init__.__doc__, 'ui.textarea'),
    (ui.input.__init__.__doc__, 'from uiwiz import ui\n\nui.input("username", "default_value", "Enter your username")'),
    (ui.upload.on_upload.__doc__, 'ui.upload("file").on_upload(on_upload=handle_upload, swap="none")'),
    #(ui.toast.__init__.__doc__, 'ui.toast("message")'),
    #(ui.aggrid.__init__.__doc__, 'ui.aggrid("grid")'),
])
def test_extract_text(docstring, expected_code_snippet):
    description, code_block, parameters = extract_text(docstring)

    # Verify that the description has no leading/trailing whitespace,
    # and does not include the code block or parameter definitions.
    assert "code-block" not in description
    assert ":param" not in description

    # If the docstring has a code block, check for the expected snippet
    if '.. code-block' in docstring:
        assert expected_code_snippet in code_block
        if 'from uiwiz import ui' in docstring:
            assert 'from uiwiz import ui' in code_block
    else:
        assert code_block == ""

    # Parameter checks only for Ace (others may not have all these params)
    if expected_code_snippet == 'ui.ace(name="editor")':
        expected_params = {
            "name": "The name of the textarea element to be submitted with a form",
            "content": "The initial content of the editor",
            "lang": 'The language mode to use. One of "sql" or "python"',
            "sql_options": "Options for the SQL language mode. Tables and columns to be used for autocompletion",
            "ace_options": "Options for the Ace Editor",
        }
        assert parameters == expected_params