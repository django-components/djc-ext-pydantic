from typing import Any, Type

from django.template import NodeList
from django.utils.safestring import SafeString
from django_components import Component, Slot, SlotFunc
from pydantic_core import core_schema


# For custom classes, Pydantic needs to be told how to handle them.
# We achieve that by setting the `__get_pydantic_core_schema__` attribute on the classes.
def monkeypatch_pydantic_core_schema() -> None:
    # Allow to use Component class inside Pydantic models
    def component_core_schema(cls: Type[Component], _source_type: Any, _handler: Any) -> Any:
        return core_schema.json_or_python_schema(
            # Inside a Python object, the field must be an instance of Component class
            python_schema=core_schema.is_instance_schema(cls),
            # Inside a JSON, the field is represented as a string
            json_schema=core_schema.str_schema(),
        )

    Component.__get_pydantic_core_schema__ = classmethod(component_core_schema)

    # Allow to use Slot class inside Pydantic models
    def slot_core_schema(cls: Type[Slot], _source_type: Any, _handler: Any) -> Any:
        return core_schema.json_or_python_schema(
            # Inside a Python object, the field must be an instance of Slot class
            python_schema=core_schema.is_instance_schema(cls),
            # Inside a JSON, the field is represented as a string
            json_schema=core_schema.str_schema(),
        )

    Slot.__get_pydantic_core_schema__ = classmethod(slot_core_schema)  # type: ignore[attr-defined]

    # Tell Pydantic to handle SafeString as regular string
    def safestring_core_schema(*args: Any, **kwargs: Any) -> Any:
        return core_schema.str_schema()

    SafeString.__get_pydantic_core_schema__ = safestring_core_schema

    # Tell Pydantic to handle SlotFunc as regular function
    def slotfunc_core_schema(*args: Any, **kwargs: Any) -> Any:
        return core_schema.callable_schema()

    SlotFunc.__get_pydantic_core_schema__ = slotfunc_core_schema  # type: ignore[attr-defined]

    # Tell Pydantic to handle NodeList as regular list
    def nodelist_core_schema(*args: Any, **kwargs: Any) -> Any:
        return core_schema.list_schema()

    NodeList.__get_pydantic_core_schema__ = nodelist_core_schema
