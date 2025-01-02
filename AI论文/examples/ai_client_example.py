"""
AI连接器使用示例
"""

import asyncio
import logging
from src.config import Config
from src.ai_client.ai_connector import AIConnector

async def main():
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 加载配置
    config = Config()
    
    # 使用异步上下文管理器
    async with AIConnector(config) as ai_client:
        # 单个文本处理示例
        text = "这是一个测试文本，需要处理AI生成的特征。"
        print("\n处理单个文本:")
        try:
            async for response in ai_client.process_text(text):
                print(response, end='')
        except Exception as e:
            print(f"处理文本时出错: {e}")
            
        # 批量处理示例
        texts = [
            "第一个测试文本",
            "第二个测试文本",
            "第三个测试文本"
        ]
        print("\n\n批量处理文本:")
        try:
            async for response in ai_client.batch_process(texts):
                print(response, end='')
        except Exception as e:
            print(f"批量处理时出错: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 