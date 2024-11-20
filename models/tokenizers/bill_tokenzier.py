from os.path import abspath, dirname, join
from threading import Lock
from typing import Any

from transformers import GPT2Tokenizer as TransformerGPT2Tokenizer

_tokenizer = None
_lock = Lock()


class GPT2Tokenizer:
    @staticmethod
    def _get_num_tokens_by_gpt2(text: str) -> int:
        """
        use gpt2 tokenizer to get num tokens
        """
        _tokenizer = GPT2Tokenizer.get_encoder()
        tokens = _tokenizer.encode(text, verbose=False)
        return len(tokens)

    @staticmethod
    def get_num_tokens(text: str) -> int:
        return GPT2Tokenizer._get_num_tokens_by_gpt2(text)

    @staticmethod
    def get_encoder() -> Any:
        global _tokenizer, _lock
        with _lock:
            if _tokenizer is None:
                base_path = abspath(__file__)
                gpt2_tokenizer_path = join(dirname(base_path), "gpt2")
                _tokenizer = TransformerGPT2Tokenizer.from_pretrained(gpt2_tokenizer_path)

            return _tokenizer
        
     
class TiktokenTokenizer():
    def __init__(self) -> None:
        ##TODO:换成GPT2 tokenzier
        self.encoder = self._init_tiktoken()
        
    def _init_tiktoken(self) -> None:
        """
        Init TikToken encoder
        """
        import tiktoken
        encoder = tiktoken.get_encoding("cl100k_base")
        return encoder
    @classmethod
    def get_num_tokens(self,string: str) -> int:
        """Returns the number of tokens in a text string."""
        try:
            return len(self.encoder.encode(string))
        except Exception:
            return 0
    @classmethod  
    def get_num_tokens_max_len(self,string: str, max_len: int) -> str:
        """Returns truncated text if the length of text exceed max_len."""
        return self.encoder.decode(self.encoder.encode(string)[:max_len])

    
