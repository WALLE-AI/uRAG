import loguru
from config.config import init_config
from metaknowledge.extract_processor import ExtractProcessor
from metaknowledge.index_process import IndexProcess
from models.embedding import EmbeddingModel
from urag.rag_service import RAGService


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
    index_process.embedding_process_index(docs)
    
    
def test_huggingface_embedding():
    embedding = EmbeddingModel.get_embedding("huggingface_embedding")
    text_embedding,tokens = embedding.embed_query("你是谁")
    
    
    
    