"""
pos_data - 使用pandas和sqlalchemy来上传

12万条数据，约20秒


Author: hanayo
Date： 2023/12/22
"""

from config import user_name, user_pwd, host_inner, port_inner, db_name, tb_name
import pandas as pd
from sqlalchemy import text, create_engine
import time

db_columns = ['pos_year', 'pos_month', 'pos_week_char', 'pos_sche', 'pos_week_num', 'pos_brand_cn',
              'pos_brand_en', 'pos_category_id', 'pos_category_desc', 'pos_dept_id', 'pos_dept_desc', 'pos_class_id',
              'pos_class_desc', 'pos_supplier_id', 'pos_supplier_desc', 'pos_item_code', 'pos_item_desc',
              'pos_bar_code', 'pos_is_seasonal', 'pos_is_pog', 'pos_region_cn', 'pos_mkt_cn', 'pos_province',
              'pos_city', 'pos_sales_store_id', 'pos_sales_store_name', 'pos_online_flg', 'pos_order_store_id',
              'pos_order_store_name', 'pos_deliver_store_id', 'pos_deliver_store_name', 'pos_sales_quantity',
              'pos_no_tax', 'pos_sales_amt_vat', 'pos_srp', 'pos_price', 'pos_price_amt', 'pos_channel_1',
              'pos_channel_2', 'pos_tier']

check_num_cols = ['pos_sales_quantity', 'pos_no_tax', 'pos_sales_amt_vat', '']


def con_tax(item):
    """
    处理tax那一列可能有的千位分隔符
    :param item:df数据要处理的那一列
    :return:返回处理后的列
    """
    if isinstance(item, str):
        if "," not in item:
            return item
        s = ""
        tmp = item.strip("").split(",")
        for i in range(len(tmp)):
            s += tmp[i]
        return float(s)
    if isinstance(item, (float, int)):
        return item


def con_nums(item):
    """
    处理pos_sales_quantity和零售价pos_price中，“-”的条目
    :param item:
    :return:处理过后的值，会当做0处理
    """
    if isinstance(item, str):
        if "-" not in item:
            return float(item)
        temp = item.strip()
        if temp == "-":
            return 0
        else:
            return float(item)
    else:
        return item


class PosUpPD:

    def __init__(self, file, table_name):
        """
        数据上传的主程序
        :param file: 包含具体路径的文件名
        :param table_name: 上传至mysql的具体table名称
        """
        conn_info = f"mysql+pymysql://{user_name}:{user_pwd}@{host_inner}:{port_inner}/{db_name}?charset=utf8mb4"
        self.engine = create_engine(conn_info)
        self.table_name = table_name
        # 读取csv，自定义df对象的列名,指定了跳过第一行
        self.csv_df = pd.read_csv(file, index_col=False, encoding='gbk', names=db_columns, thousands=",",
                                  low_memory=False, skiprows=[0])
        # 对脏数据进行处理
        self.csv_df['pos_no_tax'] = self.csv_df['pos_no_tax'].map(con_tax).map(con_nums)
        self.csv_df['pos_sales_amt_vat'] = self.csv_df['pos_sales_amt_vat'].map(con_tax).map(con_nums)
        self.csv_df['pos_price'] = self.csv_df['pos_price'].map(con_tax).map(con_nums)
        self.csv_df['pos_price_amt'] = self.csv_df['pos_price_amt'].map(con_tax).map(con_nums)
        # 用to_sql方法保存到mysql数据库
        self.csv_df.to_sql(self.table_name, self.engine, chunksize=10000, index=False,
                           if_exists='append')


if __name__ == '__main__':
    st_time = time.time()
    print("开始上传数据-->")
    PosUpPD('resource/POS by store 202301.csv', 'pos_tb_test')
    print(f"用时{(time.time() - st_time)/60:.2f}分钟")
