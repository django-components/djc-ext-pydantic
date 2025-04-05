import sys
from typing import Any, Literal, Optional, Tuple, Type, Union
from weakref import WeakKeyDictionary

from django_components import Component
from pydantic import TypeAdapter, ValidationError

ComponentTypes = Tuple[Any, Any, Any, Any, Any, Any]


# Cache the types for each component class.
# NOTE: `WeakKeyDictionary` can't be used as generic in Python 3.8
if sys.version_info >= (3, 9):
    types_store: WeakKeyDictionary[
        Type[Component],
        Union[Optional[ComponentTypes], Literal[False]],
    ] = WeakKeyDictionary()
else:
    types_store = WeakKeyDictionary()


def get_component_typing(cls: Type[Component]) -> Optional[ComponentTypes]:
    """
    Extract the types passed to the `Component` class.

    So if a component subclasses `Component` class like so

    ```py
    class MyComp(Component[MyArgs, MyKwargs, MySlots, MyData, MyJsData, MyCssData]):
        ...
    ```

    Then we want to extract the tuple (MyArgs, MyKwargs, MySlots, MyData, MyJsData, MyCssData).

    Returns `None` if types were not provided. That is, the class was subclassed
    as:

    ```py
    class MyComp(Component):
        ...
    ```
    """
    # For efficiency, the type extraction is done only once.
    # If `class_types` is `False`, that means that the types were not specified.
    # If `class_types` is `None`, then this is the first time running this method.
    # Otherwise, `class_types` should be a tuple of (Args, Kwargs, Slots, Data, JsData, CssData)
    class_types = types_store.get(cls, None)
    if class_types is False:  # noqa: E712
        return None
    elif class_types is not None:
        return class_types

    # Since a class can extend multiple classes, e.g.
    #
    # ```py
    # class MyClass(BaseOne, BaseTwo, ...):
    #     ...
    # ```
    #
    # Then we need to find the base class that is our `Component` class.
    #
    # NOTE: `__orig_bases__` is a tuple of `_GenericAlias`
    # See https://github.com/python/cpython/blob/709ef004dffe9cee2a023a3c8032d4ce80513582/Lib/typing.py#L1244
    # And https://github.com/python/cpython/issues/101688
    generics_bases: Tuple[Any, ...] = cls.__orig_bases__  # type: ignore[attr-defined]
    component_generics_base = None
    for base in generics_bases:
        origin_cls = base.__origin__
        if origin_cls == Component or issubclass(origin_cls, Component):
            component_generics_base = base
            break

    if not component_generics_base:
        # If we get here, it means that the `Component` class wasn't supplied any generics
        types_store[cls] = False
        return None

    # If we got here, then we've found ourselves the typed `Component` class, e.g.
    #
    # `Component(Tuple[int], MyKwargs, MySlots, Any, Any, Any)`
    #
    # By accessing the `__args__`, we access individual types between the brackets, so
    #
    # (Tuple[int], MyKwargs, MySlots, Any, Any, Any)
    args_type, kwargs_type, slots_type, data_type, js_data_type, css_data_type = component_generics_base.__args__

    component_types = args_type, kwargs_type, slots_type, data_type, js_data_type, css_data_type
    types_store[cls] = component_types
    return component_types


def validate_type(value: Any, type: Any, msg: str) -> None:
    """
    Validate that the value is of the given type. Uses Pydantic's `TypeAdapter` to
    validate the type.

    If the value is not of the given type, raise a `ValidationError` with a note
    about where the error occurred.
    """
    try:
        # See https://docs.pydantic.dev/2.3/usage/type_adapter/
        TypeAdapter(type).validate_python(value)
    except ValidationError as err:
        # Add note about where the error occurred
        err.add_note(msg)
        raise err
