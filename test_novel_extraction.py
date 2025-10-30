"""
测试鬼吹灯小说知识图谱提取
"""
import requests
import json

# 测试服务器地址
BASE_URL = "http://localhost:5000"

def test_novel_extraction():
    """测试鬼吹灯小说知识图谱提取"""
    print("测试鬼吹灯小说知识图谱提取...")
    
    # 提取鬼吹灯小说知识图谱
    payload = {
        "llm_type": "aliyun_openai"  # 使用OpenAI兼容模式
    }
    
    response = requests.post(f"{BASE_URL}/api/kg/extract-from-novel", json=payload)
    print(f"鬼吹灯小说提取KG结果: {response.json()}")

if __name__ == "__main__":
    test_novel_extraction()