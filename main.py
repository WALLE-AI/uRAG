import loguru

from dotenv import load_dotenv

from tests import test_rag_pipline
load_dotenv()

if __name__ == "__main__":
    loguru.logger.info("urag starting...")
    test_rag_pipline()

