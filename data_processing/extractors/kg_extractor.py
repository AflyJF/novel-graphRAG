"""
知识图谱提取器
用于从文本中提取知识图谱三元组
"""
import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from llm_interface.clients.llm_client import LLMClient

class KGExtractor:
    def __init__(self, model_type="aliyun_openai"):
        """
        初始化知识图谱提取器
        
        Args:
            model_type (str): 模型类型
        """
        self.llm_client = LLMClient(model_type)
    
    def extract_from_text(self, text):
        """
        从文本中提取知识图谱三元组
        
        Args:
            text (str): 输入文本
            
        Returns:
            dict: 包含三元组和数量的字典
        """
        try:
            triplets = self.llm_client.extract_kg_triplets(text)
            return {
                "triplets": triplets,
                "count": len(triplets)
            }
        except Exception as e:
            print(f"从文本提取知识图谱时出错: {e}")
            return {
                "triplets": [],
                "count": 0,
                "error": str(e)
            }
    
    def extract_from_file(self, file_path, output_path=None):
        """
        从文件中提取知识图谱三元组
        
        Args:
            file_path (str): 文件路径
            output_path (str): 输出文件路径
            
        Returns:
            dict: 包含三元组和输出路径的字典
        """
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取三元组
            triplets = self.llm_client.extract_kg_triplets(content)
            
            # 保存结果
            if output_path:
                result = {
                    "triplets": triplets,
                    "count": len(triplets)
                }
                
                # 确保输出目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                return {
                    "triplets": triplets,
                    "count": len(triplets),
                    "output_file": output_path
                }
            
            return {
                "triplets": triplets,
                "count": len(triplets)
            }
        except Exception as e:
            print(f"从文件提取知识图谱时出错: {e}")
            return {
                "triplets": [],
                "count": 0,
                "error": str(e)
            }