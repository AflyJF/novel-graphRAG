"""
知识图谱提取API
提供从文本和文件中提取知识图谱三元组的接口
"""
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from data_processing.extractors.kg_extractor import KGExtractor
import json

# 创建蓝图
kg_extraction_bp = Blueprint('kg_extraction', __name__)

@kg_extraction_bp.route('/api/kg/extract-from-text', methods=['POST'])
def extract_kg_from_text():
    """
    从文本中提取知识图谱三元组
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        llm_type = data.get('llm_type', 'aliyun_openai')  # 默认使用aliyun_openai
        
        if not text:
            return jsonify({"error": "文本不能为空"}), 400
        
        # 初始化提取器
        extractor = KGExtractor(llm_type)
        
        # 提取三元组
        triplets = extractor.extract_from_text(text)
        
        return jsonify({
            "message": "知识图谱提取成功",
            "count": len(triplets),
            "triplets": triplets
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@kg_extraction_bp.route('/api/kg/extract-from-file', methods=['POST'])
def extract_kg_from_file():
    """
    从文件中提取知识图谱三元组
    """
    try:
        data = request.get_json()
        filename = data.get('filename', '')
        llm_type = data.get('llm_type', 'aliyun_openai')  # 默认使用aliyun_openai
        
        if not filename:
            return jsonify({"error": "文件名不能为空"}), 400
        
        # 构造文件路径
        file_path = f'/root/autodl-tmp/uploads/{filename}'
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return jsonify({"error": "文件不存在"}), 404
        
        # 初始化提取器
        extractor = KGExtractor(llm_type)
        
        # 构造输出文件路径
        output_filename = f"{os.path.splitext(filename)[0]}_triplets.json"
        output_path = f'/root/autodl-tmp/{output_filename}'
        
        # 提取三元组并保存到文件
        result = extractor.extract_from_file(file_path, output_path)
        
        if "error" in result:
            return jsonify({"error": result["error"]}), 500
        
        result["message"] = "知识图谱提取成功"
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@kg_extraction_bp.route('/api/kg/extract-from-novel', methods=['POST'])
def extract_kg_from_novel():
    """
    从鬼吹灯小说中提取知识图谱三元组
    """
    try:
        data = request.get_json()
        llm_type = data.get('llm_type', 'aliyun_openai')  # 默认使用aliyun_openai
        
        # 小说文件路径
        novel_path = '/root/autodl-tmp/鬼吹灯之龙岭迷窟.txt'
        
        # 检查文件是否存在
        if not os.path.exists(novel_path):
            return jsonify({"error": "小说文件不存在，请确认文件已上传到 /root/autodl-tmp/目录"}), 404
        
        # 初始化提取器
        extractor = KGExtractor(llm_type)
        
        # 构造输出文件路径
        output_path = '/root/autodl-tmp/鬼吹灯之龙岭迷窟_triplets.json'
        
        # 提取三元组并保存到文件
        result = extractor.extract_from_file(novel_path, output_path)
        
        if "error" in result:
            return jsonify({"error": result["error"]}), 500
        
        result["message"] = "鬼吹灯小说知识图谱提取成功"
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500