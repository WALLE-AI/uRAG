import datetime
from typing import List

import loguru

REDUCE_TOKEN_FACTOR = 0.5  # Reduce the token occupancy to less than the model upper tokens.
TOKEN_TO_CHAR_RATIO = 4  # The ratio of the number of tokens to the number of characters.
MODEL_TOKEN_LIMIT = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "gpt-3.5-turbo-1106": 16384,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-1106-preview": 128000,
    "gpt-4-vision-preview": 128000,
}


def contains_chinese(self,string):
    """Check if the string contains Chinese characters."""
    return any(self.is_chinese(c) for c in string)

def is_chinese(self,uchar):
    """Check if the character is Chinese."""
    return '\u4e00' <= uchar <= '\u9fa5'

def replace_today(prompt:str) ->str:
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    return prompt.replace("{current_date}", today)

def reduce_tokens(self, token_upper_limit,history: List[dict]):
    """If the token occupancy is too high, we will remove the early history."""
    history_content_lens = [len(i.get("content", "").replace(" ", "")) for i in history if i]
    if len(history) > 5 and sum(history_content_lens) / TOKEN_TO_CHAR_RATIO > token_upper_limit:
        count = 0
        while (
                sum(history_content_lens) / TOKEN_TO_CHAR_RATIO >
                token_upper_limit * REDUCE_TOKEN_FACTOR
                and sum(history_content_lens) > 0
        ):
            count += 1
            del history[1:3]
            history_content_lens = [len(i.get("content", "").replace(" ", "")) for i in history if i]
        loguru.logger.warning(f"To prevent token over-limit, model forgotten the early {count} turns history.")
    return history