"""
后端主应用入口文件
"""
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # TODO: 添加路由和配置
    
    @app.route('/')
    def index():
        return {'message': 'Novel GraphRAG Backend Server'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)