import os
import sys
import pathlib
from urllib.parse import urlparse

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 重要：导入你的 Flask app 和 db（确保 app.py 里已有 db、Migrate 初始化）
from app import app, db
from flask_migrate import init as mig_init, migrate as mig_migrate, upgrade as mig_upgrade


def ensure_database(db_url: str):
    """
    确保数据库已创建（仅针对 MySQL）：若不存在则 CREATE DATABASE。
    """
    parsed = urlparse(db_url)

    # 取出数据库名，例如 /workflowdb -> workflowdb
    db_name = (parsed.path or "").lstrip("/")
    if not db_name:
        print("ERROR: DATABASE_URL 缺少数据库名（例如 .../workflowdb）")
        sys.exit(1)

    # 组装“服务器级”连接串（不含业务库名，改连到系统库 mysql）
    # 注意：scheme 可能是 mysql+pymysql
    scheme = parsed.scheme  # 比如 'mysql+pymysql'
    auth = ""
    if parsed.username:
        auth += parsed.username
        if parsed.password:
            auth += f":{parsed.password}"
        auth += "@"

    host = parsed.hostname or "localhost"
    port = f":{parsed.port}" if parsed.port else ""

    # 连接到 mysql 系统库，避免指定业务库导致报错
    server_url = f"{scheme}://{auth}{host}{port}/mysql"

    engine = create_engine(server_url, isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4"))
        print(f"OK: 数据库 `{db_name}` 已存在或创建完成。")

    engine.dispose()


def main():
    # 1) 读 .env
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: 未在 .env 中找到 DATABASE_URL")
        sys.exit(1)

    # 2) 确保数据库存在
    ensure_database(db_url)

    # 3) 迁移目录与迁移操作（需在 app_context 下）
    migrations_dir = pathlib.Path("migrations")

    with app.app_context():
        if not migrations_dir.exists():
            print("• 初始化迁移目录 ...")
            mig_init()

        print("• 生成迁移脚本（自动检测 models 变更） ...")
        mig_migrate(message="auto init/update")

        print("• 执行升级（创建/更新表结构） ...")
        mig_upgrade()

    print("\n🎉 完成：数据库已就绪，表结构已同步。")


if __name__ == "__main__":
    main()
