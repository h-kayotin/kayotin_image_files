"""
up_pos_data - 上传csv数据到mysql数据库

使用csv库读取csv，使用csv存储至mysql数据库，速度较慢
对于测试数据12766条，用时6分钟


注意：
1、列的顺序不能改变

Author: hanayo
Date： 2023/12/21
"""

import pathlib
import time

import pymysql
from config import user_name, user_pwd, host_inner, port_inner, db_name, tb_name
import datetime
import csv


class PosUP:

    def __init__(self, file):
        self.rows_num = 1
        self.updated_row = 0
        self.conn = pymysql.connect(host=host_inner, port=port_inner, user=user_name, password=user_pwd,
                                    database=db_name, charset="utf8mb4")
        self.file = pathlib.Path(file)
        self.err_rows = list()
        self.start = time.time()
        self.read_csv()
        self.conn.close()
        print(f"本次一共上传{self.updated_row}条数据,{datetime.datetime.now()}")
        self.save_log()

    def read_csv(self):
        """
        读取csv文件
        """
        csv_file = self.file
        if csv_file.is_file():
            with open(csv_file) as file:
                reader = csv.reader(file, delimiter=",", quotechar='"')
                reader.__next__()
                for row in reader:
                    row[-8] = row[-8].replace(",", "")
                    self.up_to_db(row)
                    self.rows_num += 1

    def up_to_db(self, row_list):
        sql_text = f"""
        INSERT INTO `{tb_name}` ( `pos_year`, `pos_month`, `pos_week_char`, `pos_sche`, `pos_week_num`, `pos_brand_cn`, 
        `pos_brand_en`, `pos_category_id`, `pos_category_desc`, `pos_dept_id`, `pos_dept_desc`, `pos_class_id`, 
        `pos_class_desc`, `pos_supplier_id`, `pos_supplier_desc`, `pos_item_code`, `pos_item_desc`, `pos_bar_code`, 
        `pos_is_seasonal`, `pos_is_pog`, `pos_region_cn`, `pos_mkt_cn`, `pos_province`, `pos_city`, 
        `pos_sales_store_id`, `pos_sales_store_name`, `pos_online_flg`, `pos_order_store_id`, 
        `pos_order_store_name`, `pos_deliver_store_id`, `pos_deliver_store_name`, `pos_sales_quantity`, 
        `pos_no_tax`, `pos_sales_amt_vat`, `pos_srp`, `pos_price`, `pos_price_amt`, `pos_channel_1`, 
        `pos_channel_2`, `pos_tier`) VALUES ({str(row_list)[1:-1]});        
        """
        try:
            # 获取游标对象
            with self.conn.cursor() as cursor:
                # 通过游标对象对数据库服务器发出sql语句
                affected_rows = cursor.execute(sql_text)
                if affected_rows == 1:
                    self.updated_row += 1
                if self.updated_row % 500 == 0:
                    print(f"已上传{self.updated_row}条数据,{datetime.datetime.now()}")
            # 提交
            self.conn.commit()
        except pymysql.MySQLError as err:
            # 回滚
            self.conn.rollback()
            print(type(err), err)
            self.err_rows.append(self.rows_num)

    def save_log(self):
        with open("resource/log.txt", mode="a", encoding="utf-8") as log_file:
            log_file.write(f"本次共成功上传{self.updated_row}条数据,{datetime.datetime.now()}\n")
            log_file.write(f"本次失败的条目是{self.err_rows}\n")
            cost_time = (time.time() - self.start) / 60
            log_file.write(f"本次共用时{cost_time:.2f}分钟\n")


if __name__ == '__main__':
    PosUP('resource/test1.2.csv')


