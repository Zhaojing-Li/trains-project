import requests
import json
import pandas as pd

def read_lines_from_file(path):
    """读取文件中的每一行"""
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def send_request(input_data):
    url = "http://secllm.jd.com/v1/workflows/run"
    data = {
        "inputs": {
            "input": input_data,
            "time": "今天是2025年1月14日，处于本年度的上半年，本年的第一季度.",
            "open_mock": "0",
            "province_list": "[{\"code\":\"100000\",\"name\":\"物流总部\"},{\"code\":\"110000\",\"name\":\"北京区\"},{\"code\":\"150000\",\"name\":\"内蒙省区\"},{\"code\":\"120000\",\"name\":\"天津区\"},{\"code\":\"130000\",\"name\":\"河北省区\"},{\"code\":\"140000\",\"name\":\"山西省区\"},{\"code\":\"370000\",\"name\":\"山东省区\"},{\"code\":\"210000\",\"name\":\"辽宁省区\"},{\"code\":\"220000\",\"name\":\"吉林省区\"},{\"code\":\"230000\",\"name\":\"黑龙江省区\"},{\"code\":\"310000\",\"name\":\"上海区\"},{\"code\":\"330000\",\"name\":\"浙江省区\"},{\"code\":\"320000\",\"name\":\"江苏省区\"},{\"code\":\"340000\",\"name\":\"安徽省区\"},{\"code\":\"350000\",\"name\":\"福建省区\"},{\"code\":\"710000\",\"name\":\"台湾省区\"},{\"code\":\"450000\",\"name\":\"广西省区\"},{\"code\":\"360000\",\"name\":\"江西省区\"},{\"code\":\"430000\",\"name\":\"湖南省区\"},{\"code\":\"410000\",\"name\":\"河南省区\"},{\"code\":\"420000\",\"name\":\"湖北省区\"},{\"code\":\"440000\",\"name\":\"广东省区\"},{\"code\":\"460000\",\"name\":\"海南省区\"},{\"code\":\"810000\",\"name\":\"香港特别行政区\"},{\"code\":\"820000\",\"name\":\"澳门特别行政区\"},{\"code\":\"500000\",\"name\":\"重庆区\"},{\"code\":\"510000\",\"name\":\"四川省区\"},{\"code\":\"520000\",\"name\":\"贵州省区\"},{\"code\":\"530000\",\"name\":\"云南省区\"},{\"code\":\"540000\",\"name\":\"西藏省区\"},{\"code\":\"610000\",\"name\":\"陕西省区\"},{\"code\":\"620000\",\"name\":\"甘肃省区\"},{\"code\":\"630000\",\"name\":\"青海省区\"},{\"code\":\"640000\",\"name\":\"宁夏省区\"},{\"code\":\"650000\",\"name\":\"新疆省区\"},{\"code\":\"P990001\",\"name\":\"物流总部\"},{\"code\":\"P990002\",\"name\":\"京蒙安全防损部\"},{\"code\":\"P990003\",\"name\":\"津冀安全防损部\"},{\"code\":\"P990004\",\"name\":\"鲁晋安全防损部\"},{\"code\":\"P990005\",\"name\":\"东北安全防损部\"},{\"code\":\"P990006\",\"name\":\"沪浙安全防损部\"},{\"code\":\"P990007\",\"name\":\"苏皖安全防损部\"},{\"code\":\"P990008\",\"name\":\"桂闽安全防损部\"},{\"code\":\"P990009\",\"name\":\"湘赣安全防损部\"},{\"code\":\"P990010\",\"name\":\"豫鄂安全防损部\"},{\"code\":\"P990011\",\"name\":\"粤海安全防损部\"},{\"code\":\"P990012\",\"name\":\"西南安全防损部\"},{\"code\":\"P990013\",\"name\":\"西北安全防损部\"},{\"code\":\"A000001\",\"name\":\"全国\"}]",
            "entity_knowledge": "[\"津冀安全防损部，简称“津冀大区”、“津冀”、“津冀区”\",\"京蒙安全防损部简称“京蒙大区”，也可以称为“京蒙”、“京蒙区”\",\"沪浙安全防损部简称“沪浙大区”、“沪浙”、“沪浙区”\",\"东北安全防损部简称“东北大区”、“东北”、“东北区”\",\"西南安全防损部简称“西南大区”、“西南”、“西南区”\",\"苏皖安全防损部简称“苏皖大区”、“苏皖区”、“苏皖”\",\"西北安全防损部简称“西北大区”、“西北”、“西北区”\",\"豫鄂安全防损部简称“豫鄂大区”、“豫鄂”、“豫鄂区”\",\"鲁晋安全防损部简称“鲁晋大区”、“鲁晋”、“鲁晋区”\",\"湘赣安全防损部简称“湘赣大区”、“湘赣”、“湘赣区”\",\"粤海安全防损部简称“粤海大区”、“粤海”、“粤海区”\",\"西北安全防损部简称“西北大区”、“西北”、“西北区”\",\"西南安全防损部简称“西南大区”、“西南”、“西南区”\",\"桂闽安全防损部简称“桂闽大区”、“桂闽”、“桂闽区”\",\"豫鄂安全防损部简称“豫鄂大区”、“豫鄂”、“豫鄂区”\"]",
            "indicator_knowledge": "[{\"code\": \"1001\", \"name\": \"负责人\", \"nickName\": \"\"}, {\"code\": \"1002\", \"name\": \"运营负责人\", \"nickName\": \"\"},{\"code\": \"1003\", \"name\": \"防损负责人\", \"nickName\": \"防损人\"},{\"code\": \"1004\", \"name\": \"园区\", \"nickName\": \"物流园区\"},{\"code\": \"1005\", \"name\": \"场地\", \"nickName\": \"物流场地，场地数\"},{\"code\": \"1006\", \"name\": \"巡检任务\", \"nickName\": \"已完成任务,不足时间的任务\"},{\"code\": \"1007\", \"name\": \"例外闭环\", \"nickName\": \"异常修复，问题修复，隐患处理，隐患闭环\"}, {\"code\": \"1008\", \"name\": \"例外场地\", \"nickName\": \"异常的场地，隐患场地，列外场地\"},{\"code\": \"1009\", \"name\": \"例外人员\", \"nickName\": \"异常人员，隐患人员\"},{\"code\": \"1010\", \"name\": \"片区\", \"nickName\": \"物流片区，运营片区\"}]"
        },
        "response_mode": "blocking",
        "user": "lizhaojing7"
    }

    headers = {
        "Authorization": "Bearer app-XyH2IPYuoaOtz23RkhxirU70",
        "Content-Type": "application/json"
    }


    response = requests.post(url, json=data, headers=headers)
    # 检查请求是否成功
    response.raise_for_status()
    return response


def clean_json_string(json_string):
    # 去除```json\n和```字符
    cleaned_string = json_string.replace("```json\n", "").replace("```", "")
    return json.loads(cleaned_string)


def write_to_excel(data_list):

    output_file = '/Users/lizhaojing7/Downloads/response_data.xlsx'
    df = pd.DataFrame(data_list, columns=['问题', '耗时','结果'])

    # 追加数据到Excel文件
    filePath = "/Users/lizhaojing7/Downloads/response-4o.xlsx"
    with pd.ExcelWriter(filePath, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, index=False, header=True, sheet_name='Sheet2', startrow=writer.sheets['Sheet2'].max_row)


def main(path):
    lines = read_lines_from_file(path)
    data_list = []
    for line in lines:
        response = send_request(line)
        if response.status_code == 200:
            response_json = response.json()
            outputs = response_json['data']['outputs']['output']
            elapsed_time = response_json['data']['elapsed_time']
            # 处理outputs字段
            cleaned_outputs = clean_json_string(outputs)
            # 添加到数据列表中
            data_list.append([line, elapsed_time,json.dumps(cleaned_outputs, ensure_ascii=False)])
            print(f"{line} 处理结束")
        else:
            print(f"Failed to get response for input: {line}")

    # 写入Excel
    write_to_excel(data_list)
    print("全部跑批结束")



if __name__ == "__main__":
    file_path = '/Users/lizhaojing7/Downloads/question.txt'
    main(file_path)