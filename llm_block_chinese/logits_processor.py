import torch
from vllm.v1.sample.logits_processor import LogitsProcessor 
from vllm.transformers_utils.tokenizer import get_tokenizer
from typing import Optional
from vllm.v1.sample.logits_processor import BatchUpdate


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

class ChineseBlockLogitsProcessor(LogitsProcessor):
    
    def __init__(self, vllm_config, device, is_pin_memory):
        """
        Khởi tạo tokenizer và các biến. KHÔNG tạo mask ở đây.
        """
        self.tokenizer = get_tokenizer(MODEL_NAME)
        self.mask = None

    def is_argmax_invariant(self) -> bool:
        return False

    def update_state(self, batch_update: Optional[BatchUpdate]):
        """
        Phương thức trừu tượng bắt buộc. Pass vì không cần theo dõi trạng thái.
        """
        pass
    
    def apply(self, logits: torch.Tensor) -> torch.Tensor:
        """
        Áp dụng Logits Processor. Dùng lazy initialization cho mask.
        """
        if self.mask is None:
            device = logits.device
            vocab_size = logits.size(-1)
            all_token_ids = torch.arange(vocab_size)

            # Tạo mask
            decoded_tokens = self.tokenizer.batch_decode(all_token_ids.unsqueeze(-1), skip_special_tokens=True)

            # Logic chặn ký tự tiếng Trung
            self.mask = torch.tensor([
                any(0x4E00 <= ord(c) <= 0x9FFF or 0x3400 <= ord(c) <= 0x4DBF or 0xF900 <= ord(c) <= 0xFAFF for c in token)
                for token in decoded_tokens
            ], device=device, dtype=torch.bool)
        
        # Áp dụng Mask
        logits[:, self.mask] = -float("inf") 
        return logits