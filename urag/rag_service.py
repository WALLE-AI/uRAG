import datetime
from itertools import islice
from typing import List
import loguru
from metaknowledge.datasource.retrieval_service import RetrievalService
from entities.document import Document
from models.llm import LLMApi
from prompt.search_prompt import _rewrite_question_qa_prompt,_rewrite_question_qa_prompt_zh,_rag_system_prompt_zh,_rag_system_prompt,_rag_qa_prompt,_rag_qa_prompt_zh

REDUCE_TOKEN_FACTOR = 0.5  # Reduce the token occupancy to less than the model upper tokens.
TOKEN_TO_CHAR_RATIO = 4  # The ratio of the number of tokens to the number of characters.
MODEL_TOKEN_LIMIT = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "gpt-3.5-turbo-1106": 16384,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-1106-preview": 128000,
    "gpt-4-vision-preview": 128000,
}

class RAGService():
    def __init__(self,collection_name):
        self.desc = "RAG retriever based on transformer model"
        self.collection_name = collection_name
        self.token_upper_limit = 8196
        self.history = []
        self.question_history=[]
        self.should_do_rewrite_question = False
        self.enable_history = False
        
    def __str__(self):
        return self.desc
    
    def _self_rag(self):
        pass
    
    def reduce_tokens(self, history: List[dict]):
        """If the token occupancy is too high, we will remove the early history."""
        history_content_lens = [len(i.get("content", "").replace(" ", "")) for i in history if i]
        if len(history) > 5 and sum(history_content_lens) / TOKEN_TO_CHAR_RATIO > self.token_upper_limit:
            count = 0
            while (
                    sum(history_content_lens) / TOKEN_TO_CHAR_RATIO >
                    self.token_upper_limit * REDUCE_TOKEN_FACTOR
                    and sum(history_content_lens) > 0
            ):
                count += 1
                del history[1:3]
                history_content_lens = [len(i.get("content", "").replace(" ", "")) for i in history if i]
            loguru.logger.warning(f"To prevent token over-limit, model forgotten the early {count} turns history.")
        return history
    
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
                
        
    def contains_chinese(self,string):
        """Check if the string contains Chinese characters."""
        return any(self.is_chinese(c) for c in string)
    
    def is_chinese(self,uchar):
        """Check if the character is Chinese."""
        return '\u4e00' <= uchar <= '\u9fa5'
    
    def replace_today(prompt:str) ->str:
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        return prompt.replace("{current_date}", today)
    
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
    
    def _rewrite_question(self, query):
        """
        Gets rewrite question based on the query and response. send rewrite question to the search engine.
        """

        try:
            prompt = _rewrite_question_qa_prompt_zh if self.contains_chinese(query) else _rewrite_question_qa_prompt
            user_prompt = f"{prompt}\n\n{query}"
            loguru.logger.debug(f"rewrite_question prompt: {user_prompt}")
            response = self._call_llm(
                model_provider="openrouter",
                model_name="qwen/qwen-2.5-7b-instruct",
                messages=self.question_history + [{"role": "user", "content": user_prompt}],
                max_tokens=512,
            )
            self.question_history = self.reduce_tokens(self.question_history)
            # Append the user question to the rewrite question history.
            self.question_history.append({"role": "user", "content": user_prompt})

            new_question = response.choices[0].message.content
            loguru.logger.debug(f"question rewrite result: {new_question}")
            return new_question
        except Exception as e:
            # For any exceptions, we will just return an empty list.
            loguru.logger.error(
                "encountered error while generating rewrite question"
            )
            return query
    
    def expand_query(self, query):
        pass
    
        
    def rag(self,query):
        ##query preprocessing 什么扩展、改写等等
        ##build prompt few-shot
        ##execute llm 
        ##potsprocess response
        pass
    
