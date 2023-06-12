# -*- coding: utf-8 -*-

"""
Created 2023/06/7
@author: Xiaoaowen
describe: service
"""

import pymysql
from api_utils import sql_config
from datetime import datetime

# 1440751417.283 --> '2015-08-28 16:43:37.283'
def timestamp2string(timeStamp):
    try:
        d = datetime.fromtimestamp(timeStamp)
        str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        return str1
    except Exception as e:
        print(e)
        return ''


# 查询车辆信息
def select_car(car_id):
    db = pymysql.connect(host=sql_config.sql_host, user=sql_config.sql_username, password=sql_config.sql_password,
                         database=sql_config.sql_database)
    cursor = db.cursor()
    cursor.execute("select * from Car_Info where Car_ID='" + car_id + "'")
    data = cursor.fetchone()
    db.close()
    return data

# 删除车辆信息
def del_car(car_id):
    try:
        db = pymysql.connect(host=sql_config.sql_host, user=sql_config.sql_username, password=sql_config.sql_password,
                             database=sql_config.sql_database)
        cursor = db.cursor()
        del_sql = "DELETE FROM Car_Info WHERE Car_ID='" + car_id + "';"
        cursor.execute(del_sql)
        db.commit()
        db.close()
        return data
    except:
        return "删除车辆信息失败！"

# 保存车辆信息
def save_car_info(car_id, car_type, car_time):
    try:
        db = pymysql.connect(host=sql_config.sql_host, user=sql_config.sql_username, password=sql_config.sql_password,
                             database=sql_config.sql_database)
        cursor = db.cursor()

        time_str = timestamp2string(car_time)
        print(time_str)

        sql = "insert into Car_Info (Car_ID, Car_Type, Car_time) value('" + car_id + "', '" + str(car_type) + "', '" + time_str + "')"
        print(sql)
        cursor.execute(sql)
        db.commit()
        db.close()
        return True, "保存成功"
    except:
        return False, "数据储存有问题！"

# 统计已停车位数
def get_car_count():
    try:
        db = pymysql.connect(host=sql_config.sql_host, user=sql_config.sql_username, password=sql_config.sql_password,
                             database=sql_config.sql_database)
        cursor = db.cursor()
        sql = "select COUNT(*) from Car_Info;"
        cursor.execute(sql)
        data = cursor.fetchone()
        db.close()
        return data[0]
    except:
        return "获取车位数失败！"


if __name__ == '__main__':
    Car_ID = "粤MFE658"
    data = select_car(Car_ID)
    print(get_car_count())