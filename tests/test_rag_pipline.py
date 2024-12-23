import loguru
from config.config import init_config
from metaknowledge.extract_processor import ExtractProcessor
from metaknowledge.index_process import IndexProcess
from models.embedding import EmbeddingModel
from urag.rag_service import RAGService
from urag.retrieval_service import RetrievalService
from urag.retrievers import HybridRetriever, get_sparse_retrivers
from llama_index.core import QueryBundle


def rag_pipline():
    config = init_config()
    query = "建造大模型"
    rag = RAGService(config)
    rag.rag_pipline_run(query)
    
def rag_data_build_parser_to_index():
    file_dir = "D:/LLM/project/uRAG/data/files/"
    config = init_config()
    index_process = IndexProcess(file_path=file_dir,config=config)
    docs = index_process.extract_text()
    loguru.logger.info(f"docs size:{len(docs)}")
    # index_process.embedding_process_index(docs)
    ##
    result = get_sparse_retrivers(config,docs)
    loguru.logger.info(f"docs size:{len(result)}")
    
def rag_dense_retrival():
    config = init_config()
    query = "安全生产法有那些条例"
    all_documents = []
    # response = vec.search_by_vector(query,score_threshold=0.2)
    # reranker_reponse = RankerApi.reranker_documents(query,response)
    # loguru.logger.info(f"reponse:{reranker_reponse}")
    all_documents = RetrievalService.retrieve(query=query,config=config)
    loguru.logger.info(f"reponse:{all_documents}")

def rag_hybrid_retriever():
    file_dir = "D:/LLM/project/uRAG/data/files/"
    config = init_config()
    index_process = IndexProcess(file_path=file_dir,config=config)
    docs = index_process.extract_text()
    loguru.logger.info(f"docs size:{len(docs)}")
    sparse_retriever = get_sparse_retrivers(config,docs)
    retrivever_hybrid = HybridRetriever(sparse_retriever=sparse_retriever,dense_retriever=RetrievalService,config=config)
    query = "地基与基础如何质量验收"
    query_bundle = QueryBundle(query_str=query)
    result = retrivever_hybrid.retrieve(query_bundle=query_bundle)
    loguru.logger.info(f"docs size:{len(result)}")
    
    
def test_huggingface_embedding():
    embedding = EmbeddingModel.get_embedding("tig_embedding_api")
    text_embedding,tokens = embedding.embed_query("你是谁")
    loguru.logger.info(f"embedding tokens:{len(text_embedding)}")
    
    
    