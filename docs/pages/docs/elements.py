import inspect
import typing
from pathlib import Path
from typing import Type

from docs.pages.docs.extract_doc import extract_text
from uiwiz import elements, ui


def get_clean_annotation_name(annotation):
    import typing
    if hasattr(annotation, "__name__"):
        return annotation.__name__
    elif hasattr(annotation, "_name") and annotation._name:
        return annotation._name
    elif hasattr(typing, "ForwardRef") and isinstance(annotation, typing.ForwardRef):
        return annotation.__forward_arg__
    else:
        return str(annotation).replace("typing.", "")


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
    with ui.container(space_y="space-y-2").classes("prose outline rounded-lg"):
        with ui.element().classes("flex flex-row"):
            ui.element("h2", f"ui.{element.__name__.lower()}")

        des, cb, _ = extract_text(element.__init__.__doc__)
        ui.markdown(des).classes("text-content")
        with ui.element().classes("not-prose"):
            try:
                ui.markdown("""```python
""" + cb + """```""")
            except Exception:
                pass
            try:
                exec(cb)
            except Exception:
                pass

        ui.element("h3", "Constructor").classes("mt-4")
        anno = extract_param_annotations(element)
        if anno:
            for name, details in anno.items():
                with ui.element("div").classes("flex flex-row pl-4"):
                    ui.element("span", f"{name}: {details['type']}").classes("font-bold")
                    if "default" in details:
                        ui.element("span", f"= {details['default']}").classes("text-gray-500 ml-2")
                    else:
                        ui.element("span", "No default required argument").classes("text-gray-500 ml-2")
            
            methods = [method for method in inspect.getmembers(element, predicate=inspect.isfunction) if not method[0].startswith("_")]

            if methods:
                with ui.element("h3").classes("mt-4"):
                    ui.element("span", "Methods")
                for method_name, method in methods:
                    with ui.element("div").classes("flex flex-row"):
                        sig = inspect.signature(method)
                        # Use get_type_hints to resolve forward references
                        try:
                            type_hints = typing.get_type_hints(method, globalns=method.__globals__, localns=vars(element))
                        except Exception:
                            type_hints = {}
                        params = []
                        for name, param in sig.parameters.items():
                            if name == "self":
                                continue
                            annotation = type_hints.get(name, param.annotation)
                            param_type = get_clean_annotation_name(annotation) if annotation is not inspect.Parameter.empty else 'Any'
                            params.append(f"{name}: {param_type}")
                        param_str = ", ".join(params)
                        # Return type
                        ret_anno = type_hints.get('return', sig.return_annotation)
                        return_type = get_clean_annotation_name(ret_anno) if ret_anno is not inspect.Signature.empty else "Any"
                        # Method name in bold, params in blue, return type in green
                        ui.element("span", f"{method_name}(").classes("font-bold pl-4")
                        if param_str:
                            ui.element("span", param_str).classes("text-info ml-1 mr-1")
                        ui.element("span", ")").classes("font-bold")
                        ui.element("span", f" -> {return_type}").classes("text-success ml-2")
                    if not method.__doc__:
                        ui.element("span", content="No documentation provided").classes("text-gray-500")
                    else:
                        for line in method.__doc__.splitlines():
                            ui.element("div", content=line).classes("pl-8")
