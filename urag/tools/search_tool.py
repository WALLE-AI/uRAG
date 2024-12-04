from itertools import islice
from typing import List
import loguru
from duckduckgo_search import DDGS

from entities.document import Document


def ddg_search_text(query:str, max_results=5) -> List[Document]:

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