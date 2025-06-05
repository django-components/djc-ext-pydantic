import re
from typing import Dict, List, Tuple, Type, Union

import pytest
from django_components import Component, SlotInput, types
from django_components.testing import djc_test
from pydantic import BaseModel, ValidationError

from djc_pydantic import ArgsBaseModel
from djc_pydantic.extension import PydanticExtension
from tests.testutils import setup_test_config

setup_test_config()


@djc_test
class TestValidation:
    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_no_validation_on_no_typing(self):
        class TestComponent(Component):
            def get_template_data(self, args, kwargs, slots, context):
                return {
                    "variable": kwargs["variable"],
                    "invalid_key": args[0],
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "my_slot" / %}
                Slot 2: {% slot "my_slot2" / %}
            """

        TestComponent.render(
            args=(123, "str"),
            kwargs={"variable": "test", "another": 1},
            slots={
                "my_slot": "MY_SLOT",
                "my_slot2": lambda ctx: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_args(self):
        class TestComponent(Component):
            class Args(ArgsBaseModel):
                var1: int
                var2: str
                var3: int

            def get_template_data(self, args: Args, kwargs, slots, context):
                return {
                    "variable": args.var3,
                    "invalid_key": args.var1,
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "my_slot" / %}
                Slot 2: {% slot "my_slot2" / %}
            """

        # Invalid args
        with pytest.raises(ValidationError, match="1 validation error for Args\nvar3"):
            TestComponent.render(
                args=[123, "str"],
                kwargs={"variable": "test", "another": 1},
                slots={
                    "my_slot": "MY_SLOT",
                    "my_slot2": lambda ctx: "abc",
                },
            )

        # Valid args
        TestComponent.render(
            args=(123, "str", 456),
            kwargs={"variable": "test", "another": 1},
            slots={
                "my_slot": "MY_SLOT",
                "my_slot2": lambda ctx: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_kwargs(self):
        class TestComponent(Component):
            class Kwargs(BaseModel):
                var1: int
                var2: str
                var3: int

            def get_template_data(self, args, kwargs: Kwargs, slots, context):
                return {
                    "variable": kwargs.var3,
                    "invalid_key": kwargs.var1,
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "my_slot" / %}
                Slot 2: {% slot "my_slot2" / %}
            """

        # Invalid kwargs
        with pytest.raises(ValidationError, match="3 validation errors for Kwargs"):
            TestComponent.render(
                args=(123, "str"),
                kwargs={"variable": "test", "another": 1},
                slots={
                    "my_slot": "MY_SLOT",
                    "my_slot2": lambda ctx: "abc",
                },
            )

        # Valid kwargs
        TestComponent.render(
            args=(123, "str"),
            kwargs={"var1": 1, "var2": "str", "var3": 456},
            slots={
                "my_slot": "MY_SLOT",
                "my_slot2": lambda ctx: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_slots(self):
        class TestComponent(Component):
            class Slots(BaseModel):
                slot1: SlotInput
                slot2: SlotInput

            def get_template_data(self, args, kwargs, slots, context):
                return {
                    "variable": kwargs["var1"],
                    "invalid_key": args[0],
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "slot1" / %}
                Slot 2: {% slot "slot2" / %}
            """

        # Invalid slots
        with pytest.raises(
            ValidationError,
            match=re.escape("2 validation errors for Slots\nslot1"),
        ):
            TestComponent.render(
                args=(123, "str"),
                kwargs={"var1": 1, "var2": "str"},
                slots={
                    "my_slot": "MY_SLOT",
                    "my_slot2": lambda ctx: "abc",
                },
            )

        # Valid slots
        TestComponent.render(
            args=(123, "str", 456),
            kwargs={"var1": 1, "var2": "str", "var3": 456},
            slots={
                "slot1": "SLOT1",
                "slot2": lambda ctx: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_data__invalid(self):
        class TestComponent(Component):
            class TemplateData(BaseModel):
                data1: int
                data2: str

            def get_template_data(self, args, kwargs, slots, context):
                return {
                    "variable": kwargs["variable"],
                    "invalid_key": args[0],
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "slot1" / %}
                Slot 2: {% slot "slot2" / %}
            """

        with pytest.raises(
            ValidationError,
            match=re.escape("2 validation errors for TemplateData\ndata1"),
        ):
            TestComponent.render(
                args=(123, "str"),
                kwargs={"variable": "test", "another": 1},
                slots={
                    "slot1": "SLOT1",
                    "slot2": lambda ctx, data, ref: "abc",
                },
            )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_data__valid(self):
        class TestComponent(Component):
            class TemplateData(BaseModel):
                data1: int
                data2: str

            def get_template_data(self, args, kwargs, slots, context):
                return {
                    "data1": kwargs["var1"],
                    "data2": kwargs["var2"],
                }

            template: types.django_html = """
                {% load component_tags %}
                Data 1: <strong>{{ data1 }}</strong>
                Data 2: <strong>{{ data2 }}</strong>
                Slot 1: {% slot "slot1" / %}
                Slot 2: {% slot "slot2" / %}
            """

        TestComponent.render(
            args=(123, "str", 456),
            kwargs={"var1": 1, "var2": "str", "var3": 456},
            slots={
                "slot1": "SLOT1",
                "slot2": lambda ctx: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_validate_all(self):
        class TestComponent(Component):
            class Args(ArgsBaseModel):
                var1: int
                var2: str
                var3: int

            class Kwargs(BaseModel):
                var1: int
                var2: str
                var3: int

            class Slots(BaseModel):
                slot1: SlotInput
                slot2: SlotInput

            class TemplateData(BaseModel):
                data1: int
                data2: str

            def get_template_data(self, args: Args, kwargs: Kwargs, slots: Slots, context):
                return {
                    "data1": kwargs.var1,
                    "data2": kwargs.var2,
                }

            template: types.django_html = """
                {% load component_tags %}
                Data 1: <strong>{{ data1 }}</strong>
                Data 2: <strong>{{ data2 }}</strong>
                Slot 1: {% slot "slot1" / %}
                Slot 2: {% slot "slot2" / %}
            """

        TestComponent.render(
            args=(123, "str", 456),
            kwargs={"var1": 1, "var2": "str", "var3": 456},
            slots={
                "slot1": "SLOT1",
                "slot2": lambda ctx: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_handles_nested_types(self):
        class NestedDict(BaseModel):
            nested: int

        NestedTuple = Tuple[int, str, int]
        NestedNested = Tuple[NestedDict, NestedTuple, int]

        class TestComponent(Component):
            class Args(ArgsBaseModel):
                a: NestedDict
                b: NestedTuple
                c: NestedNested

            class Kwargs(BaseModel):
                var1: NestedDict
                var2: NestedTuple
                var3: NestedNested

            def get_template_data(self, args: Args, kwargs: Kwargs, slots, context):
                return {
                    "data1": kwargs.var1,
                    "data2": kwargs.var2,
                }

            template: types.django_html = """
                {% load component_tags %}
                Data 1: <strong>{{ data1 }}</strong>
                Data 2: <strong>{{ data2 }}</strong>
                Slot 1: {% slot "slot1" / %}
                Slot 2: {% slot "slot2" / %}
            """

        with pytest.raises(
            ValidationError,
            match=re.escape("3 validation errors for Args\na"),
        ):
            TestComponent.render(
                args=(123, "str", 456),
                kwargs={"var1": 1, "var2": "str", "var3": 456},
                slots={
                    "slot1": "SLOT1",
                    "slot2": lambda ctx: "abc",
                },
            )

        TestComponent.render(
            args=({"nested": 1}, (1, "str", 456), ({"nested": 1}, (1, "str", 456), 456)),
            kwargs={"var1": {"nested": 1}, "var2": (1, "str", 456), "var3": ({"nested": 1}, (1, "str", 456), 456)},
            slots={
                "slot1": "SLOT1",
                "slot2": lambda ctx: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_handles_component_types(self):
        class TestComponent(Component):
            class Args(ArgsBaseModel):
                a: Type[Component]

            class Kwargs(BaseModel):
                component: Type[Component]

            def get_template_data(self, args: Args, kwargs: Kwargs, slots, context):
                return {
                    "component": kwargs.component,
                }

            template: types.django_html = """
                {% load component_tags %}
                Component: <strong>{{ component }}</strong>
            """

        with pytest.raises(
            ValidationError,
            match=re.escape("1 validation error for Args\na"),
        ):
            TestComponent.render(
                args=[123],
                kwargs={"component": 1},
            )

        TestComponent.render(
            args=(TestComponent,),
            kwargs={"component": TestComponent},
        )

    def test_handles_typing_module(self):
        class TestComponent(Component):
            class Args(ArgsBaseModel):
                a: Union[str, int]
                b: Dict[str, int]
                c: List[str]
                d: Tuple[int, Union[str, int]]

            class Kwargs(BaseModel):
                one: Union[str, int]
                two: Dict[str, int]
                three: List[str]
                four: Tuple[int, Union[str, int]]

            class TemplateData(BaseModel):
                one: Union[str, int]
                two: Dict[str, int]
                three: List[str]
                four: Tuple[int, Union[str, int]]

            def get_template_data(self, args: Args, kwargs: Kwargs, slots, context):
                return kwargs

            template = ""

        TestComponent.render(
            args=("str", {"str": 123}, ["a", "b", "c"], (123, "123")),
            kwargs={
                "one": "str",
                "two": {"str": 123},
                "three": ["a", "b", "c"],
                "four": (123, "123"),
            },
        )
