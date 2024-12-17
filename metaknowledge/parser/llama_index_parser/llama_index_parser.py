from typing import List

import loguru
from entities.document import Document
from metaknowledge.extractor_base import BaseExtractor
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import Settings

from metaknowledge.parser.llama_index_parser.hierarchical import HierarchicalNodeParser
# from metaknowledge.parser.llama_index_parser.splitter import SentenceSplitter
# from llama_index.core.node_parser import SentenceSplitter
from metaknowledge.parser.llama_index_parser.splitter import SentenceSplitter
from metaknowledge.parser.llama_index_parser.transformation import CustomExtractor, CustomFilePathExtractor, CustomTitleExtractor
from llama_index.core.schema import TransformComponent,MetadataMode


class LamaIndexExtractor(BaseExtractor):
    """Loader that uses unstructured to load word documents."""

    def __init__(
        self,
        file_path: str,
        file_type:str="",
        api_url: str="",
    ):
        """Initialize with file path."""
        self._file_path = file_path
        self._api_url = api_url
        self._file_type = file_type
        
    def extract(self) -> list[Document]:
        ##识别出该文件夹中文件类型
        reader = SimpleDirectoryReader(
            input_files=[self._file_path],
            required_exts=[self._file_type]
        )
        documents = []
        docs = reader.load_data()
        ##加入chunk相关逻辑
        nodes = self.llama_index_chunk(documents=docs)
        # for node in nodes:
        #     metadata = node.to_dict()
        #     metadata['metadata']["id_"] = metadata['id_']
        #     doc = Document(page_content=node.text,metadata=metadata['metadata'])
        #     documents.append(doc)
        return nodes
    
    def llama_index_chunk(self,
        documents,
        data_path=None,
        chunk_size=1024,
        chunk_overlap=50,
        split_type=0) -> list[Document]:
        transformation = self._data_preprocess(
        data_path,
        chunk_size,
        chunk_overlap,
        split_type=split_type,
        )
        pipline = IngestionPipeline(transformations=transformation)
        nodes = pipline.run(documents=documents, show_progress=True, num_workers=1)
        return nodes
        
    
    def _data_preprocess(
        self,
        data_path=None,
        chunk_size=1024,
        chunk_overlap=50,
        split_type=0,  # 0-->Sentence 1-->Hierarchical
    ) -> List[TransformComponent]:
        if split_type == 0:
            parser = SentenceSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                include_prev_next_rel=True,
            )
        else:
            parser = HierarchicalNodeParser.from_defaults(
                chunk_sizes=[chunk_size * 4, chunk_size],
                chunk_overlap=chunk_overlap,
            )
        transformation = [
            ##支持多种抽取策略，也可以二次开发，主要是对node元数据进行定制化操作，比如建立node之间的关系、实体之间的关系等
            # SentenceSplitter(),
            # TitleExtractor(nodes=5),
            # QuestionsAnsweredExtractor(questions=3),
            # SummaryExtractor(summaries=["prev", "self"]),
            # KeywordExtractor(keywords=10),
            # EntityExtractor(prediction_threshold=0.5),
            parser
        ]
        return transformation
