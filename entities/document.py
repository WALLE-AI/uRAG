
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel, Field


class FileMetaData(BaseModel):
    ##尽量保留较多的原文档解析数据
    id:str= ""  ##"唯一ID"
    name:str=""  ##"文档名称"
    size:str=""  ##"内存大小"
    pages:int="" ##"总页数"
    is_edit:bool=False ##是否能够编辑
    label:str="" ##"领域类似，比如建造、法律等"
    format:str="" ##文档格式 比如pdf、word等
    extra_info:Optional[dict] = Field(default_factory=dict)
    
class FilePageData(BaseModel):
    id:str="唯一ID"
    file_id:str=""
    page_content:str
    page_id:int ##页码ID
    image_page_id:str ##oss/local图片url
    
    
class FileChunkData(BaseModel):
    id:str=""##"唯一ID"
    chunk_content:str=""
    bbox_position:Optional[list]=[]
    metadata: Optional[dict] = Field(default_factory=dict) ##chunk所在页面page信息
    length:str="" ##"文本长度"
    tokens:int=0 ##"token数"
    
class FileEmbedData(BaseModel):
    id:str="" ##"唯一ID"
    text_vector: Optional[list[float]] = 0.0
    page_image_vector: Optional[list[float]] = 0.0
    fuse_vector: Optional[list[float]] = 0.0 ##向量
    metadata: Optional[dict] = Field(default_factory=dict)


class Document(BaseModel):
    """Class for storing a piece of text and associated metadata."""

    page_content: str

    vector: Optional[list[float]] = 0.0

    """Arbitrary metadata about the page content (e.g., source, relationships to other
        documents, etc.).
    """
    metadata: Optional[dict] = Field(default_factory=dict)
    '''
    retrieval score
    '''
    score: float = 0.0


class BaseDocumentTransformer(ABC):
    """Abstract base class for document transformation systems.

    A document transformation system takes a sequence of Documents and returns a
    sequence of transformed Documents.

    Example:
        .. code-block:: python

            class EmbeddingsRedundantFilter(BaseDocumentTransformer, BaseModel):
                embeddings: Embeddings
                similarity_fn: Callable = cosine_similarity
                similarity_threshold: float = 0.95

                class Config:
                    arbitrary_types_allowed = True

                def transform_documents(
                    self, documents: Sequence[Document], **kwargs: Any
                ) -> Sequence[Document]:
                    stateful_documents = get_stateful_documents(documents)
                    embedded_documents = _get_embeddings_from_stateful_docs(
                        self.embeddings, stateful_documents
                    )
                    included_idxs = _filter_similar_embeddings(
                        embedded_documents, self.similarity_fn, self.similarity_threshold
                    )
                    return [stateful_documents[i] for i in sorted(included_idxs)]

                async def atransform_documents(
                    self, documents: Sequence[Document], **kwargs: Any
                ) -> Sequence[Document]:
                    raise NotImplementedError

    """

    @abstractmethod
    def transform_documents(self, documents: Sequence[Document], **kwargs: Any) -> Sequence[Document]:
        """Transform a list of documents.

        Args:
            documents: A sequence of Documents to be transformed.

        Returns:
            A list of transformed Documents.
        """

    @abstractmethod
    async def atransform_documents(self, documents: Sequence[Document], **kwargs: Any) -> Sequence[Document]:
        """Asynchronously transform a list of documents.

        Args:
            documents: A sequence of Documents to be transformed.

        Returns:
            A list of transformed Documents.
        """
