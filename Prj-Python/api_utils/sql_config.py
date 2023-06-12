import os

#  ========== 一、sql配置 ==========
sql_host = os.environ.get("SQL_HOST", "127.0.0.1")
# sql_host = os.environ.get("SQL_HOST", "192.168.12.84")
sql_port = int(os.environ.get("SQL_PORT", 3306))

sql_username = os.environ.get("SQL_USERNAME", "root")
sql_password = os.environ.get("SQL_PASSWORD", "root")
# sql_password = os.environ.get("SQL_PASSWORD", "License_Plate_Info")
# sql_database = os.environ.get("SQL_DATABASE", "ChePai")
sql_database = os.environ.get("SQL_DATABASE", "chepai")
# ============================================================
