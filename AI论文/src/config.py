"""
配置管理模块
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import os
import json

@dataclass
class Config:
    """配置类"""
    
    # AI配置
    AI_API_KEY: str = ""
    AI_MODEL: str = "gpt-4o-mini"
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 1
    
    # 系统配置
    MAX_WORKERS: int = 16
    BATCH_SIZE: int = 1000
    MEMORY_LIMIT: int = 512  # MB
    
    # 性能配置
    CACHE_SIZE: int = 100
    TIMEOUT: int = 30
    
    # 文件配置
    INPUT_FORMATS: List[str] = ['.pdf', '.txt', '.docx']
    OUTPUT_FORMAT: str = 'txt'
    
    # AI特征模式
    PATTERNS: List[str] = [
        r'pattern1',
        r'pattern2',
    ]
    
    # 处理选项
    OPTIONS: Dict[str, Any] = {
        'preserve_format': True,
        'keep_structure': True,
        'optimize_memory': True
    }
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'Config':
        """从文件加载配置"""
        if not os.path.exists(config_path):
            return cls()
            
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            return cls(**config_data)
            
    def save_to_file(self, config_path: str):
        """保存配置到文件"""
        config_data = {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
            
    def validate(self):
        """验证配置有效性"""
        if not self.AI_API_KEY:
            raise ValueError("AI API密钥不能为空")
            
        if self.MAX_WORKERS < 1:
            raise ValueError("最大工作线程数必须大于0")
            
        if self.BATCH_SIZE < 1:
            raise ValueError("批处理大小必须大于0")
            
        if self.MEMORY_LIMIT < 64:
            raise ValueError("内存限制不能小于64MB") 