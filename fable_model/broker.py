from typing import Annotated

from pydantic import BaseModel, Field, SecretStr, field_serializer

from fable_model.common import BitVectorMetadata, MetaBitVectorEntity
from fable_model.match import MatchConfig


class BaseSessionModel(BaseModel):
    session: SecretStr

    @field_serializer("session")
    def serialize_session(self, value: SecretStr) -> str:
        return value.get_secret_value()


class BaseAuthenticatedSessionModel(BaseSessionModel):
    token: SecretStr

    @field_serializer("token")
    def serialize_token(self, value: SecretStr) -> str:
        return value.get_secret_value()


class SessionCreationRequest(BaseSessionModel):
    match_config: MatchConfig
    expires_in: int = 3600


class SessionUpdateResponse(BaseSessionModel):
    expires_at: int


class SessionGetResponse(SessionUpdateResponse):
    match_config: MatchConfig


class SessionCreationResponse(SessionUpdateResponse):
    token: SecretStr

    @field_serializer("token")
    def serialize_token(self, value: SecretStr) -> str:
        return value.get_secret_value()


SessionDeletionRequest = BaseAuthenticatedSessionModel
SessionUpdateRequest = BaseAuthenticatedSessionModel


class BaseClientModel(BaseSessionModel):
    client: SecretStr

    @field_serializer("client")
    def serialize_client(self, value: SecretStr) -> str:
        return value.get_secret_value()


class ClientSubmissionRequest(BaseClientModel):
    vectors: list[MetaBitVectorEntity] = Field(min_length=1)


class ClientVectorBatch(BaseModel):
    client: SecretStr
    ids: list[str]

    @field_serializer("client")
    def serialize_client(self, value: SecretStr) -> str:
        return value.get_secret_value()


class VectorMatchBatch(BaseModel):
    domain: ClientVectorBatch
    range: list[ClientVectorBatch]
    session: SecretStr
    config: MatchConfig

    @field_serializer("session")
    def serialize_session(self, value: SecretStr) -> str:
        return value.get_secret_value()


class ClientResultRequest(BaseClientModel):
    show_unfinished_results: bool = False


class MatchedClientVector(BaseModel):
    vector: MetaBitVectorEntity
    similarities: Annotated[list[Annotated[float, Field(ge=0, le=1)]], Field(min_length=1)]
    aggregated_similarity: Annotated[float, Field(ge=0, le=1)] | None
    reference_metadata: list[BitVectorMetadata]


class ClientResultResponse(BaseModel):
    finished: bool
    matches: list[MatchedClientVector]
