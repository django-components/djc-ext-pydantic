# djc-ext-pydantic

[![PyPI - Version](https://img.shields.io/pypi/v/djc-ext-pydantic)](https://pypi.org/project/djc-ext-pydantic/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/djc-ext-pydantic)](https://pypi.org/project/djc-ext-pydantic/) [![PyPI - License](https://img.shields.io/pypi/l/djc-ext-pydantic)](https://github.com/django-components/djc-ext-pydantic/blob/main/LICENSE) [![PyPI - Downloads](https://img.shields.io/pypi/dm/djc-ext-pydantic)](https://pypistats.org/packages/djc-ext-pydantic) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/django-components/djc-ext-pydantic/tests.yml)](https://github.com/django-components/djc-ext-pydantic/actions/workflows/tests.yml)

Validate components' inputs and outputs using Pydantic.

`djc-ext-pydantic` is a [django-component](https://github.com/django-components/django-components) extension that integrates [Pydantic](https://pydantic.dev/) for input and data validation.

### Example Usage

```python
from django_components import Component, SlotInput
from djc_pydantic import ArgsBaseModel
from pydantic import BaseModel

# 1. Define the Component with Pydantic models
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

# 2. Render the component
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

## Validating args

By default, Pydantic's `BaseModel` requires all fields to be passed as keyword arguments. If you want to validate positional arguments, you can use a custom subclass `ArgsBaseModel`:

```python
from pydantic import BaseModel
from djc_pydantic import ArgsBaseModel

class MyTable(Component):
    class Args(ArgsBaseModel):
        a: int
        b: str
        c: float

MyTable.render(
    args=[1, "hello", 3.14],
)
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
