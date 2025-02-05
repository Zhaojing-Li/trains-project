from openai import OpenAI
import streamlit as st  # pip3 install streamlit
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
def get_completion(table_structures, sql_requirements, model="gpt-3.5-turbo"):
    instruction = """
    你是一位专业的SQL编写工程师,可以根据表结构和用户输入，生成SQL语句。
    """
    examples = """
        表结构如下：
        orders (
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
        customers (
            id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空
            customer_name VARCHAR(255) NOT NULL, -- 客户名，不允许为空
            email VARCHAR(255) UNIQUE, -- 邮箱，唯一
            register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 注册时间，默认为当前时间
        );

        products (
            id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空
            product_name VARCHAR(255) NOT NULL, -- 产品名称，不允许为空
            price DECIMAL(10,2) NOT NULL -- 价格，不允许为空
        );
        用户需求：
        哪个用户消费最高？消费多少？
        生成的SQL：
        SELECT customer_id, SUM(price) AS total_spent FROM orders GROUP BY customer_id ORDER BY total_spent DESC LIMIT 1;
    """
    prompt = f"""
        {instruction}
        示例：
        {examples}
        表结构如下：
        {table_structures}
        用户输入：
        {sql_requirements}
    """
    print(prompt)
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # 模型输出的随机性，0 表示随机性最小
        n=4
    )
    return response.choices[0].message.content


# 设置标题
st.title("Text2SQL")

# 获取用户输入的表结构数量
num_tables = st.number_input('请输入你需要填写的表结构数量:', min_value=1, max_value=10, step=1)

# 创建用于填写表结构的输入框
table_structures = ""
for i in range(num_tables):
    table_structure = st.text_area(f"请输入表结构 {i + 1}:")
    table_structures += table_structure + "\n"

# 新增SQL需求输入框
sql_requirements = st.text_area("请输入生成SQL的需求:")

# 当用户点击提交时，传递所有输入的数据到模型
if st.button("提交"):
    if all(table_structures) and sql_requirements:  # 检查是否所有的表结构和SQL需求都已经填写
        # print(table_structures, sql_requirements)
        output = get_completion(table_structures, sql_requirements)
        st.success(output)
    else:
        st.warning("请确保所有表结构和SQL需求已经填写")


















