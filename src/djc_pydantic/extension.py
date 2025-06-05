from typing import Any, Optional, Set

from django_components import ComponentExtension, ComponentNode, OnComponentInputContext  # noqa: F401
from pydantic import BaseModel


class PydanticExtension(ComponentExtension):
    """
    A Django component extension that integrates Pydantic for input and data validation.

    NOTE: As of v0.140 the extension only ensures that the classes from django-components
    can be used with pydantic. For the actual validation, subclass `Kwargs`, `Slots`, etc
    from Pydantic's `BaseModel`, and use `ArgsBaseModel` for `Args`.

    **Example:**

    ```python
    from django_components import Component, SlotInput
    from pydantic import BaseModel

    class MyComponent(Component):
        class Args(ArgsBaseModel):
            var1: str

        class Kwargs(BaseModel):
            name: str
            age: int

        class Slots(BaseModel):
            header: SlotInput
            footer: SlotInput

        class TemplateData(BaseModel):
            data1: str
            data2: int

        class JsData(BaseModel):
            js_data1: str
            js_data2: int

        class CssData(BaseModel):
            css_data1: str
            css_data2: int

        ...
    ```
    """

    name = "pydantic"

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.rebuilt_comp_cls_ids: Set[str] = set()

    # If the Pydantic models reference other types with forward references,
    # the models may not be complete / "built" when the component is first loaded.
    #
    # Component classes may be created when other modules are still being imported,
    # so we have to wait until we start rendering components to ensure that everything
    # is loaded.
    #
    # At that point, we check for components whether they have any Pydantic models,
    # and whether those models need to be rebuilt.
    #
    # See https://errors.pydantic.dev/2.11/u/class-not-fully-defined
    #
    # Otherwise, we get an error like:
    #
    # ```
    # pydantic.errors.PydanticUserError: `Slots` is not fully defined; you should define
    # `ComponentNode`, then call `Slots.model_rebuild()`
    # ```
    def on_component_input(self, ctx: OnComponentInputContext) -> None:
        if ctx.component.class_id in self.rebuilt_comp_cls_ids:
            return

        for name in ["Args", "Kwargs", "Slots", "TemplateData", "JsData", "CssData"]:
            cls: Optional[BaseModel] = getattr(ctx.component, name, None)
            if cls is None:
                continue

            if hasattr(cls, "__pydantic_complete__") and not cls.__pydantic_complete__:
                # When resolving forward references, Pydantic needs the module globals,
                # AKA a dict that resolves those forward references.
                #
                # There's 2 problems here - user may define their own types which may need
                # resolving. And we define the Slot type which needs to access `ComponentNode`.
                #
                # So as a solution, we provide to Pydantic a dictionary that contains globals
                # from both 1. the component file and 2. this file (where we import `ComponentNode`).
                mod = __import__(cls.__module__)
                module_globals = mod.__dict__
                cls.model_rebuild(_types_namespace={**globals(), **module_globals})

        self.rebuilt_comp_cls_ids.add(ctx.component.class_id)
