from djc_ext_pydantic.monkeypatch import monkeypatch_pydantic_core_schema
from djc_ext_pydantic.extension import PydanticExtension


monkeypatch_pydantic_core_schema()

__all__ = [
    "PydanticExtension",
]
