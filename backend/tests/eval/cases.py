from dataclasses import dataclass


@dataclass
class EvalCase:
    question: str
    expected_sources: list[str]  # filenames that should be retrieved
    expected_keywords: list[str]  # keywords expected in answer
    collection: str = "eval"


EVAL_CASES = [
    EvalCase(
        question="What candidate(s) knows Korean?",
        expected_sources=["MastersResume_PublicDevelopment-1.pdf"],
        expected_keywords=["Korean"],
    ),
    EvalCase(
        question="Which candidate has chemistry experience?",
        expected_sources=["COS_Biochemistry.docx"],
        expected_keywords=["chemistry"],
    ),
    EvalCase(
        question="Which candidate is most qualified for an architecture job?",
        expected_sources=["CoD_Architecture-Resume.pdf"],
        expected_keywords=["architecture"],
    ),
]
