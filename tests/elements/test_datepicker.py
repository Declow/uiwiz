from datetime import datetime, timezone

import pytest

from uiwiz import ui


def test_datepicker():
    _date = datetime.now(timezone.utc).date()
    output = str(ui.datepicker("name", _date))
    assert f'<input id="a-0" name="name" type="date" value="{_date}">' == output


def test_datepicker_default_after_init():
    _date = datetime.now(timezone.utc).date()
    output = str(ui.datepicker("name").default_date(_date))
    assert f'<input id="a-0" name="name" type="date" value="{_date}">' == output


def test_datepicker_exception():
    with pytest.raises(ValueError) as e:
        ui.datepicker("name").default_date(None)
