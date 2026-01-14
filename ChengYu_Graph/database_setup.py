import pymysql
from pymysql import Error
from config import config
import os

# 加载配置
app_config = config['development']

def create_database():
    """创建数据库并执行初始化SQL脚本"""
    try:
        # 1. 连接到MySQL服务器
        connection = pymysql.connect(
            host=app_config.MYSQL_HOST,
            port=app_config.MYSQL_PORT,
            user=app_config.MYSQL_USER,
            password=app_config.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 2. 创建数据库
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {app_config.MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute(f"USE {app_config.MYSQL_DB}")
            
            # 3. 读取并执行SQL脚本
            sql_file_path = os.path.join(os.path.dirname(__file__), 'database_init.sql')
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_script = file.read()
            
            # 分割SQL语句并执行
            for statement in sql_script.split(';'):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)
            
            connection.commit()
            print(f"数据库 {app_config.MYSQL_DB} 创建并初始化成功！")
            
    except Error as e:
        print(f"数据库操作错误: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接已关闭")

if __name__ == '__main__':
    create_database()