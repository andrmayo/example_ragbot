from pathlib import Path

from tqdm import tqdm

from resume_ragbot.config import settings
from resume_ragbot.rag.retriever import Retriever
from resume_ragbot.rag.chunking import chunk_text
from resume_ragbot.rag.prompts import build_qa_prompt, SYSTEM_PROMPT
from resume_ragbot.extraction.extractors import EXTRACTORS
from resume_ragbot.llm import get_client
from resume_ragbot.llm.base import InputMessage

from .cases import EVAL_CASES, EvalCase
from .metrics import source_recall, keyword_recall


def load_fixtures(fixture_dir: Path, retriever: Retriever) -> None:
    """Load all test resumes into the retriever."""
    files = list(fixture_dir.iterdir())
    for file_path in tqdm(files, desc="Extracting chunks from files"):
        if file_path.is_dir():
            continue
        for extractor in EXTRACTORS:
            if extractor.supports(file_path):
                doc = extractor.extract(file_path)
                chunks = chunk_text(doc.content, source=file_path.name)
                retriever.add_chunks(chunks)
                break


def run_case(case: EvalCase, retriever: Retriever, client) -> dict:
    """Run a single eval case and return metrics."""
    # Retrieve
    chunks = retriever.search(case.question, k=settings.k_chunks)
    sources = list(set(c.source for c in chunks))

    # Generate answer
    prompt = build_qa_prompt(case.question, chunks)
    response = client.complete(
        messages=[InputMessage(role="user", content=prompt)],
        system=SYSTEM_PROMPT,
    )

    # Score
    return {
        "question": case.question,
        "answer": response.content,
        "sources": sources,
        "source_recall": source_recall(case.expected_sources, sources),
        "keyword_recall": keyword_recall(case.expected_keywords, response.content),
    }


def run_eval(fixture_dir: Path) -> list[dict]:
    """Run all eval cases and return results."""
    retriever = Retriever()
    load_fixtures(fixture_dir, retriever)

    client = get_client()
    results = []

    for case in tqdm(EVAL_CASES, desc="Running eval on cases"):
        result = run_case(case, retriever, client)
        results.append(result)
        print(f"Q: {case.question}")
        print(f"   Source recall: {result['source_recall']:.2f}")
        print(f"   Keyword recall: {result['keyword_recall']:.2f}")

    # Summary
    avg_source = sum(r["source_recall"] for r in results) / len(results)
    avg_keyword = sum(r["keyword_recall"] for r in results) / len(results)
    print(
        f"\nOverall: source_recall={avg_source:.2f}, keyword_recall={avg_keyword:.2f}"
    )

    return results


if __name__ == "__main__":
    fixture_dir = Path(__file__).parent.parent / "fixtures"
    run_eval(fixture_dir)
