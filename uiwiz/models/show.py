from typing import TypeVar, Union

import pandas as pd
from pydantic import BaseModel

from uiwiz.element import Element
from uiwiz.elements.col import Col
from uiwiz.elements.row import Row
from uiwiz.elements.table import Table
from uiwiz.models.display import display_name

T = TypeVar("T")


def show(
    data: Union[BaseModel, T, dict, list[T]],
    container_classes: str = "card w-96 bg-base-100 shadow-lg",
    label_classes: str = "flex-auto w-36 font-bold",
    limit: int = 10,
) -> Element:
    if isinstance(data, list):
        return render_list(data, limit)
    else:
        return render_instance(data, container_classes, label_classes)


def render_list(data: list[T], limit: int) -> Element:
    data_to_render = data if len(data) < limit else data[:limit]
    data_to_render = [vars(d) if not isinstance(d, dict) else d for d in data_to_render]
    return __render_list__(data_to_render)


def render_instance(
    instance: Union[BaseModel, T, dict, list[T]],
    container_classes: str = "card w-96 bg-base-100 shadow-lg",
    label_classes: str = "flex-auto w-36 font-bold",
) -> Element:
    fields: dict
    if isinstance(instance, dict):
        fields = instance
    else:
        fields = vars(instance)

    return __render_data__(fields, container_classes, label_classes)


def __render_list__(data: list[dict]) -> Element:
    return Table.from_dataframe(pd.DataFrame(data).rename(columns=display_name))


def __render_data__(data: dict, container_classes: str, label_classes: str) -> Element:
    with Element().classes(container_classes) as card:
        with Col():
            for k, v in data.items():
                with Row():
                    Element(content=display_name(k)).classes(label_classes)
                    Element(content=v)
    return card
