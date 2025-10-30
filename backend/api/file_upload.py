"""
文件上传处理模块
处理用户上传的小说文本文件
"""
import sys
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import yaml

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 创建蓝图
file_upload_bp = Blueprint('file_upload', __name__)

# 从配置文件加载配置
def load_config():
    with open('/root/novel-graphRAG/config.yaml', 'r') as f:
        return yaml.safe_load(f)

config = load_config()
UPLOAD_FOLDER = config['data']['upload_dir']

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@file_upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    处理文件上传请求
    """
    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return jsonify({'error': '没有文件在请求中'}), 400
    
    file = request.files['file']
    
    # 检查是否有文件被选择
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file:
        # 确保文件名安全
        filename = secure_filename(file.filename)
        
        # 保存文件到上传目录
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        return jsonify({
            'message': '文件上传成功',
            'filename': filename,
            'file_path': file_path
        }), 200

@file_upload_bp.route('/files', methods=['GET'])
def list_files():
    """
    列出所有已上传的文件
    """
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify({
            'files': files,
            'count': len(files)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500