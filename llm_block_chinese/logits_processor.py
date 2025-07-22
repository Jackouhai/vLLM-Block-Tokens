import re
import torch
from vllm.transformers_utils.tokenizer import get_tokenizer

_mask = None
_tokenizer = None

def filter_chinese(token_ids,logits):
    """
    A logits processor function to block Chinese characters.
    token_ids: list[int] - các token đã sinh trước đó
    logits: torch.Tensor - ma trận xác suất đầu ra (batch_size, vocab_size)
    """
    global _mask, _tokenizer
    if _mask is None:
        _tokenizer = get_tokenizer("Qwen/Qwen2.5-1.5B-Instruct")

        vocab_size = logits.size(-1)
        token_ids = torch.arange(vocab_size)
        decoded_tokens = _tokenizer.batch_decode(token_ids.unsqueeze(-1), skip_special_tokens = True)

        _mask = torch.tensor([
            any(0x4E00 <= ord(c) <= 0x9FFF or 0x3400 <= ord(c) <= 0x4DBF or 0xF900 <= ord(c) <= 0xFAFF for c in token) for token in decoded_tokens
        ], device=logits.device)

    logits[_mask] = -float("inf")
    return logits