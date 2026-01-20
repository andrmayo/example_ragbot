def source_recall(expected: list[str], actual: list[str]) -> float:
    """What fraction of expected sources were retrieved?"""
    if not expected:
        return 1.0
    hits = sum(1 for s in expected if s in actual)
    return hits / len(expected)


def keyword_recall(expected: list[str], answer: str) -> float:
    """What fraction of expected keywords appear in answer?"""
    if not expected:
        return 1.0
    answer_lower = answer.lower()
    hits = sum(1 for kw in expected if kw.lower() in answer_lower)
    return hits / len(expected)
