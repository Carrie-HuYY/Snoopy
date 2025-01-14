import os
import json
import sys

def get_txt():
    '''
    获取当前地址文件夹中所有txt的文件名
    :return: 返回文件名
    '''
    for file_name in os.listdir():
        if file_name.endswith('.txt'):
            return file_name

#
def get_Symbol(file_name):
    '''
    返回
    :param file_name:
    :return:
    '''
    with open(file_name, 'r', encoding='utf-8') as f:
        f = f.readlines()
    Symbol = []

    for i in f:
        i = i.replace('\t', ' ').replace('\n', '').split(' ')
        Symbol.append(i[0])

    return Symbol


def get_PPI_Symbol_List(symbol_list, interaction_num):
    '''
    获取PPI列表
    '''
    with open ('data/PPI/PPI.json', 'r') as f:
        PPI_DICT = json.load(f)

    sys.path.append('data/PPI')
    from PPI_target import get_targetNum_dict

    TARGET_PPI = get_targetNum_dict(symbol_list, interaction_num, PPI_DICT)
    TARGET_PPI_LIST = [i for i in TARGET_PPI.keys() if i not in symbol_list]

    return TARGET_PPI_LIST