from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExtractedDocument:
    content: str
    source: str  # filename or identifier
    metadata: dict[str, str]


class Extractor(ABC):
    @abstractmethod
    def extract(self, file_path: Path) -> ExtractedDocument:
        """Extract text content from a file."""
        ...

    @abstractmethod
    def supports(self, file_path: Path) -> bool:
        """Check if this extractor supports the given file type."""
        ...
