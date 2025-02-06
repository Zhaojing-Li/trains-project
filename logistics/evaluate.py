import pandas as pd
import string

def preprocess_string(s):
    if isinstance(s, str):
        # 移除空格、换行符和标点符号
        s = (s.replace(" ", "").replace("\n", "").replace("\r", "")
             .replace("?", ""))
        s = s.translate(str.maketrans('', '', string.punctuation))
    return s


def process_excel(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path, engine='openpyxl')

    # 确保 DataFrame 有足够的列
    # if df.shape[1] < 9:
    #     raise ValueError("输入的 Excel 文件至少需要有 9 列")

    # 创建一个空的列表来存储结果
    results = []

    # 逐行处理数据
    for index, row in df.iterrows():
        col3 = preprocess_string(row.iloc[0])
        col5 = preprocess_string(row.iloc[1])
        # col7 = preprocess_string(row.iloc[6])

        # 比较这三个数据是否相同
        # if col3 == col5 == col7:
        #     result = 1
        # else:
        #     result = 0

        if col3 == col5:
            result = 1
        else:
            result = 0

        # 将结果添加到列表中
        results.append(result)

    # 将结果写入第9列
    df.iloc[:, 2] = results

    # 将修改后的 DataFrame 写回到同一个 Excel 文件
    df.to_excel(file_path, index=False, engine='openpyxl')



def main():
    # 使用函数
    file_path = '/Users/lizhaojing7/Downloads/test.xlsx'  # 输入文件名
    process_excel(file_path)


# 使用函数
if __name__ == "__main__":
    main()

