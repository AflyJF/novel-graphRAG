# Novel GraphRAG Project

基于知识图谱的小说分析系统

## 项目简介

本项目旨在构建一个能够从系列小说中提取知识图谱并支持智能查询的系统。主要功能包括：
- 用户上传小说文本
- 使用大语言模型提取知识图谱关系
- 将关系存储到Neo4j图数据库
- 提供基于图RAG的智能查询界面

## 技术栈

- 前端: React/Vue.js
- 后端: Python Flask/FastAPI
- 大语言模型: 阿里云Qwen模型 + Qwen3-14B-Instruct本地模型
- 图数据库: Neo4j
- 推理框架: vLLM

## 目录结构

- [frontend/](file:///root/novel-graphRAG/frontend) - 前端网站代码
- [backend/](file:///root/novel-graphRAG/backend) - 后端服务
- [data_processing/](file:///root/novel-graphRAG/data_processing) - 数据处理模块
- [graph_db/](file:///root/novel-graphRAG/graph_db) - 图数据库接口
- [llm_interface/](file:///root/novel-graphRAG/llm_interface) - 大语言模型接口
- [models/](file:///root/autodl-tmp/models) - 本地模型存储
- [logs/](file:///root/novel-graphRAG/logs) - 日志文件

## 部署说明

1. 创建Conda虚拟环境
2. 安装依赖项
3. 配置Neo4j数据库
4. 下载并配置本地LLM模型
5. 启动各组件服务