from typing import Annotated, Literal

from packaging.version import Version, InvalidVersion
from pydantic import BaseModel, ConfigDict, BeforeValidator, Field


class ParentModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AttributeValueEntity(ParentModel):
    id: str
    attributes: dict[str, str]


class BitVectorMetadata(BaseModel):
    name: str
    value: str


class PseudonymizedAttributeValueEntity(AttributeValueEntity):
    pseudonym: str
    metadata: list[BitVectorMetadata] = Field(default_factory=list)

    def to_attribute_value_entity(self) -> AttributeValueEntity:
        return AttributeValueEntity(id=self.id, attributes=self.attributes)


class BitVectorEntity(ParentModel):
    id: str
    value: str


class MetaBitVectorEntity(BitVectorEntity):
    metadata: list[BitVectorMetadata] = Field(default_factory=list)


class HealthResponse(ParentModel):
    status: Literal["ok"] = "ok"


def _validate_version(value: str) -> str:
    try:
        Version(value)
    except InvalidVersion as e:
        raise ValueError(f"Invalid version: {value!r}") from e

    return value


class ServiceBaseInformation(ParentModel):
    version: Annotated[str, BeforeValidator(_validate_version)]
