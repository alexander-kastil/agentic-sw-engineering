"""Pydantic request and response models, serialized with camelCase JSON keys."""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Base model that reads and writes camelCase JSON, matching the Blazor client contract."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
