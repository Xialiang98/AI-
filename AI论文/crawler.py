"""
学术文献爬虫模块 - 用于获取相关参考文献并生成论文
"""

import logging
from typing import List, Dict
import time
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import re
import urllib.parse
import os

logger = logging.getLogger(__name__)

class LiteratureCrawler:
    """文献爬虫类，使用秘塔搜索获取相关文献"""
    
    def __init__(self):
        """初始化爬虫"""
        self.driver = None
        self.base_url = "https://metaso.cn"
        self.wait_timeout = 10
        # 创建output目录（如果不存在）
        if not os.path.exists('output'):
            os.makedirs('output')
            
    def save_references(self, papers: List[Dict], output_file: str = "output/references.txt"):
        """保存参考文献到文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# 参考文献列表\n\n")
                for i, paper in enumerate(papers, 1):
                    f.write(f"## 文献 {i}\n")
                    f.write(f"标题: {paper['title']}\n")
                    if paper['date']:
                        f.write(f"日期: {paper['date']}\n")
                    f.write(f"来源: {paper['source']}\n")
                    f.write(f"内容:\n{paper['content']}\n")
                    f.write("\n" + "-"*80 + "\n\n")
            logger.info(f"参考文献已保存到: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"保存参考文献时出错: {str(e)}")
            return None
            
    def _setup_driver(self):
        """设置浏览器驱动"""
        try:
            # 使用 Edge
            options = webdriver.EdgeOptions()
            
            # 基本设置
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
            
            # 设置用户代理
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.2849.56')
            
            # 创建服务
            service = EdgeService(EdgeChromiumDriverManager().install())
            
            # 初始化驱动
            self.driver = webdriver.Edge(service=service, options=options)
            
            # 设置页面加载超时
            self.driver.set_page_load_timeout(30)
            
            logger.info("Edge 浏览器初始化成功")
            
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}")
            raise
                
    def _close_driver(self):
        """关闭浏览器驱动"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("浏览器已关闭")
            except Exception as e:
                logger.error(f"关闭浏览器失败: {str(e)}")
            finally:
                self.driver = None
                
    def _search_metaso(self, query: str):
        """在秘塔搜索中执行搜索"""
        try:
            # 访问秘塔搜索
            logger.info(f"正在访问: {self.base_url}")
            self.driver.get(self.base_url)
            logger.info("已访问秘塔搜索首页")
            
            # 等待用户登录
            input("请先完成登录，完成后按回车继续...")
            logger.info("用户已确认登录完成")
            
            # 等待页面加载
            time.sleep(5)
            
            # 定位搜索框
            search_box = WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.search-consult-textarea"))
            )
            
            # 清空搜索框并输入查询
            search_box.clear()
            search_box.send_keys(query)
            logger.info(f"已输入搜索词: {query}")
            
            # 模拟按下回车键
            search_box.send_keys(Keys.RETURN)
            logger.info("已按下回车键")
            
            # 等待搜索结果加载
            time.sleep(40)
            
            # 点击"学术"按钮
            try:
                academic_button = WebDriverWait(self.driver, self.wait_timeout * 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiTab-root.search-domain-kits_search-domain-tab__4O_vu"))
                )
                academic_button.click()
                logger.info("已点击学术按钮")
                time.sleep(10)
            except Exception as e:
                logger.error(f"点击学术按钮失败: {str(e)}")
                raise
                
            # 点击参考文献链接
            try:
                reference_button = WebDriverWait(self.driver, self.wait_timeout * 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Search_answer-link-btn__Od5C7"))
                )
                reference_button.click()
                logger.info("已点击参考文献链接")
                time.sleep(10)
            except Exception as e:
                logger.error(f"点击参考文献链接失败: {str(e)}")
                raise
            
            # 等待数据加载完成
            try:
                WebDriverWait(self.driver, self.wait_timeout * 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#search-page-scroller > div > div > div.MuiStack-root.Search_search-result__louwQ"))
                )
                logger.info("数据加载完成")
            except Exception as e:
                logger.error(f"等待数据加载失败: {str(e)}")
                raise
                
        except TimeoutException:
            logger.error("等待页面元素超时")
            raise
        except Exception as e:
            logger.error(f"搜索过程出错: {str(e)}")
            raise
            
    def _parse_search_results(self, driver):
        try:
            # 等待搜索结果加载
            result_selector = "#search-page-scroller > div > div > div.MuiStack-root.Search_search-result__louwQ"
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, result_selector))
            )
            
            # 等待一下确保结果完全加载
            time.sleep(5)
            
            # 获取结果容器
            results_container = driver.find_element(By.CSS_SELECTOR, result_selector)
            
            # 获取所有文献条目
            results = results_container.find_elements(By.CSS_SELECTOR, "div.MuiStack-root > div")
            parsed_results = []
            
            for result in results:
                try:
                    # 获取文献信息
                    text_content = result.text
                    if not text_content or len(text_content.strip()) < 10:  # 跳过空内容或太短的内容
                        continue
                        
                    # 按行分割内容
                    lines = text_content.split('\n')
                    
                    # 解析信息
                    title = ""
                    source = ""
                    date = ""
                    is_pdf = False
                    
                    for line in lines:
                        # 检查是否包含PDF标记
                        if "PDF" in line:
                            is_pdf = True
                            # 移除PDF标记后的内容作为标题
                            title = line.replace("PDF", "").strip()
                        # 检查是否包含日期
                        elif re.search(r'\[\d{4}-\d{2}-\d{2}\]', line):
                            date = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', line).group(1)
                        # 其他内容可能是来源
                        elif line and not title:
                            title = line
                        elif line:
                            source += line + " "
                    
                    if title:  # 只添加有标题的结果
                        paper_info = {
                            "title": title,
                            "source": source.strip(),
                            "date": date,
                            "is_pdf": is_pdf,
                            "content": text_content  # 保存完整文本以备需要
                        }
                        parsed_results.append(paper_info)
                        logger.info(f"解析到文献: {title[:50]}...")
                        
                except Exception as e:
                    logger.error(f"解析单个结果时出错: {str(e)}")
                    continue
            
            logger.info(f"成功解析 {len(parsed_results)} 篇文献")
            return parsed_results, True
            
        except Exception as e:
            logger.error(f"解析搜索结果时出错: {str(e)}")
            return [], True
            
    def crawl_literature(self, topic: str, keywords: List[str], num_papers: int = 20) -> List[Dict]:
        """
        爬取相关文献
        
        Args:
            topic: 文章主题
            keywords: 关键词列表
            num_papers: 需要爬取的文献数量
            
        Returns:
            List[Dict]: 文献信息列表，每个字典包含标题、作者、摘要、发表年份等信息
        """
        try:
            # 设置浏览器驱动
            self._setup_driver()
            
            # 构建更有针对性的搜索查询
            # 使用主题和关键词，加上"参考文献"
            search_query = f"{topic} AI 医疗 深度学习 参考文献"
            logger.info(f"搜索查询: {search_query}")
            
            # 执行搜索
            self._search_metaso(search_query)
            
            # 解析搜索结果
            papers, _ = self._parse_search_results(self.driver)
            
            # 对结果进行排序和去重
            papers = self._deduplicate_papers(papers)
            papers = self._sort_papers_by_relevance(papers)
            
            # 获取指定数量的文献
            papers = papers[:num_papers] if papers else []
            
            # 保存参考文献
            if papers:
                self.save_references(papers)
            
            return papers
            
        except Exception as e:
            logger.error(f"爬取文献时出错: {str(e)}")
            return []
            
        finally:
            # 始终在完成后关闭浏览器
            self._close_driver()
            
    def _deduplicate_papers(self, papers: List[Dict]) -> List[Dict]:
        """去除重复的文献"""
        seen_titles = set()
        unique_papers = []
        
        for paper in papers:
            title = paper['title'].lower()
            if title not in seen_titles:
                seen_titles.add(title)
                unique_papers.append(paper)
                
        return unique_papers
        
    def _sort_papers_by_relevance(self, papers: List[Dict]) -> List[Dict]:
        """按相关性对文献进行排序"""
        # 这里可以实现更复杂的排序逻辑
        # 目前简单地按年份排序
        return sorted(papers, key=lambda x: x.get('year', ''), reverse=True) 