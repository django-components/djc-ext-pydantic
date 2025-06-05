from typing import Any

from pydantic import BaseModel


class ArgsBaseModel(BaseModel):
    """
    Replacement for Pydantic's `BaseModel` for positional arguments that are passed to a component.

    `BaseModel` does not support positional arguments, so this class is used to ensure that
    the arguments are passed in the correct order.

    **Example:**

    ```python
    from django_components import Component
    from djc_pydantic import ArgsBaseModel
    from pydantic import BaseModel

    class MyComponent(Component):
        class Args(ArgsBaseModel):
            var1: str
            var2: int

        class Kwargs(BaseModel):
            var3: str
            var4: int
    ```
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Get the field names in definition order
        field_names = list(self.__class__.model_fields.keys())
        # Map positional args to field names
        for i, value in enumerate(args):
            if i >= len(field_names):
                raise TypeError(f"Too many positional arguments for {self.__class__.__name__}")
            if field_names[i] in kwargs:
                raise TypeError(f"Multiple values for argument '{field_names[i]}'")
            kwargs[field_names[i]] = value
        super().__init__(**kwargs)
