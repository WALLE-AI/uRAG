from enum import Enum


class ExtractorMethod(Enum):
    LLMAMA_INDEX = "llama_index"
    LANGCHAIN = "lanchain"
    UNSTRUCTURED ="unstructured "
    UDOCPARSER = "udocparser"