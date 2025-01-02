"""
AI连接器模块 - 负责与AI服务的通信
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Any, AsyncGenerator
from config import Config

class AIConnector:
    """AI服务连接器"""
    
    def __init__(self, config: Config):
        """
        初始化AI连接器
        
        Args:
            config: 配置对象
        """
        self.config = config
        self.base_url = "https://gpt-5.vip"
        self.headers = {
            'Authorization': config.AI_API_KEY,
            'User-Agent': 'AI-Text-Processor/1.0',
            'Content-Type': 'application/json',
            'Accept': '*/*',
        }
        self.session = None
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            base_url=self.base_url,
            headers=self.headers
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()

    async def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """
        发送请求到AI服务
        
        Args:
            endpoint: API端点
            payload: 请求数据
            
        Yields:
            AI响应的数据流
        """
        retries = self.config.MAX_RETRIES
        while retries > 0:
            try:
                async with self.session.post(endpoint, json=payload) as response:
                    if response.status == 200:
                        async for line in response.content.iter_any():
                            if line:
                                yield line.decode('utf-8')
                    else:
                        error_msg = await response.text()
                        self.logger.error(f"API请求失败: {error_msg}")
                        raise Exception(f"API请求失败: {response.status} - {error_msg}")
                break
            except Exception as e:
                retries -= 1
                if retries == 0:
                    raise
                self.logger.warning(f"请求失败，剩余重试次数: {retries}, 错误: {str(e)}")
                await asyncio.sleep(self.config.RETRY_DELAY)

    async def process_text(self, text: str) -> AsyncGenerator[str, None]:
        """
        处理文本
        
        Args:
            text: 输入文本
            
        Yields:
            处理后的文本流
        """
        payload = {
            "model": self.config.AI_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ],
            "stream": True
        }
        
        try:
            async for response in self._make_request("/v1/chat/completions", payload):
                yield response
        except Exception as e:
            self.logger.error(f"处理文本时出错: {str(e)}")
            raise

    async def batch_process(self, texts: list[str]) -> AsyncGenerator[str, None]:
        """
        批量处理文本
        
        Args:
            texts: 文本列表
            
        Yields:
            处理后的文本流
        """
        tasks = [self.process_text(text) for text in texts]
        async for result in asyncio.as_completed(tasks):
            try:
                async for response in result:
                    yield response
            except Exception as e:
                self.logger.error(f"批量处理时出错: {str(e)}")
                continue 