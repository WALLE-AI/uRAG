from config.config import init_config
from urag.rag_service import RAGService


def rag_pipline():
    config = init_config()
    query = "建造大模型"
    rag = RAGService(config)
    rag.rag_pipline_run(query)
    