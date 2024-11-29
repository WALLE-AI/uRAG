from urag.rag_service import RAGService


def test_rag_pipline():
    query = "建造大模型"
    rag = RAGService()
    rag.rag_pipline_run(query)
    