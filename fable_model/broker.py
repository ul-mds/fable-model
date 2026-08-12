from typing import Annotated

from pydantic import BaseModel, Field, SecretStr

from fable_model.common import BitVectorEntity
from fable_model.match import MatchConfig


class BaseSessionModel(BaseModel):
    session: SecretStr


class BaseAuthenticatedSessionModel(BaseSessionModel):
    token: SecretStr


class SessionCreationRequest(BaseSessionModel):
    match_config: MatchConfig
    expires_in: int = 3600


class SessionUpdateResponse(BaseSessionModel):
    expires_at: int


class SessionCreationResponse(SessionUpdateResponse):
    token: SecretStr


SessionDeletionRequest = BaseAuthenticatedSessionModel
SessionUpdateRequest = BaseAuthenticatedSessionModel


class BitVectorMetadata(BaseModel):
    name: str
    value: str


class MetaBitVectorEntity(BitVectorEntity):
    metadata: list[BitVectorMetadata] = Field(default_factory=list)


class BaseClientModel(BaseSessionModel):
    client: SecretStr


class ClientSubmissionRequest(BaseClientModel):
    vectors: list[MetaBitVectorEntity] = Field(min_length=1)


class ClientVectorBatch(BaseModel):
    client: SecretStr
    ids: list[str]


class VectorMatchBatch(BaseModel):
    domain: ClientVectorBatch
    range: list[ClientVectorBatch]
    session: SecretStr
    config: MatchConfig


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
