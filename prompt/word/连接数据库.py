import pymysql

db_host = 'localhost'  # 数据库主机地址
db_user = 'root'  # 数据库用户名
db_password = '12345678'  # 数据库密码
db_name = 'AILLMtest'  # 数据库名称

# 创建数据库连接
conn = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    # 创建一个Cursor对象用于执行SQL语句
    with conn.cursor() as cursor:
        # 执行SQL语句，例如创建orders表
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS orders (
            id INT PRIMARY KEY NOT NULL, 
            customer_id INT NOT NULL,
            product_id INT NOT NULL, 
            price DECIMAL(10, 2) NOT NULL,
            STATUS INT NOT NULL CHECK (STATUS IN (0, 1, 2)), -- 确保订单状态在0, 1, 2之间
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pay_time TIMESTAMP NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        '''
        cursor.execute(create_table_sql)

    # 提交事务
    conn.commit()
except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    # 关闭数据库连接
    conn.close()
