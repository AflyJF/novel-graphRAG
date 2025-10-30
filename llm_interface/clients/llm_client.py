"""
LLM客户端
用于与大语言模型进行交互
"""
import dashscope
from openai import OpenAI
import yaml
import os
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from vllm import LLM, SamplingParams
import json

class LLMClient:
    def __init__(self, model_type="aliyun"):
        """
        初始化LLM客户端
        
        Args:
            model_type (str): 模型类型 ("aliyun" 或 "local")
        """
        self.model_type = model_type
        self.config = self._load_config()
        
        if model_type == "aliyun":
            self._init_aliyun_client()
        elif model_type == "aliyun_openai":
            self._init_aliyun_openai_client()
        elif model_type == "local":
            self._init_local_model()
    
    def _load_config(self):
        """
        加载配置文件，并替换环境变量引用
        """
        with open('/root/novel-graphRAG/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # 递归替换配置中的环境变量引用 ${VAR_NAME}
        def replace_env_vars(value):
            if isinstance(value, str):
                # 使用正则表达式查找 ${VAR} 格式的环境变量引用
                pattern = r'\$\{([^}]+)\}'
                return re.sub(pattern, lambda m: os.getenv(m.group(1), m.group(0)), value)
            elif isinstance(value, dict):
                return {k: replace_env_vars(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [replace_env_vars(item) for item in value]
            return value
        
        return replace_env_vars(config)
    
    def _init_aliyun_client(self):
        """
        初始化阿里云API客户端 (使用dashscope库)
        """
        api_config = self.config['llm']['aliyun_api']
        # 使用dashscope初始化阿里云Qwen API
        dashscope.api_key = api_config['api_key']
        self.model_name = "qwen-plus"  # 默认使用qwen-plus模型
        self.client_type = "dashscope"
    
    def _init_aliyun_openai_client(self):
        """
        初始化阿里云API客户端 (使用OpenAI风格的API)
        """
        api_config = self.config['llm']['aliyun_api']
        print(f"初始化OpenAI客户端，api_key: {api_config['api_key'][:10]}..., base_url: {api_config['base_url']}")
        # 使用OpenAI库初始化阿里云Qwen API，按照阿里云百炼平台推荐方式
        try:
            self.client = OpenAI(
                # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
                api_key=api_config['api_key'],
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
            self.model_name = "qwen-plus"  # 默认使用qwen-plus模型
            self.client_type = "openai"
            print("OpenAI客户端初始化成功")
        except Exception as e:
            print(f"OpenAI客户端初始化失败: {e}")
            raise
    
    def _init_local_model(self):
        """
        初始化本地模型
        """
        local_config = self.config['llm']['local_model']
        model_path = local_config['path']
        
        # 使用vLLM加载模型
        self.llm = LLM(model=model_path)
        self.sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=512)
        self.client_type = "vllm"
    
    def generate(self, prompt, max_tokens=512):
        """
        生成文本
        
        Args:
            prompt (str): 提示词
            max_tokens (int): 最大生成token数
            
        Returns:
            str: 生成的文本
        """
        if self.model_type == "aliyun":
            return self._generate_with_aliyun(prompt, max_tokens)
        elif self.model_type == "aliyun_openai":
            return self._generate_with_aliyun_openai(prompt, max_tokens)
        elif self.model_type == "local":
            return self._generate_with_local(prompt, max_tokens)
    
    def _generate_with_aliyun(self, prompt, max_tokens):
        """
        使用阿里云模型生成文本 (使用dashscope库)
        
        Args:
            prompt (str): 提示词
            max_tokens (int): 最大生成token数
            
        Returns:
            str: 生成的文本
        """
        try:
            messages = [
                {"role": "user", "content": prompt}
            ]
            response = dashscope.Generation.call(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens,
                result_format='message'
            )
            if response.status_code == 200:
                return response.output.choices[0]['message']['content']
            else:
                print(f"阿里云模型调用出错: {response}")
                return ""
        except Exception as e:
            print(f"阿里云模型调用出错: {e}")
            return ""
    
    def _generate_with_aliyun_openai(self, prompt, max_tokens):
        """
        使用阿里云模型生成文本 (使用OpenAI风格API)
        
        Args:
            prompt (str): 提示词
            max_tokens (int): 最大生成token数
            
        Returns:
            str: 生成的文本
        """
        try:
            completion = self.client.chat.completions.create(
                # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                # Qwen3模型通过enable_thinking参数控制思考过程（开源版默认True，商业版默认False）
                # 使用Qwen3开源版模型时，若未启用流式输出，请将下行取消注释，否则会报错
                # extra_body={"enable_thinking": False},
                max_tokens=max_tokens
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"阿里云OpenAI风格API调用出错: {e}")
            return ""
    
    def _generate_with_local(self, prompt, max_tokens):
        """
        使用本地模型生成文本
        
        Args:
            prompt (str): 提示词
            max_tokens (int): 最大生成token数
            
        Returns:
            str: 生成的文本
        """
        try:
            # 更新采样参数
            sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=max_tokens)
            outputs = self.llm.generate([prompt], sampling_params)
            return outputs[0].outputs[0].text
        except Exception as e:
            print(f"本地模型调用出错: {e}")
            return ""
    
    def extract_kg_triplets(self, text):
        """
        使用LLM从文本中提取知识图谱三元组
        
        Args:
            text (str): 输入文本
            
        Returns:
            list: 三元组列表 [{entity1, relation, entity2}, ...]
        """
        # 构造提示词
        prompt = f"""
你是一个专业的知识图谱专家，善于从中文小说文本中提取实体和关系。请从以下小说文本中提取知识图谱三元组（实体1，关系，实体2）。

提取的三元组应该包括但不限于以下类型的关系：
1. 人物与人物之间的关系（如：朋友、敌人、师徒、夫妻、兄弟、同事等）
2. 人物与地点之间的关系（如：出生地、居住地、访问地、故乡、所在地等）
3. 人物在地点做的事情（如：探险、居住、工作、发现、挖掘、调查等）
4. 人物与物品/专有名词的关系（如：拥有、使用、创建、发现、携带、穿戴等）
5. 人物与组织/门派的关系（如：成员、掌门、创始人、敌对等）
6. 时间与事件的关系（如：发生时间、持续时间等）

提取要求：
1. 确保实体名称完整准确，尽量使用全名
2. 关系描述要简洁明确，使用中文
3. 只提取文本中明确提到的事实，不要推测
4. 优先提取重要和核心的三元组

请严格按照以下JSON格式返回结果，不要包含其他内容：
{{
    "triplets": [
        {{"entity1": "实体1", "relation": "关系", "entity2": "实体2"}},
        {{"entity1": "实体1", "relation": "关系", "entity2": "实体2"}}
    ]
}}

小说文本：
{text[:3000]}  # 限制文本长度以避免超出模型处理能力
"""
        
        try:
            response_text = self.generate(prompt, max_tokens=2048)
            print(f"模型原始响应: {response_text}")
            
            # 尝试解析JSON响应
            try:
                # 查找JSON对象的开始和结束位置
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end > start:
                    json_str = response_text[start:end]
                    result = json.loads(json_str)
                    return result.get("triplets", [])
                else:
                    print(f"无法从响应中提取JSON: {response_text}")
                    return []
            except json.JSONDecodeError as je:
                print(f"JSON解析错误: {je}")
                print(f"响应内容: {response_text}")
                # 尝试修复常见的格式问题
                # 移除可能的代码块标记
                cleaned_response = response_text.replace("```json", "").replace("```", "").strip()
                try:
                    start = cleaned_response.find('{')
                    end = cleaned_response.rfind('}') + 1
                    if start != -1 and end > start:
                        json_str = cleaned_response[start:end]
                        result = json.loads(json_str)
                        return result.get("triplets", [])
                except json.JSONDecodeError:
                    pass
                return []
        except Exception as e:
            print(f"提取知识图谱时出错: {e}")
            return []