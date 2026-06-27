"""统一 LLM 调用客户端（Facade）

所有 AI 请求必须经过此模块。Skill 内禁止直接调用模型 SDK。

扩展方式：新增 Provider → 更新 _build_provider() → 完成。
无需修改 Skill 代码。
"""

import logging

from app.core.config import settings
from app.llm.base import BaseLLMProvider

logger = logging.getLogger(__name__)


def _build_provider() -> BaseLLMProvider:
    """根据配置构建 LLM Provider"""
    base_url = settings.LLM_BASE_URL
    api_key = settings.LLM_API_KEY
    model = settings.LLM_MODEL
    provider_name = settings.LLM_PROVIDER

    if provider_name == "openai_compatible":
        from app.llm.providers.openai_compatible import OpenAICompatibleProvider

        return OpenAICompatibleProvider(
            base_url=base_url, api_key=api_key, model=model
        )

    # 后续扩展：
    # elif provider_name == "anthropic":
    #     from app.llm.providers.anthropic import AnthropicProvider
    #     return AnthropicProvider(...)
    # elif provider_name == "deepseek":
    #     ...使用 OpenAICompatibleProvider(base_url="https://api.deepseek.com", ...)

    raise ValueError(f"Unknown LLM provider: {provider_name}")


class LLMClient:
    """LLM 调用门面 — 委托给具体 Provider"""

    def __init__(self):
        self._provider: BaseLLMProvider | None = None

    @property
    def provider(self) -> BaseLLMProvider:
        if self._provider is None:
            self._provider = _build_provider()
        return self._provider

    @property
    def model(self) -> str:
        return self.provider.model

    async def generate(self, prompt: str, system: str | None = None) -> str:
        if not self.provider.api_key:
            raise RuntimeError("LLM_API_KEY is not configured")
        logger.info("LLMClient.generate: provider=%s", type(self.provider).__name__)
        return await self.provider.generate(prompt, system=system)


llm_client = LLMClient()
