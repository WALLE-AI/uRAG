import loguru

from dotenv import load_dotenv

from tests.test_rag_pipline import rag_data_build_parser_to_index, rag_dense_retrival, rag_hybrid_retriever, test_huggingface_embedding, test_storge_data

load_dotenv()

if __name__ == "__main__":
    loguru.logger.info("urag starting...")
    test_storge_data()

