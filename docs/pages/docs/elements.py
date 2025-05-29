import inspect
from pathlib import Path
from typing import Type

from uiwiz import elements, ui


def get_clean_annotation_name(annotation):
    # if hasattr(annotation, '__origin__') and annotation.__origin__:
    #     if hasattr(annotation.__origin__, "__iter__"):
    #         return ""
    #     origin = annotation if "typing.Optional" not in str(annotation) else "Optional"
    #     args = ", ".join(get_clean_annotation_name(arg) for arg in annotation.__args__)
    #     return f"{origin}[{args}]"
    if hasattr(annotation, '__name__'):
        return annotation.__name__
    elif hasattr(annotation, '_name') and annotation._name:
        return annotation._name
    else:
        return str(annotation).replace('typing.', '')

def extract_param_annotations(cls):
    sig = inspect.signature(cls.__init__)
    annotations = {}
    for name, param in sig.parameters.items():
        if param.annotation is not inspect.Parameter.empty:
            default_value = str(param.default)
            annotations[name] = {
                "type": get_clean_annotation_name(param.annotation),
            }
            if param.default is not inspect.Parameter.empty:
                annotations[name]["default"] = default_value
    return annotations

def create_elements():
    pass
    print(Path(elements.__file__).parent)
    for element_name in dir(ui):
        if element_name.startswith("_"):
            continue
        element = getattr(ui, element_name)
        create_docs_element(element)



def create_docs_element(element: Type[ui.element]):
    with ui.container().classes("prose prose-maincolors"):
        with ui.element().classes("flex flex-row"):
            with ui.element("h2", f"ui.{element.__name__.lower()}"):
                ui.element("span", f"ui.{element.__name__.lower()}")
                
        # ui.element("p", element.__doc__ or "No documentation available.")
        sig = inspect.signature(element.__init__)

        anno = extract_param_annotations(element)
        if anno:
            for name, details in anno.items():
                with ui.element("div").classes("flex flex-row"):
                    ui.element("span", f"{name}: {details['type']}").classes("font-bold")
                    if "default" in details:
                        ui.element("span", f"= {details['default']}").classes("text-gray-500 ml-2")
                    else:
                        ui.element("span", "No default required argument").classes("text-gray-500 ml-2")