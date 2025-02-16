import json

import requests
import pandas as pd
import re

def read_template(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def replace_placeholders(template, **kwargs):
    pattern = re.compile(r"\{\{(.*?)\}\}")
    def replace_match(match):
        # 提取占位符中的字段名
        key = match.group(1).strip()
        # 如果字段名在 kwargs 中，则替换为对应的值，否则保留占位符
        return str(kwargs.get(key, match.group(0)))
    return pattern.sub(replace_match, template)

def query_company_openai(data_map):
    # 设置请求头
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'fa2abdc3-ad1e-48c4-8c0f-750f45251dc4'
    }
    sql_template = read_template("template.txt")
    template = replace_placeholders(sql_template, **data_map)
    message = [{
        "role": "user",
        "content": template
    }]


    body = {
        "model": "gpt-4o-0806",
        "temperature": float(0),
        "top_p": float(1),
        "messages" : message
    }
    response = requests.post('http://gpt-proxy.jd.com/v1/chat/completions', headers=headers, json=body, stream=True)
    status_code = response.status_code
    response_body = response.json()
    print(data_map['query'])
    print(response_body)
    out = response_body['choices'][0]['message']['content'].replace('"""', '')
    return json.loads(out).get('sql',str)



if __name__ == '__main__':
    data_list = []
    data_map = {'erp': "lizhaojing7", 'organization': "京东集团-CCO体系-信息安全部-合规技术组"}
    question_file = "/Users/lizhaojing7/Downloads/Pycharm Project/trains-project/logistics/special_question.txt"
    output_file = '/Users/lizhaojing7/Downloads/sql.xlsx'
    with open(question_file, "r", encoding="utf-8") as file:
        for line in file:
            query_info = line.strip()
            data_map['query'] = query_info
            result = query_company_openai(data_map)
            data_list.append([query_info, result])

    #写入excel
    df = pd.DataFrame(data_list, columns=['query','answer'])
    with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=True, sheet_name='Sheet1',
                        startrow=writer.sheets['Sheet1'].max_row)