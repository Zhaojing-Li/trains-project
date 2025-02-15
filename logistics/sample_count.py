import pandas as pd
import openpyxl
import ast
from collections import defaultdict
from itertools import combinations
import Levenshtein
import heapq
import itertools
from Levenshtein import distance as levenshtein_distance

def main():
    file_path = '/Users/lizhaojing7/Downloads/巡检数据增强-v1_标注.xlsx'
    output_file = '/Users/lizhaojing7/Downloads/work.xlsx'


    df = pd.read_excel(file_path, engine='openpyxl')

    info_counts = defaultdict(int)
    group_info = defaultdict(int)
    for index, row in df.iterrows():
        out = row['final_all_output']
        question = row['final_input']
        answer = ast.literal_eval(out)

        duration_list = answer['result'][0]['duration']
        indicators_list = eval(answer['result'][0]['indicators'])


        if not indicators_list:
            info = 'NONE'
        else:
            if isinstance(indicators_list, list):
                for indicators in indicators_list:
                    send_info_to_group(duration_list, indicators, group_info,question,out)
            elif isinstance(indicators_list, dict):
                send_info_to_group(duration_list, indicators_list, group_info,question,out)


    max_distance = -1
    most_different_pair = None
    different_dict = defaultdict(int)
    for key_info, qa_list in itertools.islice(group_info.items(), 1):
    #for key_info, qa_list in group_info.items():
        print('进入相似度比较')
        most_different_pair = find_most_different_objects(qa_list)
        # for (obj1, obj2) in combinations(qa_list, 2):
        #     distance = Levenshtein.distance(obj1['query'], obj2['query'])
        #     if distance > max_distance:
        #         max_distance = distance
        #         most_different_pair = [obj1, obj2]
        if key_info not in different_dict:
            different_dict[key_info] = []
        different_dict[key_info].append(most_different_pair)
        print('比较结束')


    #进行输出
    data_list = []
    for key_info, count in different_dict.items():
        print(count)
        result = count[0]
        print(result)
        print(result[0][0]['query'])
        parts = key_info.split('&')
        for i in range(8):
            data_list.append([parts[0],parts[1],parts[2],parts[3],parts[4],result[i][0]['query'],result[i][0]['answer']])
            data_list.append([parts[0], parts[1], parts[2], parts[3], parts[4], result[i][1]['query'], result[i][1]['answer']])
    df = pd.DataFrame(data_list, columns=['intent','indicator','duration', 'specialtyType','taskType','query','answer'])
    with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, index=False, header=True, sheet_name='Sheet1',
                    startrow=writer.sheets['Sheet1'].max_row)





def find_most_different_objects(obj_list):
    print('编辑距离计算')
    max_distance = -1
    # most_different_pair = None
    heap = []
    if len(obj_list)> 1000:
        obj_list = obj_list[:1000]

    for obj1, obj2 in itertools.combinations(obj_list, 2):
        processed_query1 = process_query(obj1)
        processed_query2 = process_query(obj2)
        distance = levenshtein_distance(processed_query1, processed_query2)

        heap_element = (distance, id(obj1), id(obj2), obj1, obj2)

        if len(heap) <= 8:
            heapq.heappush(heap, heap_element)
        elif distance > heap[0][0]:
            heapq.heappushpop(heap,heap_element)

    heap.sort(reverse=True, key=lambda x: x[0])
    print(heap)

    print('计算结束')
    return [(obj1, obj2) for _, _, _, obj1, obj2 in heap]
        # if distance > max_distance:
        #     max_distance = distance
        #     most_different_pair = [obj1, obj2]
    # return heap



def process_query(obj):
    query = obj['query']
    answer = ast.literal_eval(obj['answer'])
    key = ast.literal_eval(answer['result'][0]['logisticTier'])[0]['key']
    if key:
        query = query.replace(key, '')
    return query.strip()




# 分组数据组装
def send_info_to_group(duration_list, indicators, group_info,question,out):
    indicator = indicators['indicator']
    intent = indicators['intent']
    specialtyType = 'NONE' if 'specialtyType' not in indicators else indicators['specialtyType']
    taskType = 'NONE' if 'taskType' not in indicators else indicators['taskType']

    info = intent + '&' + indicator + '&' + specialtyType + '&' + taskType
    if not duration_list:
        info = info + '&' + 'NONE'
        if info not in group_info:
            group_info[info] = []
        group_info[info].append({'query': question, 'answer': out})

    else:
        if isinstance(duration_list, list):
            for duration in duration_list:
                info = info + '&' + duration['type']
                if info not in group_info:
                    group_info[info] = []
                group_info[info].append({'query': question, 'answer': out})
        elif isinstance(duration_list, dict):
            info = info + '&' + duration_list['type']
            if info not in group_info:
                group_info[info] = []
            group_info[info].append({'query': question, 'answer': out})


def count_num(duration_list, indicators, info_counts):
    intent = indicators['intent']
    indicator = indicators['indicator']
    specialtyType = 'NONE' if 'specialtyType' not in indicators else indicators['specialtyType']
    taskType = 'NONE' if 'taskType' not in indicators else indicators['taskType']

    info = intent + '&' + indicator + '&' + specialtyType + '&' + taskType
    if not duration_list:
        info = info + '&' + 'NONE'
        info_counts[info] += 1
    else:
        if isinstance(duration_list, list):
            for duration in duration_list:
                info = info + '&' + duration['type']
                info_counts[info] += 1
        elif isinstance(duration_list, dict):
            info = info + '&' + duration_list['type']
            info_counts[info] += 1




if __name__ == "__main__":
    main()