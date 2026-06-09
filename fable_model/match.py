from enum import Enum
from typing import Annotated, Any, Self

from pydantic import Field, model_validator, field_validator

from fable_model.common import ParentModel, BitVectorEntity


class MatchMethod(str, Enum):
    crosswise = "crosswise"
    pairwise = "pairwise"


class SimilarityMeasure(str, Enum):
    dice = "dice"
    cosine = "cosine"
    jaccard = "jaccard"
    russell_rao = "russell_rao"
    sokal_sneath = "sokal_sneath"
    sokal_michener = "sokal_michener"
    roger_tanimoto = "roger_tanimoto"


class SimilarityAggregator(str, Enum):
    none = "none"
    avg = "avg"
    max = "max"
    min = "min"


class MatchConfig(ParentModel):
    measures: Annotated[list[SimilarityMeasure], Field(min_length=1)]
    thresholds: Annotated[list[Annotated[float, Field(ge=0, le=1)]], Field(min_length=1)]
    aggregator: SimilarityAggregator = SimilarityAggregator.none
    aggregator_args: Annotated[dict[str, Any], Field(default_factory=dict)]
    method: MatchMethod = MatchMethod.crosswise

    @field_validator("measures", mode="before")
    @classmethod
    def cast_measures(cls, v):
        if isinstance(v, str):
            return [v]
        return v

    @field_validator("thresholds", mode="before")
    @classmethod
    def cast_thresholds(cls, v):
        if isinstance(v, (float, int)):
            return [v]
        return v

    @model_validator(mode="after")
    def validate_measures_and_thresholds(self) -> Self:
        if self.aggregator == SimilarityAggregator.none:
            if len(self.measures) != len(self.thresholds):
                raise ValueError(
                    "Without an aggregator, there must be as many similarity measures as there are thresholds."
                )
        else:
            if len(self.thresholds) != 1:
                raise ValueError("With an aggregator, there need to be exactly one threshold.")

        return self


class BaseMatchRequest(ParentModel):
    config: MatchConfig

    def with_vectors(self, domain_lst: list[BitVectorEntity], range_lst: list[BitVectorEntity]) -> "VectorMatchRequest":
        return VectorMatchRequest(
            config=self.config,
            domain=domain_lst,
            range=range_lst,
        )


class VectorMatchRequest(BaseMatchRequest):
    domain: Annotated[list[BitVectorEntity], Field(min_length=1)]
    range: Annotated[list[BitVectorEntity], Field(min_length=1)]


class Match(ParentModel):
    domain: BitVectorEntity
    range: BitVectorEntity
    similarities: Annotated[list[Annotated[float, Field(ge=0, le=1)]], Field(min_length=1)]
    aggregated_similarity: Annotated[float, Field(ge=0, le=1)] | None


class VectorMatchResponse(ParentModel):
    config: MatchConfig
    matches: list[Match]
