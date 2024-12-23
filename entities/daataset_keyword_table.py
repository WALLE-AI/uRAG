import json
from typing import List, Optional
import uuid
import loguru
from pydantic import BaseModel, Field

from metaknowledge import storage


class DatasetKeywordTable(BaseModel):
    id:str=Field(
        default_factory=lambda: str(uuid.uuid4()), description="Unique ID of the node."
    )
    keyword_table: str = Field(default="", description="Text content of the node.")
    data_source_type:str = Field(default="", description="Text content of the node.")
    
    @property
    def keyword_table_dict(self):
        class SetDecoder(json.JSONDecoder):
            def __init__(self, *args, **kwargs):
                super().__init__(object_hook=self.object_hook, *args, **kwargs)

            def object_hook(self, dct):
                if isinstance(dct, dict):
                    for keyword, node_idxs in dct.items():
                        if isinstance(node_idxs, list):
                            dct[keyword] = set(node_idxs)
                return dct
        tenant_id = ""
        dataset_id=""
        if self.data_source_type == "database":
            return json.loads(self.keyword_table, cls=SetDecoder) if self.keyword_table else None
        else:
            file_key = "keyword_files/" + tenant_id + "/" + dataset_id + ".txt"
            try:
                keyword_table_text = storage.load_once(file_key)
                if keyword_table_text:
                    return json.loads(keyword_table_text.decode("utf-8"), cls=SetDecoder)
                return None
            except Exception as e:
                loguru.logger.exception(f"Failed to load keyword table from file: {file_key}")
                return None