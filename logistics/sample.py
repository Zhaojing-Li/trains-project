import pandas as pd
import json
import ast
from collections import defaultdict
import random

def filter_profession(indicator,filter_profession_type) -> bool:
    if 'specialtyType' not in indicator:
        return False
    elif indicator['specialtyType'] == filter_profession_type:
        return True
    else:
        return False


def filter_task(indicator,task_type) -> bool:
    if 'taskType' not in indicator:
        return False
    elif indicator['taskType'] == task_type:
        return True
    else:
        return False

def main():
    file_path = '/Users/lizhaojing7/Downloads/巡检数据增强-v1_标注.xlsx'
    output_file = '/Users/lizhaojing7/Downloads/work.xlsx'

    filter_time = 'LATEST_QUARTER'
    filter_indicator = '1008'
    filter_intend = 'QUERY_RATIO'

    filter_task_type = 'SPECIALIZED_TASK'
    filter_profession_type = 'LOSS_SPECIALITY'


    sample_size = 7
    filtered_questions = []
    filtered_answers = []

    df = pd.read_excel(file_path, engine='openpyxl')
    info_counts = defaultdict(int)

    for index, row in df.iterrows():
        out = row['final_all_output']
        question= row['final_input']
        answer = ast.literal_eval(out)

        duration_list = answer['result'][0]['duration']
        indicators_list = eval(answer['result'][0]['indicators'])

        if not duration_list:
            duration_match = False
        else:
            if isinstance(duration_list, list):
                duration_match = any(d['type'] == filter_time for d in duration_list)
            elif isinstance(duration_list, dict):
                duration_match = duration_list['type'] == filter_time
            else:
                duration_match = False




        #是否有满足条件的数据
        duration_match = True
        # if not duration_list:
        #     duration_match = False
        # else:
        #     if isinstance(duration_list, list):
        #         duration_match = any(d['type'] == filter_time for d in duration_list)
        #     elif isinstance(duration_list, dict):
        #         duration_match = duration_list['type'] == filter_time
        #     else:
        #         duration_match = False

        if not indicators_list:
            indicator_match = False
        else:
            if isinstance(indicators_list, list):
                indicator_match = any(ind['indicator'] == filter_indicator and
                                      ind['intent'] == filter_intend
                                      # and filter_profession(ind,filter_profession_type)
                                      # and filter_task(ind,filter_task_type)
                                      for ind in indicators_list)
            elif isinstance(indicators_list, dict):
                indicator_match = (indicators_list['indicator'] == filter_indicator and indicators_list['intent'] == filter_intend)
            else:
                indicator_match = False


        if duration_match and indicator_match :
            filtered_questions.append(question)
            filtered_answers.append(answer)

            # 如果符合条件的行已经达到20条，则停止读取
            if len(filtered_answers) >= 30:
                break


    # 从符合条件的记录中随机抽取sample_size条
    if len(filtered_questions) > sample_size:
        sampled_indices = random.sample(range(len(filtered_questions)), sample_size)
        sampled_questions = [filtered_questions[i] for i in sampled_indices]
        sampled_answers = [filtered_answers[i] for i in sampled_indices]
    else:
        sampled_questions = filtered_questions
        sampled_answers = filtered_answers


    # 将抽取的行转换为DataFrame
    sampled_df = pd.DataFrame({'问题': sampled_questions, '答案': sampled_answers})

    with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        sampled_df.to_excel(writer, index=False, header=False, sheet_name='Sheet1', startrow=writer.sheets['Sheet1'].max_row)





if __name__ == "__main__":
    main()