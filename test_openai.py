import os
from openai import OpenAI

# 测试OpenAI客户端初始化
print("测试OpenAI客户端初始化...")

# 获取API密钥
api_key = os.getenv("DASHSCOPE_API_KEY")
print(f"API密钥前缀: {api_key[:10] if api_key else 'None'}")

if not api_key:
    print("错误: 未设置DASHSCOPE_API_KEY环境变量")
    exit(1)

try:
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    print("OpenAI客户端初始化成功")
    
    # 测试简单调用
    completion = client.chat.completions.create(
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你好"},
        ],
        # Qwen3模型通过enable_thinking参数控制思考过程（开源版默认True，商业版默认False）
        # 使用Qwen3开源版模型时，若未启用流式输出，请将下行取消注释，否则会报错
        # extra_body={"enable_thinking": False},
    )
    print("测试调用成功，响应:")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"OpenAI客户端测试失败: {e}")
    import traceback
    traceback.print_exc()