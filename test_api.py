"""
API测试脚本
用于测试文件上传和知识图谱提取功能
"""
import requests
import json

# 测试服务器地址
BASE_URL = "http://localhost:5000"

def test_file_upload():
    """测试文件上传功能"""
    print("测试文件上传...")
    
    # 列出当前已上传的文件
    response = requests.get(f"{BASE_URL}/api/files/files")
    print(f"当前文件列表: {response.json()}")
    
    # 上传测试文件
    with open('/root/autodl-tmp/uploads/test_novel.txt', 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/api/files/upload", files=files)
        print(f"文件上传结果: {response.json()}")

def test_kg_extraction():
    """测试知识图谱提取功能"""
    print("\n测试知识图谱提取...")
    
    # 从文本提取
    text = "胡八一和王胖子是好友，他们一起在内蒙古探险。"
    payload = {
        "text": text,
        "llm_type": "aliyun_openai"  # 使用OpenAI兼容模式
    }
    
    response = requests.post(f"{BASE_URL}/api/kg/extract-from-text", json=payload)
    print(f"从文本提取KG结果: {response.json()}")
    
    # 从文件提取
    payload = {
        "filename": "test_novel.txt",
        "llm_type": "aliyun_openai"  # 使用OpenAI兼容模式
    }
    
    response = requests.post(f"{BASE_URL}/api/kg/extract-from-file", json=payload)
    print(f"从文件提取KG结果: {response.json()}")

def test_kg_extraction_with_sample_text():
    """测试使用样本文本提取知识图谱"""
    print("\n测试使用样本文本提取知识图谱...")
    
    # 使用更详细的文本进行测试
    sample_text = """
    《鬼吹灯》是天下霸唱创作的一部盗墓小说。故事主要讲述了胡八一、王胖子和雪莉杨三人深入各种古墓探险的故事。
    他们在内蒙古的草原上发现了古墓，经历了一系列惊险刺激的冒险。胡八一精通风水秘术，王胖子胆大心细，
    雪莉杨则出身探险世家。三人组队深入精绝古城，寻找雮尘珠，以解除身上的诅咒。
    在探险过程中，他们遭遇了各种诡异的事件和危险的生物，但凭借智慧和勇气一次次化险为夷。
    """
    
    payload = {
        "text": sample_text,
        "llm_type": "aliyun_openai"  # 使用OpenAI兼容模式
    }
    
    response = requests.post(f"{BASE_URL}/api/kg/extract-from-text", json=payload)
    print(f"使用样本文本提取KG结果: {response.json()}")

if __name__ == "__main__":
    test_file_upload()
    test_kg_extraction()
    test_kg_extraction_with_sample_text()