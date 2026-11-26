from functools import cached_property
from typing import Self

from pydantic import BaseModel, Field, SecretStr, model_validator, computed_field, field_serializer

from fable_model.broker import BaseSessionModel, ClientResultResponse
from fable_model.common import BitVectorMetadata
from fable_model.mask import BaseMaskRequest
from fable_model.transform import BaseTransformRequest


class MetadataAttribute(BaseModel):
    name: str
    attribute: str

    def to_metadata(self, value: str) -> BitVectorMetadata:
        return BitVectorMetadata(name=self.name, value=value)


class PseudonymsSubmissionRequest(BaseSessionModel):
    pseudonyms: list[str]


class ClientCreationRequest(BaseSessionModel):
    transformation: BaseTransformRequest
    masking: BaseMaskRequest
    data_source_domain: str
    metadata_attributes: list[MetadataAttribute] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_attributes(self) -> Self:
        transform_attributes = {
            transformer.attribute_name for transformer in self.transformation.attribute_transformers
        }
        mask_attributes = {attr.attribute_name for attr in self.masking.attributes}
        diff = transform_attributes - mask_attributes

        if len(diff) != 0:
            raise ValueError(
                f"There are attributes configured to be transformed that are not configured to be masked, {diff}."
            )

        return self

    @computed_field
    @cached_property
    def attributes(self) -> list[str]:
        return list({attr.attribute_name for attr in self.masking.attributes})


class ClientMatchSession(ClientCreationRequest):
    client: SecretStr
    session_expires_at: int

    @field_serializer("client")
    def serialize_client(self, value: SecretStr) -> str:
        return value.get_secret_value()


class ResultsFetchingRequest(BaseSessionModel):
    show_unfinished_results: bool = False


PseudonymMatchResponse = ClientResultResponse
