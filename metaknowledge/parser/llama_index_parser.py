from entities.document import Document
from metaknowledge.extractor_base import BaseExtractor
from llama_index.core import SimpleDirectoryReader

from utils.helper import identify_file_types


class LamaIndexExtractor(BaseExtractor):
    """Loader that uses unstructured to load word documents."""

    def __init__(
        self,
        file_path: str,
        api_url: str,
    ):
        """Initialize with file path."""
        self._file_path = file_path
        self._api_url = api_url
        
    def file_extract(self) -> list[Document]:
        ##识别出该文件夹中文件类型
        file_type = identify_file_types(self._file_path)
        reader = SimpleDirectoryReader(
        input_dir=self._file_path,
        recursive=True,
        required_exts=file_type,
        )
        return reader.load_data()