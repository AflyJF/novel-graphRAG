"""
后端主应用
"""
from flask import Flask
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 导入API模块
from backend.api.file_upload import file_upload_bp
from backend.api.kg_extraction import kg_extraction_bp

def create_app():
    """
    创建Flask应用
    """
    app = Flask(__name__)
    
    # 启用CORS
    CORS(app)
    
    # 注册蓝图
    app.register_blueprint(file_upload_bp)
    app.register_blueprint(kg_extraction_bp)
    
    @app.route('/')
    def home():
        return 'Novel GraphRAG 后端服务正在运行'
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)