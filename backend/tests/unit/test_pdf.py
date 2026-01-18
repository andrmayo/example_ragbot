from pathlib import Path

from resume_ragbot.extraction.extractors import PdfExtractor


class TestPdfExtractor:
    def test_supports_pdf(self):
        extractor = PdfExtractor()
        assert extractor.supports(Path("resume.pdf")) is True
        assert extractor.supports(Path("resume.PDF")) is True
        assert extractor.supports(Path("resume.docx")) is False
        assert extractor.supports(Path("resume.txt")) is False

    def test_extract_returns_content(self, sample_pdf: Path):
        extractor = PdfExtractor()
        result = extractor.extract(sample_pdf)

        assert result.content != ""
        assert result.source == "engineering_resume25.pdf"
        assert result.metadata["file_type"] == ".pdf"
        assert "page_count" in result.metadata

    def test_extract_contains_expected_text(self, sample_pdf: Path):
        extractor = PdfExtractor()
        result = extractor.extract(sample_pdf)

        assert "Erica Engineer" in result.content
        assert "Environmental Engineering" in result.content
        assert "University of Georgia" in result.content
