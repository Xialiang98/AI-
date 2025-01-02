"""
核心处理模块 - 包含AI文本清理和PDF解析功能
"""

import asyncio
import aiohttp
import json
import logging
import PyPDF2
from typing import Dict, Any, AsyncGenerator, List, Tuple
from config import Config
import re
import http.client

logger = logging.getLogger(__name__)

class TextProcessor:
    """文本处理器，负责生成规范的学术论文"""
    
    def __init__(self):
        self.config = Config()
        self.conn = http.client.HTTPSConnection("gpt-5.vip")
        self.headers = {
            'Authorization': '',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'gpt-5.vip',
            'Connection': 'keep-alive'
        }
        
    def _make_ai_request(self, messages: List[Dict]) -> str:
        """发送AI请求并获取响应"""
        try:
            payload = json.dumps({
                "model": "gpt-4o-mini",
                "messages": messages,
                "stream": True
            })
            
            self.conn.request("POST", "/v1/chat/completions", payload, self.headers)
            response = self.conn.getresponse()
            data = response.read()
            result = data.decode("utf-8")
            
            # 解析流式响应
            response_text = ""
            for line in result.strip().split('\n'):
                if line.startswith('data: '):
                    try:
                        json_str = line[6:]  # 移除 'data: ' 前缀
                        if json_str.strip() == '[DONE]':
                            continue
                        response_data = json.loads(json_str)
                        if 'choices' in response_data and len(response_data['choices']) > 0:
                            delta = response_data['choices'][0].get('delta', {})
                            if 'content' in delta:
                                response_text += delta['content']
                    except json.JSONDecodeError:
                        continue
                        
            return response_text
            
        except Exception as e:
            logger.error(f"AI请求失败: {str(e)}")
            raise
            
    def _build_english_prompt(self, original_text: str, references: List[Dict], topic_info: Dict) -> str:
        """构建英文提示词"""
        # 读取参考文献文件
        references_text = ""
        try:
            with open("output/references.txt", 'r', encoding='utf-8') as f:
                references_text = f.read()
        except Exception as e:
            logger.error(f"读取参考文献失败: {str(e)}")
            
        prompt_parts = [
            "Please write a high-quality academic paper in English based on the following information:",
            "\nOriginal Text:",
            original_text,
            "\nMain Topic:",
            topic_info['topic']['en'],
            "\nKeywords:",
            ", ".join(topic_info['keywords']['en']),
            "\nRelevant References:",
            references_text,
            "\nRequirements:",
            "1. Follow standard academic paper structure (Introduction, Methods, Results, Discussion, Conclusion)",
            "2. Incorporate insights from the provided references",
            "3. Maintain academic writing style",
            "4. Ensure logical flow and coherence",
            "5. Include in-text citations",
            "6. Avoid mechanical language and transition words",
            "7. Focus on original analysis and insights"
        ]
        
        return "\n".join(prompt_parts)
        
    def _build_chinese_prompt(self, original_text: str, references: List[Dict], topic_info: Dict) -> str:
        """构建中文提示词"""
        # 读取参考文献文件
        references_text = ""
        try:
            with open("output/references.txt", 'r', encoding='utf-8') as f:
                references_text = f.read()
        except Exception as e:
            logger.error(f"读取参考文献失败: {str(e)}")
            
        prompt_parts = [
            "请根据以下信息撰写一篇高质量的中文学术论文：",
            "\n原始文本：",
            original_text,
            "\n主题：",
            topic_info['topic']['cn'],
            "\n关键词：",
            "、".join(topic_info['keywords']['cn']),
            "\n相关参考文献：",
            references_text,
            "\n要求：",
            "1. 遵循标准学术论文结构（摘要、引言、研究方法、研究结果、讨论、结论）",
            "2. 合理引用提供的参考文献，使用[年份]格式",
            "3. 保持学术写作风格，避免口语化表达",
            "4. 确保逻辑流畅和连贯性",
            "5. 避免机械化用语和过渡词",
            "6. 注重原创性分析和见解",
            "7. 不要使用'我们'、'本文'等字眼",
            "8. 不要在引用时使用'等'字",
            "9. 每个段落要有明确的主题",
            "10. 结论部分要简明扼要"
        ]
        
        return "\n".join(prompt_parts)
        
    def _format_english_paper(self, text: str) -> str:
        """格式化英文论文"""
        try:
            # 1. 移除AI生成特征
            ai_patterns = [
                r'As an AI .*?,',
                r'I apologize,.*?\.', 
                r'I cannot.*?\.', 
                r'I do not have.*?\.', 
                r'I\'m sorry,.*?\.', 
                r'I am not able to.*?\.', 
                r'I must inform you.*?\.', 
                r'Please note that.*?\.', 
                r'It\'s important to note.*?\.', 
                r'I would recommend.*?\.', 
                r'I suggest.*?\.', 
                r'In my opinion.*?\.', 
                r'Based on my understanding.*?\.', 
                r'From my perspective.*?\.', 
                r'As far as I know.*?\.', 
                r'To the best of my knowledge.*?\.'
            ]
            for pattern in ai_patterns:
                text = re.sub(pattern, '', text, flags=re.IGNORECASE)
            
            # 2. 移除机械化过渡词
            transition_words = [
                r'\bHowever,\s+', r'\bMoreover,\s+', r'\bFurthermore,\s+',
                r'\bTherefore,\s+', r'\bThus,\s+', r'\bHence,\s+',
                r'\bConsequently,\s+', r'\bNevertheless,\s+', r'\bNonetheless,\s+',
                r'\bIn addition,\s+', r'\bBesides,\s+', r'\bMeanwhile,\s+',
                r'\bSubsequently,\s+', r'\bAs a result,\s+', r'\bFor instance,\s+',
                r'\bFor example,\s+', r'\bIn other words,\s+', r'\bThat is to say,\s+',
                r'\bIn conclusion,\s+', r'\bTo sum up,\s+', r'\bOverall,\s+'
            ]
            for word in transition_words:
                text = re.sub(word, '', text)
            
            # 3. 移除多余的标记
            text = re.sub(r'\*\*|\#\#|__', '', text)
            
            # 4. 格式化段落和空白
            text = re.sub(r'\s+', ' ', text)  # 统一空白字符
            text = re.sub(r'([.!?])\s+([A-Z])', r'\1\n\n\2', text)  # 段落分隔
            
            # 5. 处理章节标题格式
            sections = ['Title', 'Abstract', 'Introduction', 'Methods', 'Results', 'Discussion', 'Conclusion', 'References']
            for section in sections:
                text = re.sub(f'({section}:?)', r'\n\n\1\n', text)
            
            # 6. 规范化引用格式
            text = re.sub(r'\((\d{4})\)', r' [\1]', text)  # 将(2023)改为[2023]
            text = re.sub(r'et\s+al\.', 'et al.', text)  # 规范化et al.
            
            # 7. 确保段落缩进
            lines = text.split('\n')
            formatted_lines = []
            for line in lines:
                if line.strip():
                    if any(section in line for section in sections):
                        formatted_lines.append(line.strip())
                    else:
                        formatted_lines.append('    ' + line.strip())
                else:
                    formatted_lines.append('')
            
            text = '\n'.join(formatted_lines)
            
            # 8. 规范化标题格式
            text = re.sub(r'^Title\s*\n\s*(.+?)(?=\n\n)', 
                         lambda m: f'Title\n{m.group(1).upper()}', text)
            
            return text.strip()
                
        except Exception as e:
            logger.error(f"格式化英文论文时出错: {str(e)}")
            return text
            
    def _format_chinese_paper(self, text: str) -> str:
        """格式化中文论文"""
        try:
            # 1. 移除AI生成特征
            ai_patterns = [
                r'作为人工智能.*?，',
                r'我认为.*?。',
                r'我的理解是.*?。',
                r'我不能.*?。',
                r'我必须说明.*?。',
                r'请注意.*?。',
                r'需要说明的是.*?。',
                r'我建议.*?。',
                r'我的观点是.*?。',
                r'据我所知.*?。',
                r'本文.*?。',
                r'我们.*?。'
            ]
            for pattern in ai_patterns:
                text = re.sub(pattern, '', text)
            
            # 2. 移除机械化过渡词
            transition_words = [
                r'然而，', r'但是，', r'不过，', r'因此，', r'所以，',
                r'此外，', r'另外，', r'而且，', r'并且，', r'接着，',
                r'随后，', r'总之，', r'总而言之，', r'综上所述，',
                r'例如，', r'比如，', r'换句话说，', r'也就是说，',
                r'值得注意的是，', r'需要指出的是，', r'显然，', r'显而易见，',
                r'毫无疑问，', r'众所周知，', r'一般来说，', r'通常来说，'
            ]
            for word in transition_words:
                text = text.replace(word, '')
            
            # 3. 移除多余的标记
            text = re.sub(r'\*\*|\#|__', '', text)
            
            # 4. 格式化段落和空白
            text = re.sub(r'\s+', ' ', text)  # 统一空白字符
            text = re.sub(r'([。！？])\s*([^，。！？、])', r'\1\n\n\2', text)  # 段落分隔
            
            # 5. 处理章节标题格式
            sections = ['标题', '摘要', '引言', '研究方法', '研究结果', '讨论', '结论', '参考文献']
            for section in sections:
                text = re.sub(f'({section})', r'\n\n\1\n', text)
            
            # 6. 规范化引用格式
            text = re.sub(r'（(\d{4})）', r'[\1]', text)  # 将（2023）改为[2023]
            text = re.sub(r'等人', '', text)  # 移除"等人"
            text = re.sub(r'等', '', text)  # 移除"等"
            
            # 7. 确保段落缩进
            lines = text.split('\n')
            formatted_lines = []
            for line in lines:
                if line.strip():
                    if any(section in line for section in sections):
                        formatted_lines.append(line.strip())
                    else:
                        formatted_lines.append('    ' + line.strip())
                else:
                    formatted_lines.append('')
            
            text = '\n'.join(formatted_lines)
            
            # 8. 规范化标题格式
            text = re.sub(r'^标题\s*\n\s*(.+?)(?=\n\n)', 
                         lambda m: f'标题\n{m.group(1)}', text)
            
            # 9. 移除特殊字符
            text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？、：；''""（）【】《》\[\]\s\.]', '', text)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"格式化中文论文时出错: {str(e)}")
            return text
            
    def _add_references_english(self, text: str, references: List[Dict]) -> str:
        """添加英文参考文献"""
        try:
            # 添加参考文献部分标题
            text += "\n\nReferences\n\n"
            
            # 格式化每个参考文献
            for i, ref in enumerate(references, 1):
                authors = ", ".join(ref['authors'])
                title = ref['title']
                year = ref['year']
                source = ref['source']
                
                reference = f"[{i}] {authors}. ({year}). {title}. {source}."
                if ref.get('url'):
                    reference += f" Retrieved from {ref['url']}"
                    
                text += reference + "\n\n"
                
            return text
            
        except Exception as e:
            logger.error(f"添加英文参考文献时出错: {str(e)}")
            return text
            
    def _add_references_chinese(self, text: str, references: List[Dict]) -> str:
        """添加中文参考文献"""
        try:
            # 添加参考文献部分标题
            text += "\n\n参考文献\n\n"
            
            # 格式化每个参考文献
            for i, ref in enumerate(references, 1):
                authors = "，".join(ref['authors'])
                title = ref['title']
                year = ref['year']
                source = ref['source']
                
                reference = f"[{i}] {authors}. {title}[J]. {source}, {year}."
                if ref.get('url'):
                    reference += f" 来源：{ref['url']}"
                    
                text += reference + "\n\n"
                
            return text
            
        except Exception as e:
            logger.error(f"添加中文参考文献时出错: {str(e)}")
            return text
        
    def process_english(self, original_text: str, references: List[Dict], topic_info: Dict) -> str:
        """处理并生成英文版论文"""
        try:
            # 1. 构建提示词
            prompt = self._build_english_prompt(
                original_text=original_text,
                references=references,
                topic_info=topic_info
            )
            
            # 2. 调用AI生成论文
            messages = [
                {"role": "system", "content": self.config.SYSTEM_PROMPT_EN},
                {"role": "user", "content": prompt}
            ]
            generated_text = self._make_ai_request(messages)
            
            # 3. 格式化论文
            formatted_text = self._format_english_paper(generated_text)
            
            # 4. 移除重复的参考文献部分
            if 'References' in formatted_text:
                parts = formatted_text.split('References', 1)
                formatted_text = parts[0] + 'References' + parts[1].split('References')[0]
            
            # 5. 添加参考文献
            final_text = self._add_references_english(formatted_text, references)
            
            return final_text
            
        except Exception as e:
            logger.error(f"处理英文论文时出错: {str(e)}")
            return original_text
            
    def process_chinese(self, original_text: str, references: List[Dict], topic_info: Dict) -> str:
        """处理并生成中文版论文"""
        try:
            # 1. 构建提示词
            prompt = self._build_chinese_prompt(
                original_text=original_text,
                references=references,
                topic_info=topic_info
            )
            
            # 2. 调用AI生成论文
            messages = [
                {"role": "system", "content": self.config.SYSTEM_PROMPT_CN},
                {"role": "user", "content": prompt}
            ]
            generated_text = self._make_ai_request(messages)
            
            # 3. 格式化论文
            formatted_text = self._format_chinese_paper(generated_text)
            
            # 4. 移除重复的参考文献部分
            if '参考文献' in formatted_text:
                parts = formatted_text.split('参考文献', 1)
                formatted_text = parts[0] + '参考文献' + parts[1].split('参考文献')[0]
            
            # 5. 添加参考文献
            final_text = self._add_references_chinese(formatted_text, references)
            
            return final_text
            
        except Exception as e:
            logger.error(f"处理中文论文时出错: {str(e)}")
            return original_text
            
    def parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """解析PDF文件"""
        try:
            with open(file_path, 'rb') as file:
                # 创建PDF读取器
                reader = PyPDF2.PdfReader(file)
                
                # 提取文本内容
                content = ""
                for page in reader.pages:
                    content += page.extract_text()
                
                # 提取元数据
                metadata = reader.metadata if reader.metadata else {}
                
                return {
                    "content": content,
                    "metadata": metadata,
                    "pages": len(reader.pages)
                }
        except Exception as e:
            logger.error(f"解析PDF时出错: {str(e)}")
            raise
            
    def process_pdf_to_paper(self, file_path: str) -> str:
        """处理PDF并生成论文"""
        try:
            # 解析PDF
            pdf_data = self.parse_pdf(file_path)
            
            # 调用AI生成论文
            prompt = f"""
            请根据以下参考文献内容生成一篇学术论文：
            
            参考文献内容：
            {pdf_data['content']}
            
            要求：
            1. 保持学术性和专业性
            2. 避免明显的AI生成特征
            3. 包含合适的引用
            4. 遵循学术论文格式
            """
            
            messages = [
                {"role": "user", "content": prompt}
            ]
            return self._make_ai_request(messages)
            
        except Exception as e:
            logger.error(f"生成论文时出错: {str(e)}")
            raise
            
    def batch_process(self, files: List[str]) -> List[Dict[str, Any]]:
        """批量处理文件"""
        results = []
        for file_path in files:
            try:
                if file_path.lower().endswith('.pdf'):
                    result = self.process_pdf_to_paper(file_path)
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    result = self.process_chinese(text, [], {"topic": {"cn": "", "en": ""}, "keywords": {"cn": [], "en": []}})
                results.append({"file": file_path, "result": result})
            except Exception as e:
                logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
                results.append({"file": file_path, "error": str(e)})
        return results 