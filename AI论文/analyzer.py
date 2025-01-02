import logging
from typing import Dict, List
import jieba
import jieba.analyse
from collections import Counter
import re
from textblob import TextBlob
from gensim import corpora, models
import numpy as np

logger = logging.getLogger(__name__)

class TopicAnalyzer:
    """主题分析器，负责分析文章主题和提取关键词"""
    
    def __init__(self):
        # 加载停用词
        self.stopwords = self._load_stopwords()
        
        # 初始化jieba分析器
        jieba.initialize()
        
    def analyze(self, text: str) -> Dict:
        """
        分析文章主题和关键词
        
        Args:
            text: 待分析的文本
            
        Returns:
            Dict: 包含主题、关键词等信息的字典
        """
        try:
            # 预处理文本
            cleaned_text = self._preprocess_text(text)
            
            # 分离中英文
            chinese_text, english_text = self._split_languages(cleaned_text)
            
            # 分析主题
            chinese_topic = self._analyze_chinese_topic(chinese_text)
            english_topic = self._analyze_english_topic(english_text)
            
            # 提取关键词
            chinese_keywords = self._extract_chinese_keywords(chinese_text)
            english_keywords = self._extract_english_keywords(english_text)
            
            # 合并结果
            result = {
                'topic': {
                    'en': english_topic,
                    'cn': chinese_topic
                },
                'keywords': {
                    'en': english_keywords,
                    'cn': chinese_keywords
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"分析文章主题时出错: {str(e)}")
            return {
                'topic': {'en': '', 'cn': ''},
                'keywords': {'en': [], 'cn': []}
            }
            
    def _load_stopwords(self) -> set:
        """加载停用词"""
        try:
            # 这里应该从文件加载停用词表
            # 现在使用一个简单的示例
            return {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
                '的', '了', '和', '与', '及', '或', '而', '等', '中', '在'
            }
        except Exception as e:
            logger.error(f"加载停用词时出错: {str(e)}")
            return set()
            
    def _preprocess_text(self, text: str) -> str:
        """预处理文本"""
        # 移除URL
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        
        # 统一空白字符
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
        
    def _split_languages(self, text: str) -> tuple:
        """分离中英文"""
        chinese = ''.join(re.findall(r'[\u4e00-\u9fff]+', text))
        english = ''.join(re.findall(r'[a-zA-Z]+', text))
        return chinese, english
        
    def _analyze_chinese_topic(self, text: str) -> str:
        """分析中文主题"""
        try:
            # 使用jieba进行分词
            words = jieba.cut(text)
            words = [w for w in words if w not in self.stopwords]
            
            # 使用TF-IDF提取主题词
            tfidf = jieba.analyse.extract_tags(
                text,
                topK=5,
                withWeight=True
            )
            
            # 返回权重最高的词作为主题
            return tfidf[0][0] if tfidf else ''
            
        except Exception as e:
            logger.error(f"分析中文主题时出错: {str(e)}")
            return ''
            
    def _analyze_english_topic(self, text: str) -> str:
        """分析英文主题"""
        try:
            # 使用TextBlob进行词性标注
            blob = TextBlob(text)
            
            # 提取名词短语
            noun_phrases = blob.noun_phrases
            
            # 统计词频
            phrase_counts = Counter(noun_phrases)
            
            # 返回最常见的名词短语作为主题
            most_common = phrase_counts.most_common(1)
            return most_common[0][0] if most_common else ''
            
        except Exception as e:
            logger.error(f"分析英文主题时出错: {str(e)}")
            return ''
            
    def _extract_chinese_keywords(self, text: str) -> List[str]:
        """提取中文关键词"""
        try:
            # 使用jieba提取关键词
            keywords = jieba.analyse.extract_tags(
                text,
                topK=10,
                withWeight=False
            )
            return keywords
            
        except Exception as e:
            logger.error(f"提取中文关键词时出错: {str(e)}")
            return []
            
    def _extract_english_keywords(self, text: str) -> List[str]:
        """提取英文关键词"""
        try:
            # 使用TextBlob进行词性标注
            blob = TextBlob(text)
            
            # 提取名词和形容词
            words = [word for (word, tag) in blob.tags if tag.startswith(('NN', 'JJ'))]
            
            # 统计词频
            word_counts = Counter(words)
            
            # 返回最常见的10个词
            return [word for word, _ in word_counts.most_common(10)]
            
        except Exception as e:
            logger.error(f"提取英文关键词时出错: {str(e)}")
            return [] 