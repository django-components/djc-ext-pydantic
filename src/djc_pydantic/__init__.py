from djc_pydantic.monkeypatch import monkeypatch_pydantic_core_schema
from djc_pydantic.extension import PydanticExtension


monkeypatch_pydantic_core_schema()

__all__ = [
    "PydanticExtension",
]
