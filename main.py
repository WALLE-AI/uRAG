import loguru

from dotenv import load_dotenv

from tests.test_rag_pipline import rag_data_build_parser_to_index, test_huggingface_embedding

load_dotenv()

if __name__ == "__main__":
    loguru.logger.info("urag starting...")
    rag_data_build_parser_to_index()

