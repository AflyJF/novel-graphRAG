# Novel GraphRAG - 基于知识图谱的小说分析系统

## 项目简介

Novel GraphRAG是一个基于知识图谱的小说分析系统，旨在通过大型语言模型（LLM）从长篇小说文本中提取实体和关系，构建知识图谱，并基于图RAG技术进行智能查询和分析。

## 功能特性

- 小说文本上传和管理
- 基于LLM的知识图谱构建
- 图数据库存储和查询
- 智能问答和推理

## 系统架构

```
novel-graphRAG/
├── backend/              # 后端服务
├── frontend/             # 前端界面
├── data_processing/      # 数据处理模块
├── graph_db/             # 图数据库接口
├── llm_interface/        # 大语言模型接口
├── uploads/              # 上传文件存储目录
├── processed/            # 处理后文件存储目录
└── models/               # 本地模型存储目录
```

## 环境配置

### 1. 创建Conda环境

```bash
conda create -n novel-graphRAG python=3.10
conda activate novel-graphRAG
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置阿里云API密钥

要使用阿里云的大语言模型，您需要获取API密钥：

1. 访问 [阿里云DashScope控制台](https://dashscope.console.aliyun.com/apiKey)
2. 注册账号并完成实名认证
3. 创建API密钥

**安全提示：为了防止API密钥泄露，请不要直接修改config.yaml文件中的api_key字段。**

将您的API密钥设置为系统环境变量：

```bash
# 在~/.bashrc或~/.profile中添加
export DASHSCOPE_API_KEY="your_actual_api_key_here"

# 重新加载配置
source ~/.bashrc
```

或者在启动应用时临时设置：

```bash
DASHSCOPE_API_KEY="your_actual_api_key_here" python backend/app.py
```

系统会自动从环境变量DASHSCOPE_API_KEY读取API密钥，config.yaml中的`${DASHSCOPE_API_KEY}`会被自动替换。

```yaml
llm:
  aliyun_api:
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"  # 使用阿里云百炼平台OpenAI兼容模式
    api_key: "${DASHSCOPE_API_KEY}"  # 从环境变量读取
```

阿里云DashScope平台支持两种API调用方式：
1. 使用dashscope库（默认方式）
2. 使用OpenAI风格的API调用（推荐，与标准OpenAI API兼容）

推荐使用OpenAI兼容模式，这样只需要提供API密钥、base_url和模型名称即可，简化了配置过程。这种方式与标准OpenAI API完全兼容，便于后续扩展到其他支持OpenAI API的平台。

### 4. 配置Neo4j数据库

在 `config.yaml` 文件中配置Neo4j数据库连接信息：

```yaml
database:
  neo4j:
    uri: "bolt://localhost:7687"
    username: "neo4j"
    password: "your_password"
```

## 使用方法

1. 启动后端服务：
   ```bash
   python backend/app.py
   ```

2. 访问前端界面：
   在浏览器中打开 `http://localhost:5000`

## API接口

- `/api/files/upload` - 上传小说文件
- `/api/files/files` - 获取已上传文件列表
- `/api/kg/extract-from-text` - 从文本中提取知识图谱
- `/api/kg/extract-from-file` - 从文件中提取知识图谱

## 项目进度

请查看 `logs/activity.log` 文件了解项目开发进度。

## 技术栈

- 后端：Flask
- 前端：HTML/CSS/JavaScript
- 数据库：Neo4j图数据库
- 大语言模型：阿里云Qwen系列模型
- 本地模型推理：vLLM

## 开发计划

1. 完善文件上传和处理功能
2. 实现知识图谱提取和存储
3. 开发图数据库查询接口
4. 构建前端用户界面
5. 实现基于图RAG的智能查询功能