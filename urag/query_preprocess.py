##Query预处理 主要重写 扩写等等

import loguru
from models.llm import LLMApi
from prompt.search_prompt import _rewrite_question_qa_prompt,_rewrite_question_qa_prompt_zh,_rag_system_prompt_zh,_rag_system_prompt,_rag_qa_prompt,_rag_qa_prompt_zh
from urag.utils.utils import contains_chinese

class QueryProcessor(object):
    def __init__(self):
        self.desc = "Prompt for query processing"
    def __str__(self) -> str:
        return self.desc
    
    def _call_llm(self,model_provider:str,model_name:str,messages:List[dict],max_tokens=512,temperature=0.2,stream=True):
        response_dict = LLMApi.call_llm(prompt=messages,llm_type=model_provider,model_name=model_name,stream=stream)
        return response_dict
    
    def _rewrite_question(self, query):
        """
        Gets rewrite question based on the query and response. send rewrite question to the search engine.
        """

        try:
            prompt = _rewrite_question_qa_prompt_zh if contains_chinese(query) else _rewrite_question_qa_prompt
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
        ##如何扩写
        pass