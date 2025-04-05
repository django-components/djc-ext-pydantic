from django_components import ComponentExtension
from django_components.extension import (
    OnComponentInputContext,
    OnComponentDataContext,
)

from djc_pydantic.validation import get_component_typing, validate_type


class PydanticExtension(ComponentExtension):
    """
    A Django component extension that integrates Pydantic for input and data validation.

    This extension uses the types defined on the component's class to validate the inputs
    and outputs of Django components.

    The following are validated:

    - Inputs:

        - `args`
        - `kwargs`
        - `slots`

    - Outputs (data returned from):

        - `get_context_data()`
        - `get_js_data()`
        - `get_css_data()`

    Validation is done using Pydantic's `TypeAdapter`. As such, the following are expected:

    - Positional arguments (`args`) should be defined as a `Tuple` type.
    - Other data (`kwargs`, `slots`, ...) are all objects or dictionaries, and can be defined
      using either `TypedDict` or Pydantic's `BaseModel`.

    **Example:**

    ```python
    MyCompArgs = Tuple[str, ...]

    class MyCompKwargs(TypedDict):
        name: str
        age: int

    class MyCompSlots(TypedDict):
        header: SlotContent
        footer: SlotContent

    class MyCompData(BaseModel):
        data1: str
        data2: int

    class MyCompJsData(BaseModel):
        js_data1: str
        js_data2: int

    class MyCompCssData(BaseModel):
        css_data1: str
        css_data2: int

    class MyComponent(Component[MyCompArgs, MyCompKwargs, MyCompSlots, MyCompData, MyCompJsData, MyCompCssData]):
        ...
    ```

    To exclude a field from validation, set its type to `Any`.

    ```python
    class MyComponent(Component[MyCompArgs, MyCompKwargs, MyCompSlots, Any, Any, Any]):
        ...
    ```
    """

    name = "pydantic"

    # Validate inputs to the component on `Component.render()`
    def on_component_input(self, ctx: OnComponentInputContext) -> None:
        maybe_inputs = get_component_typing(ctx.component_cls)
        if maybe_inputs is None:
            return

        args_type, kwargs_type, slots_type, data_type, js_data_type, css_data_type = maybe_inputs
        comp_name = ctx.component_cls.__name__

        # Validate args
        validate_type(ctx.args, args_type, f"Positional arguments of component '{comp_name}' failed validation")
        # Validate kwargs
        validate_type(ctx.kwargs, kwargs_type, f"Keyword arguments of component '{comp_name}' failed validation")
        # Validate slots
        validate_type(ctx.slots, slots_type, f"Slots of component '{comp_name}' failed validation")

    # Validate the data generated from `get_context_data()`, `get_js_data()` and `get_css_data()`
    def on_component_data(self, ctx: OnComponentDataContext) -> None:
        maybe_inputs = get_component_typing(ctx.component_cls)
        if maybe_inputs is None:
            return

        args_type, kwargs_type, slots_type, data_type, js_data_type, css_data_type = maybe_inputs
        comp_name = ctx.component_cls.__name__

        # Validate data
        validate_type(ctx.context_data, data_type, f"Data of component '{comp_name}' failed validation")
        # Validate JS data
        validate_type(ctx.js_data, js_data_type, f"JS data of component '{comp_name}' failed validation")
        # Validate CSS data
        validate_type(ctx.css_data, css_data_type, f"CSS data of component '{comp_name}' failed validation")
