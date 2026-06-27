"""LLM Provider 抽象基类

所有 Provider 必须继承此类并实现 generate 方法。
新增模型厂商只需新增一个 Provider 文件。
"""

import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    """LLM Provider 抽象接口"""

    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        logger.info("Provider initialized: %s → %s", self.__class__.__name__, base_url)

    @abstractmethod
    async def generate(self, prompt: str, system: str | None = None) -> str:
        """生成文本。所有 Provider 必须实现此方法。"""
        ...
