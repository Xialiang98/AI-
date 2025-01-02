# 学术论文生成系统 - 开发文档
 By乾元

## 项目概述

本项目是一个基于AI的学术论文生成系统，主要功能包括：
1. 基于用户输入的主题进行文献爬取
2. 智能分析文本主题和关键词
3. 生成中英文学术论文
4. 自动引用相关文献

## 系统架构

### 核心模块

1. `main.py` - 主程序入口
   - 命令行参数解析
   - 工作流程控制
   - 文件读写操作
   - 错误处理和日志记录

2. `crawler.py` - 文献爬虫模块
   - 基于秘塔搜索的文献获取
   - 自动化网页操作（Edge浏览器）
   - 文献数据解析和清洗
   - 异常处理和重试机制

3. `analyzer.py` - 主题分析模块
   - 文本主题提取
   - 关键词识别
   - 中英文处理
   - 语义分析

4. `processor.py` - 论文处理模块
   - 论文格式化处理
   - 中英文论文生成
   - 参考文献整合
   - 文本优化

5. `config.py` - 配置管理
   - 系统配置参数
   - 爬虫配置
   - 文本处理规则
   - 输出格式设置
6.requirements.txt为依赖文件
7.请拉取本项目后执行此文件的依赖命令安装
## 技术实现

### 1. 文献爬取

#### 实现原理
1. 使用 Selenium 和 Edge WebDriver 实现自动化操作
2. 通过秘塔搜索获取学术文献
3. 智能等待和重试机制
4. 文献数据解析和存储

#### 关键代码
```python
def crawl_literature(self, topic: str, keywords: List[str], num_papers: int = 20):
    # 初始化浏览器
    self._setup_driver()
    
    # 构建搜索查询
    search_query = f"{topic} {' '.join(keywords)} 参考文献"
    
    # 执行搜索和数据获取
    self._search_metaso(search_query)
    
    # 解析搜索结果
    papers = self._parse_search_results(self.driver)
    
    return papers[:num_papers]
```

### 2. 主题分析

#### 实现原理
1. 使用jieba分词进行中文处理
2. 基于textblob进行英文处理
3. 关键词提取和权重计算
4. 主题相关度分析

#### 关键功能
- 中英文关键词提取
- 主题分类和聚类
- 文本相似度计算
- 语义理解和分析

### 3. 论文生成

#### 实现原理
1. 模板化论文结构
2. 智能段落组织
3. 参考文献自动引用
4. 中英文格式适配

#### 处理流程
1. 解析原始输入
2. 提取核心内容
3. 整合参考文献
4. 生成目标论文

## 部署说明

### 1. 环境要求
- Python 3.8+
- Edge浏览器
- 内存 8GB+
- 操作系统：Windows 10/11
- ### 2. 运行测试
```bash
python test_crawler.py  # 测试爬虫功能
python test_analyzer.py # 测试分析功能
```

## 使用指南

### 1. 基本用法
```bash
python main.py input.txt
```

### 2. 参数说明
- `input_file`: 输入文件路径
- 输出文件将自动生成在相同目录下
  - `*_SCI_EN.txt`: 英文版论文
  - `*_SCI_CN.txt`: 中文版论文

## 开发规范

### 1. 代码风格
- 遵循PEP 8规范
- 使用类型注解
- 添加详细注释
- 使用英文编写代码和注释

### 2. 错误处理
- 使用try-except捕获异常
- 记录详细错误日志
- 实现错误重试机制
- 优雅降级处理

### 3. 日志规范
- 使用logging模块
- 记录关键操作步骤
- 错误信息需要详细
- 包含时间戳和级别

## 维护指南

### 1. 常见问题
- 爬虫无法获取数据
  - 检查网络连接
  - 验证选择器是否更新
  - 确认浏览器驱动版本
  
- 主题分析不准确
  - 调整关键词权重
  - 优化分词规则
  - 更新停用词表

- 论文生成质量问题
  - 检查模板配置
  - 优化文本处理规则
  - 调整参考文献引用

### 2. 性能优化
- 使用异步处理
- 实现并发爬取
- 优化内存使用
- 添加缓存机制

### 3. 更新维护
- 定期更新依赖
- 监控系统性能
- 备份重要数据
- 记录更新日志

## 版本历史

### v1.0.0 (2024-01-01)
- 初始版本发布
- 实现基础爬虫功能
- 支持中英文论文生成
- 完成主题分析模块

### v1.0.1 (2024-01-02)
- 优化爬虫稳定性
- 改进文献解析算法
- 添加日志记录
- 修复已知问题 
### 开发者联系方式：
<img src="https://img1.lookpic.cn/2025/01/02/_20250102164849.jpeg" alt="微信截图 20250102164849" border="0">
### 本项目须知：
1.任何作弊手段都是可耻的，本项目只是展示一种可能性
2.本项目采用Python进行开发，效果展示效果图为：
![微信截图_20250102164849.png](https://img.picui.cn/free/2025/01/02/677653018d405.png)

