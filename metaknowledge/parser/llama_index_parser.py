from typing import List
from entities.document import Document
from metaknowledge.extractor_base import BaseExtractor
from llama_index.core import SimpleDirectoryReader



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
        
    def file_extract(self,file_type:List) -> list[Document]:
        ##识别出该文件夹中文件类型
        reader = SimpleDirectoryReader(
        input_dir=self._file_path,
        recursive=True,
        required_exts=file_type,
        )
        docs = reader.load_data()
        return docs