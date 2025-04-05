from djc_pydantic.extension import PydanticExtension
from djc_pydantic.monkeypatch import monkeypatch_pydantic_core_schema

monkeypatch_pydantic_core_schema()

__all__ = [
    "PydanticExtension",
]
