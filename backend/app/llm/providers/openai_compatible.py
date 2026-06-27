"""OpenAI-compatible Provider

支持所有 OpenAI Chat Completions 兼容 API 的模型：
OpenAI, DeepSeek, Qwen, OpenRouter, vLLM, Ollama 等。
"""

import logging

import httpx

from app.core.config import settings
from app.llm.base import BaseLLMProvider

logger = logging.getLogger(__name__)


class OpenAICompatibleProvider(BaseLLMProvider):
    """OpenAI-compatible Chat Completions 格式"""

    async def generate(self, prompt: str, system: str | None = None) -> str:
        logger.info("Calling LLM: model=%s", self.model)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=settings.LLM_TIMEOUT) as client:
            response = await client.post(
                f"{self.base_url}{settings.LLM_API_PATH}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            logger.info("LLM response: %d chars", len(content))
            return content
