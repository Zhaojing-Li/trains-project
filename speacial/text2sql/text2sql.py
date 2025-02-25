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


def send_request(input_map):

    sql_template = read_template("../../logistics/template.txt")
    template = replace_placeholders(sql_template, **input_map)
    url = "http://secllm.jd.com/v1/completion-messages"
    data = {
        "inputs": {
            "query": template,
        },
        "response_mode": "blocking",
        "user": "lizhaojing7"
    }

    headers = {
        "Authorization": "Bearer app-y8LT80cIoUZaCs1qDjIzgvBM",
        "Content-Type": "application/json"
    }


    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    # 检查请求是否成功
    response.raise_for_status()
    return response




if __name__ == '__main__':
    data_list = []
    data_map = {}
    question_file = "special_question_1.txt"
    #output_file = '/Users/lizhaojing7/Downloads/sql.xlsx'
    with open(question_file, "r", encoding="utf-8") as file:
        for line in file:
            query_info = line.strip()
            data_map['query'] = query_info
            result = send_request(data_map)
            data_list.append([query_info, result])



    #写入excel
    # df = pd.DataFrame(data_list, columns=['query','answer'])
    # with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
    #         df.to_excel(writer, index=False, header=True, sheet_name='Sheet1',
    #                     startrow=writer.sheets['Sheet1'].max_row)