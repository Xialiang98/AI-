"""
主程序入口 - AI文本处理系统
"""

import logging
import argparse
import os
from typing import Dict, List
from processor import TextProcessor
from analyzer import TopicAnalyzer
from crawler import LiteratureCrawler

def setup_logging():
    """配置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def read_input_file(file_path: str) -> str:
    """读取输入文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"读取文件失败: {str(e)}")
        raise

def save_output_file(content: str, original_file: str, suffix: str):
    """保存输出文件"""
    try:
        # 构建输出文件路径
        base_name = os.path.splitext(original_file)[0]
        output_file = f"{base_name}_SCI_{suffix}.txt"
        
        # 保存文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        logging.info(f"已保存到: {output_file}")
        
    except Exception as e:
        logging.error(f"保存文件失败: {str(e)}")
        raise

def main():
    """主函数"""
    # 设置日志
    setup_logging()
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='学术论文生成器')
    parser.add_argument('input_file', help='输入文件路径')
    args = parser.parse_args()
    
    try:
        # 1. 读取输入文件
        original_text = read_input_file(args.input_file)
        logging.info("已读取输入文件")
        
        # 2. 分析主题和关键词
        analyzer = TopicAnalyzer()
        topic_info = analyzer.analyze(original_text)
        logging.info("已完成主题分析")
        
        # 3. 爬取相关文献
        crawler = LiteratureCrawler()
        references = crawler.crawl_literature(
            topic=topic_info['topic']['en'],
            keywords=topic_info['keywords']['en']
        )
        logging.info(f"已爬取 {len(references)} 篇相关文献")
        
        # 4. 处理文本
        processor = TextProcessor()
        
        # 4.1 生成英文版
        english_paper = processor.process_english(
            original_text=original_text,
            references=references,
            topic_info=topic_info
        )
        logging.info("已生成英文版论文")
        
        # 4.2 生成中文版
        chinese_paper = processor.process_chinese(
            original_text=original_text,
            references=references,
            topic_info=topic_info
        )
        logging.info("已生成中文版论文")
        
        # 5. 保存结果
        save_output_file(english_paper, args.input_file, 'EN')
        save_output_file(chinese_paper, args.input_file, 'CN')
        
        logging.info("处理完成")
        return 0
        
    except Exception as e:
        logging.error(f"处理失败: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main()) 