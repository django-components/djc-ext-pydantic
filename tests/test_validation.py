from typing import Any, Dict, List, Tuple, Type, Union

import pytest
from django_components import Component, SlotContent, types
from django_components.testing import djc_test
# from pydantic import ValidationError # TODO: Set more specific error message
from typing_extensions import TypedDict

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
            def get_context_data(self, var1, var2, variable, another, **attrs):
                return {
                    "variable": variable,
                    "invalid_key": var1,
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
                "my_slot2": lambda ctx, data, ref: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_no_validation_on_any(self):
        class TestComponent(Component[Any, Any, Any, Any, Any, Any]):
            def get_context_data(self, var1, var2, variable, another, **attrs):
                return {
                    "variable": variable,
                    "invalid_key": var1,
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
                "my_slot2": lambda ctx, data, ref: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_invalid_args(self):
        TestArgs = Tuple[int, str, int]

        class TestComponent(Component[TestArgs, Any, Any, Any, Any, Any]):
            def get_context_data(self, var1, var2, variable, another, **attrs):
                return {
                    "variable": variable,
                    "invalid_key": var1,
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "my_slot" / %}
                Slot 2: {% slot "my_slot2" / %}
            """

        # TODO: Set more specific error message
        # with pytest.raises(
        #     ValidationError,
        #     match=re.escape("Positional arguments of component 'TestComponent' failed validation"),
        # ):
        with pytest.raises(Exception):
            TestComponent.render(
                args=(123, "str"),  # type: ignore
                kwargs={"variable": "test", "another": 1},
                slots={
                    "my_slot": "MY_SLOT",
                    "my_slot2": lambda ctx, data, ref: "abc",
                },
            )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_valid_args(self):
        TestArgs = Tuple[int, str, int]

        class TestComponent(Component[TestArgs, Any, Any, Any, Any, Any]):
            def get_context_data(self, var1, var2, var3, variable, another, **attrs):
                return {
                    "variable": variable,
                    "invalid_key": var1,
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "my_slot" / %}
                Slot 2: {% slot "my_slot2" / %}
            """

        TestComponent.render(
            args=(123, "str", 456),
            kwargs={"variable": "test", "another": 1},
            slots={
                "my_slot": "MY_SLOT",
                "my_slot2": lambda ctx, data, ref: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_invalid_kwargs(self):
        class TestKwargs(TypedDict):
            var1: int
            var2: str
            var3: int

        class TestComponent(Component[Any, TestKwargs, Any, Any, Any, Any]):
            def get_context_data(self, var1, var2, variable, another, **attrs):
                return {
                    "variable": variable,
                    "invalid_key": var1,
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "my_slot" / %}
                Slot 2: {% slot "my_slot2" / %}
            """

        # TODO: Set more specific error message
        # with pytest.raises(
        #     ValidationError,
        #     match=re.escape("Keyword arguments of component 'TestComponent' failed validation"),
        # ):
        with pytest.raises(Exception):
            TestComponent.render(
                args=(123, "str"),
                kwargs={"variable": "test", "another": 1},  # type: ignore
                slots={
                    "my_slot": "MY_SLOT",
                    "my_slot2": lambda ctx, data, ref: "abc",
                },
            )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_valid_kwargs(self):
        class TestKwargs(TypedDict):
            var1: int
            var2: str
            var3: int

        class TestComponent(Component[Any, TestKwargs, Any, Any, Any, Any]):
            def get_context_data(self, a, b, c, var1, var2, var3, **attrs):
                return {
                    "variable": var1,
                    "invalid_key": var2,
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "my_slot" / %}
                Slot 2: {% slot "my_slot2" / %}
            """

        TestComponent.render(
            args=(123, "str", 456),
            kwargs={"var1": 1, "var2": "str", "var3": 456},
            slots={
                "my_slot": "MY_SLOT",
                "my_slot2": lambda ctx, data, ref: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_invalid_slots(self):
        class TestSlots(TypedDict):
            slot1: SlotContent
            slot2: SlotContent

        class TestComponent(Component[Any, Any, TestSlots, Any, Any, Any]):
            def get_context_data(self, var1, var2, variable, another, **attrs):
                return {
                    "variable": variable,
                    "invalid_key": var1,
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "slot1" / %}
                Slot 2: {% slot "slot2" / %}
            """

        # TODO: Set more specific error message
        # with pytest.raises(
        #     ValidationError,
        #     match=re.escape("Slots of component 'TestComponent' failed validation"),
        # ):
        with pytest.raises(Exception):
            TestComponent.render(
                args=(123, "str"),
                kwargs={"variable": "test", "another": 1},
                slots={
                    "my_slot": "MY_SLOT",
                    "my_slot2": lambda ctx, data, ref: "abc",
                },  # type: ignore
            )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_valid_slots(self):
        class TestSlots(TypedDict):
            slot1: SlotContent
            slot2: SlotContent

        class TestComponent(Component[Any, Any, TestSlots, Any, Any, Any]):
            def get_context_data(self, a, b, c, var1, var2, var3, **attrs):
                return {
                    "variable": var1,
                    "invalid_key": var2,
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "slot1" / %}
                Slot 2: {% slot "slot2" / %}
            """

        TestComponent.render(
            args=(123, "str", 456),
            kwargs={"var1": 1, "var2": "str", "var3": 456},
            slots={
                "slot1": "SLOT1",
                "slot2": lambda ctx, data, ref: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_invalid_data(self):
        class TestData(TypedDict):
            data1: int
            data2: str

        class TestComponent(Component[Any, Any, Any, TestData, Any, Any]):
            def get_context_data(self, var1, var2, variable, another, **attrs):
                return {
                    "variable": variable,
                    "invalid_key": var1,
                }

            template: types.django_html = """
                {% load component_tags %}
                Variable: <strong>{{ variable }}</strong>
                Slot 1: {% slot "slot1" / %}
                Slot 2: {% slot "slot2" / %}
            """

        # TODO: Set more specific error message
        # with pytest.raises(
        #     ValidationError,
        #     match=re.escape("Data of component 'TestComponent' failed validation"),
        # ):
        with pytest.raises(Exception):
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
    def test_valid_data(self):
        class TestData(TypedDict):
            data1: int
            data2: str

        class TestComponent(Component[Any, Any, Any, TestData, Any, Any]):
            def get_context_data(self, a, b, c, var1, var2, **attrs):
                return {
                    "data1": var1,
                    "data2": var2,
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
                "slot2": lambda ctx, data, ref: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_validate_all(self):
        TestArgs = Tuple[int, str, int]

        class TestKwargs(TypedDict):
            var1: int
            var2: str
            var3: int

        class TestSlots(TypedDict):
            slot1: SlotContent
            slot2: SlotContent

        class TestData(TypedDict):
            data1: int
            data2: str

        class TestComponent(Component[TestArgs, TestKwargs, TestSlots, TestData, Any, Any]):
            def get_context_data(self, a, b, c, var1, var2, **attrs):
                return {
                    "data1": var1,
                    "data2": var2,
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
                "slot2": lambda ctx, data, ref: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_handles_nested_types(self):
        class NestedDict(TypedDict):
            nested: int

        NestedTuple = Tuple[int, str, int]
        NestedNested = Tuple[NestedDict, NestedTuple, int]
        TestArgs = Tuple[NestedDict, NestedTuple, NestedNested]

        class TestKwargs(TypedDict):
            var1: NestedDict
            var2: NestedTuple
            var3: NestedNested

        class TestComponent(Component[TestArgs, TestKwargs, Any, Any, Any, Any]):
            def get_context_data(self, a, b, c, var1, var2, **attrs):
                return {
                    "data1": var1,
                    "data2": var2,
                }

            template: types.django_html = """
                {% load component_tags %}
                Data 1: <strong>{{ data1 }}</strong>
                Data 2: <strong>{{ data2 }}</strong>
                Slot 1: {% slot "slot1" / %}
                Slot 2: {% slot "slot2" / %}
            """

        # TODO: Set more specific error message
        # with pytest.raises(
        #     ValidationError,
        #     match=re.escape("Positional arguments of component 'TestComponent' failed validation"),
        # ):
        with pytest.raises(Exception):
            TestComponent.render(
                args=(123, "str", 456),  # type: ignore
                kwargs={"var1": 1, "var2": "str", "var3": 456},  # type: ignore
                slots={
                    "slot1": "SLOT1",
                    "slot2": lambda ctx, data, ref: "abc",
                },
            )

        TestComponent.render(
            args=({"nested": 1}, (1, "str", 456), ({"nested": 1}, (1, "str", 456), 456)),
            kwargs={"var1": {"nested": 1}, "var2": (1, "str", 456), "var3": ({"nested": 1}, (1, "str", 456), 456)},
            slots={
                "slot1": "SLOT1",
                "slot2": lambda ctx, data, ref: "abc",
            },
        )

    @djc_test(
        components_settings={"extensions": [PydanticExtension]},
    )
    def test_handles_component_types(self):
        TestArgs = Tuple[Type[Component]]

        class TestKwargs(TypedDict):
            component: Type[Component]

        class TestComponent(Component[TestArgs, TestKwargs, Any, Any, Any, Any]):
            def get_context_data(self, a, component, **attrs):
                return {
                    "component": component,
                }

            template: types.django_html = """
                {% load component_tags %}
                Component: <strong>{{ component }}</strong>
            """

        # TODO: Set more specific error message
        # with pytest.raises(
        #     ValidationError,
        #     match=re.escape("Positional arguments of component 'TestComponent' failed validation"),
        # ):
        with pytest.raises(Exception):
            TestComponent.render(
                args=[123],  # type: ignore
                kwargs={"component": 1},  # type: ignore
            )

        TestComponent.render(
            args=(TestComponent,),
            kwargs={"component": TestComponent},
        )

    def test_handles_typing_module(self):
        TodoArgs = Tuple[
            Union[str, int],
            Dict[str, int],
            List[str],
            Tuple[int, Union[str, int]],
        ]

        class TodoKwargs(TypedDict):
            one: Union[str, int]
            two: Dict[str, int]
            three: List[str]
            four: Tuple[int, Union[str, int]]

        class TodoData(TypedDict):
            one: Union[str, int]
            two: Dict[str, int]
            three: List[str]
            four: Tuple[int, Union[str, int]]

        TodoComp = Component[TodoArgs, TodoKwargs, Any, TodoData, Any, Any]

        class TestComponent(TodoComp):
            def get_context_data(self, *args, **kwargs):
                return {
                    **kwargs,
                }

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
