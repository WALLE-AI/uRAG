from itertools import islice
from typing import List
import loguru
from urag.retrieval_service import RetrievalService
from entities.document import Document
from models.llm import LLMApi
from prompt.search_prompt import _rewrite_question_qa_prompt,_rewrite_question_qa_prompt_zh,_rag_system_prompt_zh,_rag_system_prompt,_rag_qa_prompt,_rag_qa_prompt_zh
from urag.utils.utils import get_yaml_data

class RAGService():
    def __init__(self):
        self.desc = "RAG retriever based on transformer model"
        self.config = self._init_config()
        self.collection_name = self.config["collection_name"]
        self.token_upper_limit = 8196
        self.history = []
        self.question_history=[]
        self.should_do_rewrite_question = False
        self.enable_history = False
        
    def _init_config(self):
        config_path = "config/config.yaml"
        config = get_yaml_data(config_path)
        for key in config:
            loguru.logger.info(f"{key}: {config[key]}")
        return config
        
    def __str__(self):
        return self.desc
    
    def _self_rag(self):
        pass
    
    def _rag_fusion(self):
        ##https://mp.weixin.qq.com/s/_IHUdaEOYCwmfBrz0s3ohA
        pass
    
    def ddg_search_text(self,query:str, max_results=5) -> List[Document]:
        from duckduckgo_search import DDGS
        search_results = []
        reference_results = []
        with DDGS() as ddgs:
            ddgs_gen = ddgs.text(query, backend="lite")
            for r in islice(ddgs_gen, max_results):
                search_results.append(r)
        for idx, result in enumerate(search_results):
            loguru.logger.debug(f"搜索结果{idx + 1}：{result}")
            ##[result["body"], result["href"]]
            metadata = {
                "query": query,
                "name": result["title"],
                "url": result["href"]

            }
            doc = Document(
                page_content=result["body"],
                metadata=metadata
            )
            reference_results.append(doc)
        return reference_results
    
    def _rig_rag(self):
        pass
    def _retrieve(self, query:str,reranker=False)->List[Document]:
        top_k = 5
        score = 0.5
        all_documents = []
        retravial = "semantic_search"
        all_documents = RetrievalService.retrieve(retrieval_method=retravial,docs_index=self.collection_name,query=query,
                              top_k=top_k,score_threshold=score,
                              reranking_model=reranker)
        return all_documents
    
    def _call_llm(self,model_provider:str,model_name:str,messages:List[dict],max_tokens=512,temperature=0.2,stream=True):
        response_dict = LLMApi.call_llm(prompt=messages,llm_type=model_provider,model_name=model_name,stream=stream)
        return response_dict
                

    def _build_prompt(self, query:str):
        contexts = self._retrieve(query)
        if not self.history:
            # Append the system prompt to the history, for multi turn chat.
            content = _rag_system_prompt_zh if self.contains_chinese(query) else _rag_system_prompt
            self.history.append({"role": "system", "content": content})
        prompt = _rag_qa_prompt_zh if self.contains_chinese(query) else _rag_qa_prompt
        prompt = self.replace_today(prompt)
        qa_prompt = prompt.format(
            context="\n\n".join(
                    [f"[[citation:{i + 1}]] {c.page_content}" for i, c in enumerate(contexts)]
                )
        )
        return qa_prompt
        
    def rag_pipline_run(self,query):
        ##query preprocessing 什么扩展、改写等等
        ##build prompt few-shot
        ##execute llm 
        ##potsprocess response
        pass
    
    
    
