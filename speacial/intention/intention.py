import json
import time

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


# def send_request(input_map):
#
#     sql_template = read_template("/Users/lizhaojing7/Downloads/Pycharm Project/trains-project/speacial/intention/intention_prompt.txt")
#     template = replace_placeholders(sql_template, **input_map)
#     url = "http://secllm.jd.com/v1/completion-messages"
#     data = {
#         "inputs": {
#             "query": template,
#         },
#         "response_mode": "blocking",
#         "user": "lizhaojing7"
#     }
#
#     headers = {
#         "Authorization": "Bearer app-y8LT80cIoUZaCs1qDjIzgvBM",
#         "Content-Type": "application/json"
#     }
#
#     start_time = time.time()
#     response = requests.post(url, json=data, headers=headers)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"请求耗时**: {elapsed_time:.6f}秒")
#     print(response.json().get('answer',str))
#     return response.json().get('answer',str) + f"请求耗时**: {elapsed_time:.6f}秒"



def query_company_openai(data_map):
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'fa2abdc3-ad1e-48c4-8c0f-750f45251dc4'
    }
    sql_template = read_template("/Users/lizhaojing7/Downloads/Pycharm Project/trains-project/speacial/intention/intention_prompt.txt")
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
        start_time = time.time()
        response = requests.post('http://gpt-proxy.jd.com/v1/chat/completions', headers=headers, json=body, stream=True)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"请求耗时**: {elapsed_time:.6f}秒")
        response_body = response.json()
        print(data_map['query'])
        out = response_body['choices'][0]['message']['content']
        print(f"结果：{out}, 时长为 {elapsed_time:.6f}秒")
        new_out = f"结果：{out}, 时长为 {elapsed_time:.6f}秒"
        return new_out
    except Exception as e:
        print(f"API调用失败: {e}")
        return "模型调用失败"




if __name__ == '__main__':
    data_list = []
    data_map = {}
    question_file = "/Users/lizhaojing7/Downloads/Pycharm Project/trains-project/speacial/intention/intention_question.txt"
    output_file = '/Users/lizhaojing7/Downloads/intention.xlsx'
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