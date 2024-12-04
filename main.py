import loguru

from dotenv import load_dotenv

from tests.test_rag_pipline import rag_pipline

load_dotenv()

if __name__ == "__main__":
    loguru.logger.info("urag starting...")
    rag_pipline()

