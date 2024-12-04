from pathlib import Path
from entities.document import Document
from entities.extractor_type import ExtractorMethod
from metaknowledge.parser.unstructured.unstructured_doc_extractor import UnstructuredWordExtractor
from metaknowledge.parser.unstructured.unstructured_markdown_extractor import UnstructuredMarkdownExtractor
from metaknowledge.parser.unstructured.unstructured_pdf_extractor import UnstructuredPdfExtractor
    
def _is_file_format(file_path):
    input_file = Path(file_path)
    file_extension = input_file.suffix.lower()
    return file_extension


class ExtractProcessor:
    @classmethod
    def load_from_upload_file(file_path):
        pass
    
    @classmethod
    def extract(
        cls, file_path: str,config
    ) -> list[Document]:
        file_extension = _is_file_format(file_path)
        if config['extractor_type'] == ExtractorMethod.LLMAMA_INDEX.value:
            ##采用llama_index进行文本解析、chunk
            pass
        elif config['extractor_type'] == ExtractorMethod.LANGCHAIN.value:
            ##采用langchain进行文本解析、chunk
            pass
        
        elif config['extractor_type'] == ExtractorMethod.UDOCPARSER.value:
             ##采用自研的udocparser进行文本解析、chunk
            pass
        elif config['extractor_type'] == ExtractorMethod.UNSTRUCTURED.value:
            if file_extension in {".md", ".markdown"}:
                extractor = UnstructuredMarkdownExtractor(file_path, "unstructured_api_url")
            elif file_extension in {".docx",".doc"}:
                extractor = UnstructuredWordExtractor(file_path, "unstructured_api_url")
            elif file_extension == ".pdf":
                extractor = UnstructuredPdfExtractor(file_path,"unstructured_api_url")