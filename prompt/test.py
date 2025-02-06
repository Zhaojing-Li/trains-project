from openai import OpenAI
from dotenv import load_dotenv

# 这是注释
word = 'ceshi'
sen = "hutu"
para = """test"""
#删除引用
#//del para
print(word); print(sen); print(para)


# 截取字符串 左闭右开 正序是从0开始； 逆序是从-1开始
new_para= para[0:2]
print (para[2:5])  # 输出字符串中第三个至第六个之间的字符串
print (para[2:])       # 输出从第三个字符开始的字符串
print (para * 2)       # 输出字符串两次
print(para[1:4:2])     # 取下标【1，4）其中步长为2


# 列表list[]   元组()不允许二次赋值    字典{}（kv结构）
tuple_1 = ( 'run', 786 , 2.23, 'john', 70.2 )
tiny_tuple = (123, 'john')


# 字典
my_dict = {}
my_dict['one'] = "This is one"
my_dict[2] = "This is two"
print('字典' + my_dict[2])


# 例：条件语句
num = 5
if num == 3:  # 判断num的值
    print()
    'boss'
elif num == 2:
    print()
    'user'
elif num == 1:
    print()
    'worker'
else:
    print()
    'roadman'  # 条件均不成立时输出


for num in range(10, 20):  # 迭代 10 到 20 (不包含) 之间的数字
    for i in range(2, num):  # 根据因子迭代
        if num % i == 0:  # 确定第一个因子
            j = num / i  # 计算第二个因子
            print('%d 等于 %d * %d' % (num, i, j))
            break  # 跳出当前循环
    else:  # 循环的 else 部分
        print('%d 是一个质数' % num)










