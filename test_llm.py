"""
简单的LLM测试脚本
用于测试LLM客户端是否正常工作
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_interface.clients.llm_client import LLMClient

def test_llm():
    """测试LLM客户端"""
    print("测试LLM客户端...")
    
    # 创建LLM客户端
    llm_client = LLMClient(model_type="aliyun")
    
    # 测试简单文本生成
    print("\n1. 测试简单文本生成:")
    prompt = "你好，请简单介绍一下 yourself in one sentence."
    response = llm_client.generate(prompt, max_tokens=100)
    print(f"响应: {response}")
    
    # 测试知识图谱提取
    print("\n2. 测试知识图谱提取:")
    text = "胡八一和王胖子是好友，他们一起在内蒙古探险。"
    triplets = llm_client.extract_kg_triplets(text)
    print(f"提取的三元组: {triplets}")

if __name__ == "__main__":
    test_llm()