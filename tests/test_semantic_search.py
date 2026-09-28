import pytest
from matching.semantic_search import hybrid_search, evaluate_retrieval_performance, cosine_similarity
import numpy as np

def test_cosine_similarity():
    v1 = np.array([1.0, 0.0], dtype=np.float32)
    v2 = np.array([1.0, 0.0], dtype=np.float32)
    assert cosine_similarity(v1, v2) == 1.0

def test_hybrid_search():
    res = hybrid_search("data pipelines", alpha=0.7, top_k=2)
    assert len(res["results"]) == 2
    assert res["results"][0]["id"] == "CAND_101"

def test_evaluate_retrieval_performance():
    res = evaluate_retrieval_performance()
    assert res["semantic_mrr"] > res["keyword_mrr"]
    assert res["mrr_lift_percent"] == 100.0