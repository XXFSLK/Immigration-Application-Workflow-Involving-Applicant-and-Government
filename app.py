

from flask import Flask
from extensions import db,migrate
from utils.config import Config  # 配置文件在 utils 文件夹中

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)

    # 这里再注册蓝图，避免循环导入
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app

# 作为可执行入口
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
