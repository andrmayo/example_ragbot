from pathlib import Path

from resume_ragbot.extraction.extractors import PlaintextExtractor


class TestPlaintextExtractor:
    def test_supports_txt(self):
        extractor = PlaintextExtractor()
        assert extractor.supports(Path("resume.txt")) is True
        assert extractor.supports(Path("resume.TXT")) is True
        assert extractor.supports(Path("resume.md")) is True
        assert extractor.supports(Path("resume.pdf")) is False
        assert extractor.supports(Path("resume.docx")) is False

    def test_extract_returns_content(self, sample_txt: Path):
        extractor = PlaintextExtractor()
        result = extractor.extract(sample_txt)

        assert result.content != ""
        assert result.source == "engineering_resume25.txt"
        assert result.metadata["file_type"] == ".txt"

    def test_extract_contains_expected_text(self, sample_txt: Path):
        extractor = PlaintextExtractor()
        result = extractor.extract(sample_txt)

        assert "Erica Engineer" in result.content
        assert "Environmental Engineering" in result.content
        assert "University of Georgia" in result.content
