# djc-ext-pydantic

[![PyPI - Version](https://img.shields.io/pypi/v/djc-ext-pydantic)](https://pypi.org/project/djc-ext-pydantic/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/djc-ext-pydantic)](https://pypi.org/project/djc-ext-pydantic/) [![PyPI - License](https://img.shields.io/pypi/l/djc-ext-pydantic)](https://github.com/django-components/djc-ext-pydantic/blob/main/LICENSE) [![PyPI - Downloads](https://img.shields.io/pypi/dm/djc-ext-pydantic)](https://pypistats.org/packages/djc-ext-pydantic) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/django-components/djc-ext-pydantic/tests.yml)](https://github.com/django-components/djc-ext-pydantic/actions/workflows/tests.yml)

Validate components' inputs and outputs using Pydantic.

`djc-ext-pydantic` is a [django-component](https://github.com/django-components/django-components) extension that integrates [Pydantic](https://pydantic.dev/) for input and data validation. It uses the types defined on the component's class to validate both inputs and outputs of Django components.

### Validated Inputs and Outputs

- **Inputs:**

  - `args`: Positional arguments, expected to be defined as a [`Tuple`](https://docs.python.org/3/library/typing.html#typing.Tuple) type.
  - `kwargs`: Keyword arguments, can be defined using [`TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict) or Pydantic's [`BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel).
  - `slots`: Can also be defined using [`TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict) or Pydantic's [`BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel).

- **Outputs:**
  - Data returned from `get_context_data()`, `get_js_data()`, and `get_css_data()`, which can be defined using [`TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict) or Pydantic's [`BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel).

### Example Usage

```python
from pydantic import BaseModel
from typing import Tuple, TypedDict

# 1. Define the types
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

# 2. Define the component with those types
class MyComponent(Component[
    MyCompArgs,
    MyCompKwargs,
    MyCompSlots,
    MyCompData,
    MyCompJsData,
    MyCompCssData,
]):
    ...

# 3. Render the component
MyComponent.render(
    # ERROR: Expects a string
    args=(123,),
    kwargs={
        "name": "John",
        # ERROR: Expects an integer
        "age": "invalid",
    },
    slots={
        "header": "...",
        # ERROR: Expects key "footer"
        "foo": "invalid",
    },
)
```

If you don't want to validate some parts, set them to [`Any`](https://docs.python.org/3/library/typing.html#typing.Any).

```python
class MyComponent(Component[
    MyCompArgs,
    MyCompKwargs,
    MyCompSlots,
    Any,
    Any,
    Any,
]):
    ...
```

## Installation

```bash
pip install djc-ext-pydantic
```

Then add the extension to your project:

```python
# settings.py
COMPONENTS = {
    "extensions": [
        "djc_pydantic.PydanticExtension",
    ],
}
```

or by reference:

```python
# settings.py
from djc_pydantic import PydanticExtension

COMPONENTS = {
    "extensions": [
        PydanticExtension,
    ],
}
```

## Release notes

Read the [Release Notes](https://github.com/django-components/djc-ext-pydantic/tree/main/CHANGELOG.md)
to see the latest features and fixes.

## Development

### Tests

To run tests, use:

```bash
pytest
```
