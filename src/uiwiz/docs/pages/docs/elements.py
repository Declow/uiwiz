import contextlib
import inspect
import typing

from docs.pages.docs.extract_doc import extract_text

from uiwiz import PageRouter, ui


def get_class_properties(cls: object) -> list[tuple[str, object]]:
    # Returns a list of (name, property) tuples for all properties in the class
    return [
        (name, prop)
        for name, prop in inspect.getmembers(cls)
        if not name.startswith("_")
        and not inspect.isroutine(prop)
        and not isinstance(prop, (property, staticmethod, classmethod))
    ]


def get_clean_annotation_name(annotation: object) -> str:
    if hasattr(annotation, "__name__"):
        return annotation.__name__
    if hasattr(annotation, "_name") and annotation._name:  # noqa: SLF001
        return annotation._name  # noqa: SLF001
    if hasattr(typing, "ForwardRef") and isinstance(annotation, typing.ForwardRef):
        return annotation.__forward_arg__
    return str(annotation).replace("typing.", "")


def extract_param_annotations(cls: object) -> dict[str, dict[str, str]]:
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


def create_elements(router: PageRouter) -> None:
    for element_name in dir(ui):
        if element_name.startswith("_"):
            continue
        element = getattr(ui, element_name)
        create_docs_element(element, router)


def create_docs_element(element: ui.element, router: PageRouter) -> None:  # noqa: C901, PLR0912
    app = router  # noqa
    with ui.container(space_y="").classes("prose rounded-lg"):
        with ui.element().classes("flex flex-row"):
            ui.element("h2", f"ui.{element.__name__.lower()}")

        des, cb, _ = extract_text(element.__init__.__doc__)
        ui.markdown(des).classes("text-content")
        with ui.element().classes("not-prose"):
            with contextlib.suppress(Exception):
                ui.markdown(
                    """```python
"""
                    + cb
                    + " "
                    + """```""",
                )
            with contextlib.suppress(Exception):
                exec(cb)  # noqa: S102

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

            methods = [
                method
                for method in inspect.getmembers(element, predicate=inspect.isfunction)
                if not method[0].startswith("_")
            ]

            if methods:
                with ui.element("h3").classes("mt-4"):
                    ui.element("span", "Methods")
                for method_name, method in methods:
                    with ui.element("div").classes("flex flex-row"):
                        sig = inspect.signature(method)
                        # Use get_type_hints to resolve forward references
                        try:
                            type_hints = typing.get_type_hints(
                                method,
                                globalns=method.__globals__,
                                localns=vars(element),
                            )
                        except Exception:  # noqa: BLE001
                            type_hints = {}
                        params = []
                        for name, param in sig.parameters.items():
                            if name == "self":
                                continue
                            annotation = type_hints.get(name, param.annotation)
                            param_type = (
                                get_clean_annotation_name(annotation)
                                if annotation is not inspect.Parameter.empty
                                else "Any"
                            )
                            params.append(f"{name}: {param_type}")
                        param_str = ", ".join(params)
                        # Return type
                        ret_anno = type_hints.get("return", sig.return_annotation)
                        return_type = (
                            get_clean_annotation_name(ret_anno) if ret_anno is not inspect.Signature.empty else "Any"
                        )
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
