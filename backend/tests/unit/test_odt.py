from pathlib import Path

from resume_ragbot.extraction.extractors import OdtExtractor


class TestOdtExtractor:
    def test_supports_odt(self):
        extractor = OdtExtractor()
        assert extractor.supports(Path("resume.odt")) is True
        assert extractor.supports(Path("resume.ODT")) is True
        assert extractor.supports(Path("resume.pdf")) is False
        assert extractor.supports(Path("resume.docx")) is False

    def test_extract_returns_content(self, sample_odt: Path):
        extractor = OdtExtractor()
        result = extractor.extract(sample_odt)

        assert result.content != ""
        assert result.source == "engineering_resume25.odt"
        assert result.metadata["file_type"] == ".odt"

    def test_extract_contains_expected_text(self, sample_odt: Path):
        extractor = OdtExtractor()
        result = extractor.extract(sample_odt)

        assert "Erica Engineer" in result.content
        assert "Environmental Engineering" in result.content
        assert "University of Georgia" in result.content
