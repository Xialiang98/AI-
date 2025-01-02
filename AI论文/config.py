"""
配置管理模块
"""

from dataclasses import dataclass, field
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
    INPUT_FORMATS: List[str] = field(default_factory=lambda: ['.pdf', '.txt', '.docx'])
    OUTPUT_FORMAT: str = 'txt'
    
    # AI特征模式
    PATTERNS: List[str] = field(default_factory=lambda: [
        r'As an AI language model',
        r'I apologize, but I',
        r'I cannot',
        r'I do not have',
        r'I\'m sorry, but',
        r'I am not able to',
        r'I must inform you',
        r'Please note that',
        r'It\'s important to note',
        r'I would recommend',
        r'I suggest',
        r'In my opinion',
        r'Based on my understanding',
        r'From my perspective',
        r'As far as I know',
        r'To the best of my knowledge'
    ])
    
    # 处理选项
    OPTIONS: Dict[str, Any] = field(default_factory=lambda: {
        'preserve_format': True,    # 保持格式
        'keep_structure': True,     # 保持结构
        'optimize_memory': True,    # 内存优化
        'remove_headers': True,     # 移除页眉页脚
        'merge_paragraphs': False,  # 合并段落
        'clean_spacing': True,      # 清理多余空格
        'normalize_quotes': True,   # 规范化引号
        'fix_punctuation': True,    # 修正标点符号
        'remove_duplicates': True   # 移除重复内容
    })
    
    # 要移除的机械化表达
    MECHANICAL_PHRASES: List[str] = field(default_factory=lambda: [
        "然而", "However",
        "首先", "First",
        "其次", "Second",
        "总结", "In summary",
        "随后", "Subsequently",
        "总而言之", "In conclusion",
        "最后", "Finally",
        "此外", "Moreover",
        "因此", "Therefore",
        "总之", "In general",
        "尤其是", "Especially",
        "另外", "Additionally",
        "这个", "This",
        "**", "*",
        "特别是", "Particularly",
        "值得注意的是", "Notably",
        "需要指出的是", "It should be noted",
        "不难发现", "It is easy to find",
        "通过分析", "Through analysis",
        "根据上述", "Based on the above",
        "由此可见", "Thus it can be seen",
        "综上所述", "In summary"
    ])
    
    # OpenAI API配置
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    # 英文系统提示词
    SYSTEM_PROMPT_EN: str = """You are a distinguished scholar who has published multiple papers in top journals like Nature/Science and serves as a senior reviewer for SCI journals. Your task is to write a high-quality academic paper in English based on the provided information.

Requirements:

1. Paper Quality:
   - Deeply understand and explore the core ideas and research value
   - Write according to the highest standards of SCI journals
   - Demonstrate profound academic insights and innovative thinking
   - Ensure rigorous argumentation and clear logic
   - Use the latest research methods and theoretical frameworks
   - Provide specific and feasible solutions
   - Analyze the essence and impact of problems
   - Establish systematic theoretical frameworks
   - Provide sufficient experimental data support
   - Conduct in-depth quantitative and qualitative analysis
   - Demonstrate research innovation and importance
   - Emphasize theoretical and practical value

2. Writing Style:
   - Maintain professional and rigorous academic writing style
   - Completely avoid mechanical transition words
   - Use natural, fluent, and elegant language
   - Employ discipline-specific academic terminology
   - Connect contexts naturally
   - Drive writing with research findings
   - Advance arguments with data and analysis
   - Ensure terminology accuracy
   - Maintain coherence and hierarchy in argumentation
   - Focus on logical connections between paragraphs
   - Emphasize progressive relationships between arguments

3. Paper Structure:
   - Title
   - Abstract
   - Keywords
   - Introduction
   - Literature Review
   - Theoretical Framework
   - Materials and Methods
   - Results
   - Discussion
   - Practical Implications
   - Conclusion
   - References

4. Innovation Requirements:
   - Present original insights and viewpoints
   - Establish new theoretical frameworks or models
   - Discover new research questions or directions
   - Provide unique solutions
   - Extend boundaries of existing research
   - Propose new research methods or tools
   - Discover new research patterns
   - Innovatively solve practical problems

5. Academic Standards:
   - Ensure all arguments are supported by sufficient evidence
   - Accurately cite and review relevant literature
   - Objectively evaluate other research
   - Clearly state research limitations
   - Follow academic ethical norms
   - Maintain paper originality
   - Ensure data authenticity and reliability
   - Strictly follow research methods
   - Guarantee reasoning rigor
   - Ensure conclusion reliability
   - Avoid overgeneralization
   - Mind research boundaries"""

    # 中文系统提示词
    SYSTEM_PROMPT_CN: str = """你是一位在Nature/Science等顶级期刊发表过多篇论文的资深学者，同时也是SCI期刊的资深审稿人。你的任务是基于提供的信息，用中文撰写一篇最高水平的学术论文。

要求如下：

1. 论文质量要求：
   - 完全理解并深入挖掘核心思想和研究价值
   - 按照最高标准SCI期刊的要求撰写
   - 展现深刻的学术洞见和创新性思维
   - 确保论证严密、逻辑清晰
   - 使用最新的研究方法和理论框架
   - 提供具体可行的解决方案
   - 深入分析问题的本质和影响
   - 建立系统的理论框架
   - 提供充分的实验数据支持
   - 进行深入的定量和定性分析
   - 展示研究的创新性和重要性
   - 强调研究的理论和实践价值

2. 写作风格要求：
   - 保持专业、严谨的学术写作风格
   - 完全避免使用机械化的过渡词
   - 使用自然流畅、优雅的语言
   - 采用学科专有的学术用语
   - 通过上下文自然衔接
   - 以研究发现驱动行文
   - 用数据和分析推动论述
   - 确保术语使用的准确性
   - 保持论述的连贯性和层次性
   - 注重段落之间的逻辑衔接
   - 强调论点的递进关系

3. 论文结构要求：
   - 标题
   - 摘要
   - 关键词
   - 引言
   - 文献综述
   - 理论框架
   - 材料与方法
   - 研究结果
   - 讨论
   - 实践启示
   - 结论
   - 参考文献

4. 创新性要求：
   - 提出原创性的见解和观点
   - 建立新的理论框架或模型
   - 发现新的研究问题或方向
   - 提供独特的解决方案
   - 拓展现有研究的边界
   - 提出新的研究方法或工具
   - 发现新的研究规律或模式
   - 创新性地解决实际问题

5. 学术规范要求：
   - 确保所有论述有充分的证据支持
   - 准确引用和评述相关文献
   - 客观公正地评价其他研究
   - 清晰说明研究局限性
   - 遵守学术伦理规范
   - 保持论文的原创性
   - 确保数据的真实性和可靠性
   - 严格遵循研究方法
   - 保证推理的严密性
   - 确保结论的可靠性
   - 避免过度推广
   - 注意研究的边界"""

    # 需要移除的机械化词语
    MECHANICAL_PHRASES: List[str] = field(default_factory=lambda: [
        # 中文过渡词
        "然而", "首先", "其次", "总结", "随后", "总而言之",
        "总之", "尤其是", "另外", "这个", "特别是", "值得注意的是",
        "需要指出的是", "不难发现", "通过分析", "根据上述", "由此可见",
        "综上所述", "因此", "所以", "但是", "不过", "接着", "最后",
        "此外", "同时", "此时", "从而", "于是", "故而", "以及",
        "并且", "而且", "不仅如此", "除此之外", "换句话说", "换言之",
        "简言之", "具体来说", "具体而言", "总的来说", "总的来看",
        "事实上", "显然", "显而易见", "毫无疑问", "众所周知",
        "一般来说", "一般而言", "一般来讲", "通常来说", "通常而言",
        
        # English transition words
        "However", "First", "Second", "In summary", "Subsequently",
        "In conclusion", "Therefore", "Especially", "Additionally",
        "This", "Particularly", "It is worth noting", "It should be noted",
        "Through analysis", "Based on the above", "Thus", "Hence",
        "Moreover", "Furthermore", "Nevertheless", "Nonetheless",
        "Meanwhile", "Consequently", "As a result", "In addition",
        "Besides", "In other words", "That is to say", "In brief",
        "Specifically", "Generally speaking", "In general", "Obviously",
        "Evidently", "Without doubt", "As is known to all",
        "Usually", "Typically", "Normally", "In most cases"
    ])
    
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
            
        if not self.PATTERNS:
            raise ValueError("AI特征模式列表不能为空")
            
        if not isinstance(self.OPTIONS, dict):
            raise ValueError("处理选项必须是字典类型")
            
        if not self.OPENAI_API_KEY or self.OPENAI_API_KEY == "YOUR-API-KEY-HERE":
            raise ValueError("请设置有效的OpenAI API密钥")
            
        if not isinstance(self.MAX_WORKERS, int) or self.MAX_WORKERS <= 0:
            raise ValueError("MAX_WORKERS必须是正整数")
            
        if not isinstance(self.BATCH_SIZE, int) or self.BATCH_SIZE <= 0:
            raise ValueError("BATCH_SIZE必须是正整数")
            
        if not isinstance(self.MEMORY_LIMIT, str) or not self.MEMORY_LIMIT.endswith(("G", "M")):
            raise ValueError("MEMORY_LIMIT必须是以G或M结尾的字符串") 