import textwrap
import pandas as pd
import time
import get
import sys
import os
import json
import analysis
from elasticsearch import Elasticsearch
import output
import analysis


def set_config_auto():
    with open('config.json', 'r') as f:
        config = json.load(f)

    disease_name = config['disease_name']
    reported_number = config['reported_number']
    interaction_num = config['interaction_num']

    os.makedirs('output/' + disease_name + ' reported_number_' + str(reported_number), exist_ok=True)
    os.makedirs('output/' + disease_name + ' reported_number_' + str(reported_number) + '/Target', exist_ok=True)
    os.makedirs('output/' + disease_name + ' reported_number_' + str(reported_number) + '/PPI_Target', exist_ok=True)

    return disease_name, reported_number, interaction_num


def get_data(protein_list_path, interaction_num):
    sys.path.append('data/PPI')
    from PPI_target import get_targetNum_dict

    file_name = protein_list_path
    Symbol_list = get.get_Symbol(file_name)

    print('The number of proteins in the file is: ', len(Symbol_list))

    # step_2.2 获取symbol对应的PPI蛋白 在这里只要跟差异表达蛋白拥有相互作用就进行保留
    # interaction_num = 0 已经存在相互作用的蛋白 最少应该和几个差异表达蛋白列表中的蛋白相互作用,可以设置为参数

    Symbol_PPI_list = get.get_PPI_Symbol_List(Symbol_list, interaction_num)

    print('The number of PPI proteins list is: ', len(Symbol_PPI_list))
    print('Please wait for a while, the program is running...')

    t0=time.time()
    print('Program start time:',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

    with open ('data/Drug/Symbol_To_Target.json', 'r') as f:
        Symbol_To_Target_wm = json.load(f)

    with open ('data/ID_Transformed/Symbol_To_Fullname.json', 'r') as f:
        Symbol_To_Fullname = json.load(f)

    return Symbol_PPI_list, Symbol_To_Target_wm, Symbol_To_Fullname, Symbol_list


def PDDR(protein_list_path):
    '''
    整体Snoopy代码运行流
    :return: 返回result文件夹中的可视化方案及文件（可选）
    '''
    disease_name, reported_number, interaction_num = set_config_auto()

    Symbol_PPI_list, Symbol_To_Target_wm, Symbol_To_Fullname, Symbol_list = get_data(protein_list_path, interaction_num)

    p_h_dr,p_no_dr,p_fa,p_ct,p_ot = analysis.classify_targets_wm(Symbol_To_Target_wm, Symbol_PPI_list)
    h_dr,no_dr,fa,ct,ot = analysis.classify_targets_wm(Symbol_To_Target_wm, Symbol_list)

    analysis.classify_targets_html(h_dr,no_dr,fa,ct,ot,'Target')
    analysis.classify_targets_html(p_h_dr,p_no_dr,p_fa,p_ct,p_ot,'PPI_Target')




if __name__ == "__main__":
    PDDR(protein_list_path = "Example_protein_list.txt")