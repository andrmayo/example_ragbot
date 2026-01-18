from pathlib import Path

from resume_ragbot.extraction.extractors import DocxExtractor


class TestDocxExtractor:
    def test_supports_docx(self):
        extractor = DocxExtractor()
        assert extractor.supports(Path("resume.docx")) is True
        assert extractor.supports(Path("resume.DOCX")) is True
        assert extractor.supports(Path("resume.pdf")) is False
        assert extractor.supports(Path("resume.txt")) is False

    def test_extract_returns_content(self, sample_docx: Path):
        extractor = DocxExtractor()
        result = extractor.extract(sample_docx)

        assert result.content != ""
        assert result.source == "engineering_resume25.docx"
        assert result.metadata["file_type"] == ".docx"

    def test_extract_contains_expected_text(self, sample_docx: Path):
        extractor = DocxExtractor()
        result = extractor.extract(sample_docx)

        assert "Erica Engineer" in result.content
        assert "Environmental Engineering" in result.content
        assert "University of Georgia" in result.content
