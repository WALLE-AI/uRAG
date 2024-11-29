from enum import Enum


class ExtractorMethod(Enum):
    SEMANTIC_SEARCH = "llama_index"
    FULL_TEXT_SEARCH = "lanchain"
    HYBRID_SEARCH = "udocparser"