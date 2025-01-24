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

# 'hepatocellular carcinoma'
# 查询药物关于疾病的报道信息
def get_drug_report_info(drug_ap, drug_cl, disease, input_num):
    drug_ap_not_report, drug_ap_report, drug_cl_not_report, drug_cl_report = [], [], [], []
    for drug_name in drug_ap:
        # 这个名字需要进行处理
        # 会出现特殊字符无法处理的情况[Avastin+/-Tarceva]
        drug_name = drug_name.replace(
            '+/-', ' ').replace(
            '/', ' ').replace(
            '[', '').replace(
            ']', '').replace(
            '-', ' ')
        query = {
            'query': {
                'bool': {
                    'must': [
                        {
                            "match": {
                                "abstract": drug_name
                            }
                        },
                        {
                            "match_phrase": {
                                "abstract": disease
                            }
                        },
                    ]
                }
            }
        }
        res = es.search(index='abstract22', body=query, scroll='5m')
        reported_number = res['hits']['total']['value']
        es.clear_scroll(scroll_id=res['_scroll_id'])
        if reported_number > input_num:
            drug_ap_report.append(drug_name)
        else:
            drug_ap_not_report.append(drug_name)
    for drug_name in drug_cl:
        drug_name = drug_name.replace(
            '+/-', ' ').replace(
            '/', ' ').replace(
            '[', '').replace(
            ']', '').replace(
            '-', ' ')
        query = {
            'query': {
                'bool': {
                    'must': [
                        {
                            "match": {
                                "abstract": drug_name
                            }
                        },
                        {
                            "match_phrase": {
                                "abstract": disease
                            }
                        },
                    ]
                }
            }
        }
        res = es.search(index='abstract22', body=query, scroll='5m')
        reported_number = res['hits']['total']['value']
        es.clear_scroll(scroll_id=res['_scroll_id'])
        if reported_number > input_num:
            drug_cl_report.append(drug_name)
        else:
            drug_cl_not_report.append(drug_name)
    return drug_ap_not_report, drug_ap_report, drug_cl_not_report, drug_cl_report


# 从药物列表获取药物的频率
def get_drug_frequency(drug_not_report, drug_report):
    drug_frequency = []
    if drug_not_report != []:
        for drug in drug_not_report:
            # 这个名字需要进行处理
            # 会出现特殊字符无法处理的情况[Avastin+/-Tarceva]
            drug_name = drug.replace(
                '+/-', ' ').replace(
                '/', ' ').replace(
                '[', '').replace(
                ']', '').replace(
                '-', ' ')
            query = {
                'query': {
                    "match": {
                        "abstract": drug_name
                    }
                }
            }
            res = es.search(index='abstract22', body=query, scroll='5m')
            reported_number = res['hits']['total']['value']
            drug_frequency.append(reported_number)
            es.clear_scroll(scroll_id=res['_scroll_id'])
    else:
        for drug in drug_report:
            drug_name = drug.replace(
                '+/-', ' ').replace(
                '/', ' ').replace(
                '[', '').replace(
                ']', '').replace(
                '-', ' ')
            query = {
                'query': {
                    "match": {
                        "abstract": drug_name
                    }
                }
            }
            res = es.search(index='abstract22', body=query, scroll='5m')
            reported_number = res['hits']['total']['value']
            drug_frequency.append(reported_number)
            es.clear_scroll(scroll_id=res['_scroll_id'])
    return drug_frequency


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