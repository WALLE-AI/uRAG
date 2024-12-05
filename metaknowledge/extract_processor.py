import os
from pathlib import Path

import loguru
from entities.document import Document
from entities.extractor_type import ExtractorMethod
from metaknowledge.parser.llama_index_parser import LamaIndexExtractor
from metaknowledge.parser.unstructured.unstructured_doc_extractor import UnstructuredWordExtractor
from metaknowledge.parser.unstructured.unstructured_markdown_extractor import UnstructuredMarkdownExtractor
from metaknowledge.parser.unstructured.unstructured_pdf_extractor import UnstructuredPdfExtractor
    
def _is_file_format(file_path):
    input_file = Path(file_path)
    file_extension = input_file.suffix.lower()
    return file_extension


def identify_file_types(file_or_dir_path:str):
    if not os.path.exists(file_or_dir_path) or not os.path.isdir(file_or_dir_path):
        return "Path does not exist or is not a directory"
    file_types = []
    for item in os.listdir(file_or_dir_path):
        item_path = os.path.join(file_or_dir_path, item)
        if os.path.isfile(item_path):
            # 获取文件扩展名
            _, ext = os.path.splitext(item)
            ext = ext.lower()
            file_types.append(ext)

    return file_types

def is_file_or_directory(file_or_dir_path:str):
    if not os.path.exists(file_or_dir_path):
        return loguru.logger.info(f"Path does not exist {file_or_dir_path}")
    if os.path.isfile(file_or_dir_path):
        return [file_or_dir_path]
    elif os.path.isdir(file_or_dir_path):
        return [os.path.join(file_or_dir_path, file) for file in os.listdir(file_or_dir_path) if os.path.isfile(os.path.join(file_or_dir_path, file))]
    else:
        return loguru.logger.info("Path is neither a file nor a directory")


class ExtractProcessor:
    @classmethod
    def load_from_upload_file(file_path):
        pass
    
    @classmethod
    def load_from_dir(file_path):
        ##
        pass
    
    @classmethod
    def extract_llama_index(file_or_dir_path:str):
        file_types = identify_file_types(file_or_dir_path)
        extract = LamaIndexExtractor(file_or_dir_path)
        return extract.file_extract(file_types)
    
    @classmethod
    def extract(file_or_dir_path: str,config) -> list[Document]:
        files = is_file_or_directory(file_or_dir_path)
        for file in files:
            file_extension = _is_file_format(file_or_dir_path)
            if config['extractor_type'] == ExtractorMethod.LANGCHAIN.value:
                ##采用langchain进行文本解析、chunk
                pass
            elif config['extractor_type'] == ExtractorMethod.UDOCPARSER.value:
                    ##采用自研的udocparser进行文本解析、chunk
                pass
            elif config['extractor_type'] == ExtractorMethod.UNSTRUCTURED.value:
                if file_extension in {".md", ".markdown"}:
                    extractor = UnstructuredMarkdownExtractor(file_or_dir_path, "unstructured_api_url")
                elif file_extension in {".docx",".doc"}:
                    extractor = UnstructuredWordExtractor(file_or_dir_path, "unstructured_api_url")
                elif file_extension == ".pdf":
                    extractor = UnstructuredPdfExtractor(file_or_dir_path,"unstructured_api_url")
            docs = extractor.extract()