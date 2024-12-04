from pathlib import Path
from typing import List
import uuid

import loguru
from tqdm import tqdm
from entities.document import Document
from metaknowledge.datasource.vector_factory import Vector
from utils.helper import get_directory_all_markdown_files


class IndexProcess():
    def __init__(self,file_path,index_name):
        self.desc = "index processing"
        self.vdb = Vector(index_name)
        self.file_path = file_path
        self.etl_type = "Unstructured"
    def __str__(self) -> str:
        return self.desc
    
    def extract_text(self):
        # docs = ExtractProcessor.extract(self.file_path,self.etl_type)
        # return self._preproces_docs_metadata(docs)
        ##调用docparse模块直接得到chunk
        pass
    
    def _preproces_docs_metadata(self,docs:List[Document]) -> List[Document]:
        file_name = Path(self.file_path).stem.split("_")[-1]
        for doc in docs:
            # token_num = LLMApi._get_num_tokens_by_gpt2(doc.page_content)
            #TODO:chunk_size大小要考虑到embedding model embedding context lengt
            metadata = {
                    "doc_id":str(uuid.uuid4()),
                    "file_name":file_name
                }
            doc.metadata.update(metadata)
        return docs
            
    def late_chunking_embedding():
        pass
    
    def meta_chunking_embedding():
        pass
    def embedding_process_index(self, docs:List[Document]):
        self.vdb.create(docs)
        
         
def test_markdown_file_embedding():
    markdown_files_dir = "data/markdown/"
    markdonw_files = get_directory_all_markdown_files(markdown_files_dir)
    collection_name =  "Vector_index_markdown_"+str(uuid.uuid4())+"_Node"
    chunk_docs_len = 0
    for file in tqdm(markdonw_files):
        process = IndexProcess(file,collection_name)
        docs = process.extract_text()
        chunk_docs_len += len(docs)
        loguru.logger.info(f"markdown_files embedding {file}")
        process.embedding_process_index(docs)
    loguru.logger.info(f"collection_name:{collection_name}")
    loguru.logger.info(f"embeding insert start docs:{len(docs)}")
        
        
# def test_markdon_file_rag():
#     collection_name = "Vector_index_markdown_20756a9b-7316-4024-8603-f5a56391cd05_Node"
#     rag = RAGService(collection_name)
#     question_list = ["建筑大模型","建筑加固工程质量验收主要讲的是什么"]
#     for question in question_list:
#         context = rag._retrieve(question,reranker=True)
#         loguru.logger.info(f"context:{context}")
    
    
    
    
        


        
        
        