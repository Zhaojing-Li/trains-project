import json
import ast


def convert_to_json(input_data):
    # 将单引号替换为双引号
    input_data = input_data.replace("\\","").replace("'", '"')

    # 将字符串转换为字典
    data = json.loads(input_data)

    # 处理answer部分
    answer = json.loads(data['answer'])
    result = answer['result'][0]

    # 处理logisticTier
    logistic_tier_str = result['logisticTier']
    logistic_tier_dict = ast.literal_eval(logistic_tier_str)
    result['logisticTier'] = logistic_tier_dict[0] if isinstance(logistic_tier_dict, list) else logistic_tier_dict

    # 处理indicators
    indicators_str = result['indicators']
    indicators_list = ast.literal_eval(indicators_str)
    result['indicators'] = indicators_list if isinstance(indicators_list, list) else [indicators_list]

    # 处理duration
    duration_dict = result['duration']
    result['duration'] = [duration_dict] if isinstance(duration_dict, dict) else duration_dict

    # 更新answer
    answer['result'] = [result]
    data['answer'] = json.dumps(answer, ensure_ascii=False)

    # 返回最终的JSON格式数据
    return json.dumps(data, ensure_ascii=False)



def conversion(input_data):
    answer_ast = ast.literal_eval(input_data['answer'])
    answer_dict = json.loads(answer_ast)

    # 处理logisticTier
    for result in answer_dict['result']:
        logistic_tier_str = result['logisticTier']
        logistic_tier_dict = json.loads(logistic_tier_str)
        result['logisticTier'] = logistic_tier_dict[0] if isinstance(logistic_tier_dict, list) else logistic_tier_dict

        # 处理indicators
        indicators_str = result['indicators']
        indicators_list = json.loads(indicators_str)
        result['indicators'] = indicators_list if isinstance(indicators_list, list) else [indicators_list]

        # 处理duration
        duration_dict = result['duration']
        result['duration'] = [duration_dict] if isinstance(duration_dict, dict) else duration_dict

    # 将整个数据转换为JSON格式
    output_data = {
        "query": input_data['query'],
        "answer": answer_dict
    }

    # 输出JSON格式的字符串
    output_json = json.dumps(output_data, ensure_ascii=False)
    print(output_json)


if __name__ == '__main__':
    query = {'query': '绥化明水营业部上一周巡检中未发现任何例外的场地数量是多少？', 'answer': '{\'result\': [{\'logisticTier\': \'[{"provinceCode": "230000", "key": "绥化明水营业部", "tier": "SITE", "type": "CURRENT"}]\', \'indicators\': \'[{"intent": "QUERY_QUANTITY", "indicator": "1008"}]\', \'duration\': {\'key\': \'1\', \'type\': \'LAST_WEEK\'}}]}'}
    #conversion(query)
    convert_to_json(query)