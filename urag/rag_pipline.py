from itertools import islice
from typing import List
import loguru
from metaknowledge.index_process import IndexProcess
from urag.retrieval_service import RetrievalService
from entities.document import Document
from llama_index.core import QueryBundle
from models.llm import LLMApi
from prompt.search_prompt import _rewrite_question_qa_prompt,_rewrite_question_qa_prompt_zh,_rag_system_prompt_zh,_rag_system_prompt,_rag_qa_prompt,_rag_qa_prompt_zh
from urag.retrievers import HybridRetriever, get_sparse_retrivers
from urag.utils.utils import contains_chinese, replace_today
from utils.helper import ddg_search_text

class RAGPipline(object):
    def __init__(self,config):
        self.desc = "RAG retriever based on transformer model"
        self.config = config
        self.collection_name = self.config["collection_name"]
        self.token_upper_limit = 8196
        self.history = []
        self.question_history=[]
        self.should_do_rewrite_question = False
        self.enable_history = False
        
    def __str__(self):
        return self.desc
    
    def _self_rag(self):
        pass
    
    def _rag_fusion(self):
        ##https://mp.weixin.qq.com/s/_IHUdaEOYCwmfBrz0s3ohA
        pass
    
    def _rig_rag(self):
        pass
        
    def _retrieve(self, query:str)->List[Document]:
        ##多路召回 neo4j 向量数据库、字面匹配和图片信息
        # all_documents = []
        # all_documents = RetrievalService.retrieve(query=query,config=self.config)
        # if self.config['tools_search_api']:
        #     search_document = ddg_search_text(query)
        #     all_documents += search_document            
        # return all_documents
        file_dir = "D:/LLM/project/uRAG/data/files/"
        index_process = IndexProcess(file_path=file_dir,config=self.config)
        docs = index_process.extract_text()
        loguru.logger.info(f"docs size:{len(docs)}")
        sparse_retriever = get_sparse_retrivers(self.config,docs)
        retrivever_hybrid = HybridRetriever(sparse_retriever=sparse_retriever,dense_retriever=RetrievalService,config=self.config)
        query_bundle = QueryBundle(query_str=query)
        all_documents = retrivever_hybrid.retrieve(query_bundle=query_bundle)
        if self.config['tools_search_api']:
            search_document = ddg_search_text(query)
            all_documents += search_document            
        return all_documents
    
    def _call_llm(self,model_provider:str,model_name:str,messages:List[dict],max_tokens=512,temperature=0.2,stream=True):
        response_dict = LLMApi.call_llm(prompt=messages,llm_type=model_provider,model_name=model_name,stream=stream)
        return response_dict
                

    def _build_prompt(self, query:str):
        contexts = self._retrieve(query)
        if not self.history:
            # Append the system prompt to the history, for multi turn chat.
            content = _rag_system_prompt_zh if contains_chinese(query) else _rag_system_prompt
            self.history.append({"role": "system", "content": content})
        prompt = _rag_qa_prompt_zh if contains_chinese(query) else _rag_qa_prompt
        prompt = replace_today(prompt)
        qa_prompt = prompt.format(
            context="\n\n".join(
                    [f"[[citation:{i + 1}]] {c.page_content}" for i, c in enumerate(contexts)]
                ),
            query = query
        )
        qa_prompt = {
            "role":"user","content":qa_prompt
        }
        self.history.append(qa_prompt)
        return self.history
        
    def rag_pipline_run(self,query):
        ##query preprocessing 什么扩展、改写等等
        ##build prompt few-shot
        ##execute llm 
        ##potsprocess response
        
        model_provider = "siliconflow"
        model_name = "Qwen/Qwen2.5-7B-Instruct"
        messages = self._build_prompt(query=query)
        response_dict = self._call_llm(messages=messages,model_provider=model_provider,model_name=model_name)
        loguru.logger.info(f"reponse:{response_dict}")
        return response_dict
    
    
    
