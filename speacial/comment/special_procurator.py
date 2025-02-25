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
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'fa2abdc3-ad1e-48c4-8c0f-750f45251dc4'
    }
    sql_template = read_template("template_comment.txt")
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
    try:
        response = requests.post('http://gpt-proxy.jd.com/v1/chat/completions', headers=headers, json=body, stream=True)
        response_body = response.json()
        out = response_body['choices'][0]['message']['content']
        print(f'结果'+ out)
        return out
    except Exception as e:
        print(f"API调用失败: {e}")
        return "模型调用失败"



if __name__ == '__main__':
    data_list = []
    data_map = {}
    file_path = '/Users/lizhaojing7/Downloads/专项/reason3.xlsx'
    output_file = '/Users/lizhaojing7/Downloads/专项/end.xlsx'

    df = pd.read_excel(file_path, engine='openpyxl')
    # 逐行处理数据
    for index, row in df.iterrows():
        reason = row.iloc[0]
        short_reason = row.iloc[1]
        data_map['comment'] = reason
        data_map['short_comment'] = short_reason
        result = query_company_openai(data_map)
        data_list.append([reason,short_reason, result])


    #写入excel
    df = pd.DataFrame(data_list, columns=['原评语','精简评语','有无冲突'])
    with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=True, sheet_name='Sheet1',
                        startrow=writer.sheets['Sheet1'].max_row)