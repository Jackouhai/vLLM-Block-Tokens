#  vLLM Logits Processor: Block Chinese Characters

A custom `logits processor` for vLLM to **block Chinese token generation** during text generation.

---

##  Features

✅ Automatically identifies Chinese tokens in the vocabulary.

✅ Uses batch_decode + Unicode ranges to detect Chinese tokens.

✅ Masks Chinese tokens via logits[token_id] = -inf.

✅ Plug-and-play support with vLLM using --logits-processor-pattern.

---

## 🗂️ Project Structure
```bash
llm-block-chinese/
├── llm_block_chinese/           # Contains the main logits processor code
│   └── logits_processor.py      # filter_chinese() implementation
├── .gitignore                   # Git ignore rules
├── .python-version              # Python version for uv environment
├── README.md                    # Project documentation
├── main.py                      # Script to send test prompts
├── pyproject.toml               # Project dependencies and uv config
├── uv.lock                      # Locked dependency versions (managed by uv)

```

##  Yêu cầu

Python ≥ 3.10

CUDA + compatible GPU driver installed

A model supported by vLLM (e.g., Qwen/Qwen2.5-1.5B-Instruct)

Installed vllm and torch

---

## ⚙️ Cài đặt

### 1. Cài `uv` (nếu chưa có)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Full Setup (environment and requirements)

```bash
uv sync
```

### 3. Run vLLM server

```bash
source .venv/bin/activate
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-1.5B-Instruct \
  --served-model-name qwen2.5 \
  --port 8000 \
  --logits-processor-pattern "llm_block_chinese\.logits_processor\.filter_chinese"
```
If not enough vram (e.g., NVIDIA T600-Laptop):
```bash
source .venv/bin/activate
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-1.5B-Instruct \
  --served-model-name qwen2.5 \
  --port 8000 \
  --logits-processor-pattern "llm_block_chinese\.logits_processor\.filter_chinese" \
  --cpu-offload-gb 2 \
  --max-model-len 2048
```








