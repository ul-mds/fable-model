from fable_model import (
    BitVectorEntity,
    AttributeValueEntity,
    BaseMatchRequest,
    MatchConfig,
    SimilarityMeasure,
    BaseMaskRequest,
    MaskConfig,
    HashConfig,
    HashFunction,
    HashAlgorithm,
    DoubleHash,
    CLKFilter,
    BaseTransformRequest,
    TransformConfig,
    EmptyValueHandling,
    GlobalTransformerConfig,
    NormalizationTransformer,
    MatchMethod,
    SimilarityAggregator,
)

_dummy_entity = AttributeValueEntity(
    id="001", attributes={"first_name": "John", "last_name": "Doe", "date_of_birth": "1987-06-05", "gender": "m"}
)


def test_match_to_full_model_without_aggregation():
    domain_lst = [BitVectorEntity(id="D001", value="kY7yXn+rmp8L0nyGw5NlMw==")]
    range_lst = [BitVectorEntity(id="R001", value="qig0C1i8YttqhPwo4VqLlg==")]

    base = BaseMatchRequest(
        config=MatchConfig(
            measures=SimilarityMeasure.jaccard,
            thresholds=0.8,
            method=MatchMethod.pairwise,
        )
    )

    req = base.with_vectors(domain_lst, range_lst)

    assert base.config == req.config
    assert domain_lst == req.domain
    assert range_lst == req.range


def test_match_to_full_model_with_aggregation():
    domain_lst = [BitVectorEntity(id="D001", value="kY7yXn+rmp8L0nyGw5NlMw==")]
    range_lst = [BitVectorEntity(id="R001", value="qig0C1i8YttqhPwo4VqLlg==")]

    base = BaseMatchRequest(
        config=MatchConfig(
            measures=[SimilarityMeasure.cosine, SimilarityMeasure.roger_tanimoto, SimilarityMeasure.russell_rao],
            thresholds=0.75,
            method=MatchMethod.pairwise,
            aggregator=SimilarityAggregator.avg,
        ),
    )

    req = base.with_vectors(domain_lst, range_lst)

    assert base.config == req.config
    assert domain_lst == req.domain
    assert range_lst == req.range


def test_mask_to_full_model():
    entities = [_dummy_entity]

    base = BaseMaskRequest(
        config=MaskConfig(
            token_size=2,
            hash=HashConfig(function=HashFunction(algorithms=[HashAlgorithm.sha1]), strategy=DoubleHash()),
            filter=CLKFilter(filter_size=1024, hash_values=5),
            padding="_",
        )
    )

    req = base.with_entities(entities)

    assert base.config == req.config
    assert entities == req.entities


def test_transform_to_full_model():
    entities = [_dummy_entity]

    base = BaseTransformRequest(
        config=TransformConfig(empty_value=EmptyValueHandling.ignore),
        global_transformers=GlobalTransformerConfig(before=[NormalizationTransformer()]),
    )

    req = base.with_entities(entities)

    assert base.config == req.config
    assert entities == req.entities
