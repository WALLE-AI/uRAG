from entities.document import Document
from metaknowledge.extractor_base import BaseExtractor


class LlamaChainExtractor(BaseExtractor):
    """Loader that uses unstructured to load word documents."""

    def __init__(
        self,
        file_path: str,
        api_url: str,
    ):
        """Initialize with file path."""
        self._file_path = file_path
        self._api_url = api_url
        
    def pdf_extract(self) -> list[Document]:
        pass