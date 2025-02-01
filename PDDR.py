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


def PDDR():
    '''
    整体Snoopy代码运行流
    :return: 返回result文件夹中的可视化方案及文件（可选）
    '''

    # step_1 环境配置
    sys.path.append('data/PPI')
    from PPI_target import get_targetNum_dict

    with open('config.json', 'r') as f:
        config = json.load(f)

    print('Welcome to use the new tool OTTM')
    print("-------------------------------------------------------------------")
    print('Please make sure to correctly fill in the configuration file')

    disease_name = config['disease_name']
    reported_number = config['reported_number']
    os.makedirs('output/' + disease_name + ' reported_number_' + str(reported_number), exist_ok=True)
    os.makedirs('output/' + disease_name + ' reported_number_' + str(reported_number) + '/Target', exist_ok=True)
    os.makedirs('output/' + disease_name + ' reported_number_' + str(reported_number) + '/PPI_Target', exist_ok=True)

    file_name = get.get_txt()

    # step_2.1 获得文件中的symbol
    Symbol_list = get.get_Symbol(file_name)
    print('The number of proteins in the file is: ', len(Symbol_list))

    # step_2.2 获取symbol对应的PPI蛋白 在这里只要跟差异表达蛋白拥有相互作用就进行保留
    # interaction_num = 0 已经存在相互作用的蛋白 最少应该和几个差异表达蛋白列表中的蛋白相互作用,可以设置为参数
    interaction_num = config['interaction_num']
    Symbol_PPI_list = get.get_PPI_Symbol_List(Symbol_list, interaction_num)

    print('The number of PPI proteins list is: ', len(Symbol_PPI_list))
    print('Please wait for a while, the program is running...')

    # 显示开始运行的时间
    t0=time.time()
    print('Program start time:',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

    # step_2.3 获取symbol对应靶标信息
    with open ('data/Drug/Symbol_To_Target.json', 'r') as f:
        Symbol_To_Target = json.load(f)

    with open ('data/ID_Transformed/Symbol_To_Fullname.json', 'r') as f:
        Symbol_To_Fullname = json.load(f)

    # step_3.1 PPI对应的靶标分类
    p_h_dr,p_no_dr,p_fa,p_ct,p_ot = analysis.classify_targets(Symbol_To_Target, Symbol_PPI_list)
    # step_3.2 symbol对应的靶标分类
    h_dr,no_dr,fa,ct,ot = analysis.classify_targets(Symbol_To_Target, Symbol_list)
    # step_3.3 将靶标分类信息输出到html中制作两张图分别保存到Target/PPI_Target文件夹中
    analysis.classify_targets_html(h_dr,no_dr,fa,ct,ot,'Target')
    analysis.classify_targets_html(p_h_dr,p_no_dr,p_fa,p_ct,p_ot,'PPI_Target')
    # step_3.4 symbol对应的靶标
    fda_no_review, fda_review ,ct_no_review, ct_review = analysis.report_info(fa,ct,disease_name, reported_number)
    p_fda_no_review, p_fda_review ,p_ct_no_review, p_ct_review = analysis.report_info(p_fa,p_ct,disease_name, reported_number)

    # step_4.生成靶标信息的Tree图
    output.all_targets_tree(fda_no_review, fda_review ,ct_no_review, ct_review,'Target')
    output.all_targets_tree(p_fda_no_review, p_fda_review ,p_ct_no_review, p_ct_review,'PPI_Target')

    t1=time.time()
    print('Program end time:',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print("Running Time：%.6fs"%(t1-t0))

    print('The number of recommend targets is: ', len(fda_no_review + ct_no_review))
    print('The number of recommend PPI targets is: ', len(p_fda_no_review + p_ct_no_review))

    # step3.5_生成靶标列表
    target_max_number = config['target_max_number'] # 靶标推荐最大值,根据文献数量进行排序

    no_review = fda_no_review + ct_no_review
    p_no_review = p_fda_no_review + p_ct_no_review

    fda_no_review = output.new_targets_list(fda_no_review,output.sort_targets(no_review, target_max_number))
    ct_no_review = output.new_targets_list(ct_no_review,output.sort_targets(no_review, target_max_number))
    p_fda_no_review = output.new_targets_list(p_fda_no_review,output.sort_targets(p_no_review, target_max_number))
    p_ct_no_review = output.new_targets_list(p_ct_no_review,output.sort_targets(p_no_review ,target_max_number))

    # 获得全部靶标药物推荐的旭日图，以及每个靶标对应的药物信息和药物热度
    output.get_sunburst_tree_bar('Target', fda_no_review, ct_no_review, fa, disease_name, reported_number)
    output.get_sunburst_tree_bar('PPI_Target', p_fda_no_review, p_ct_no_review, p_fa, disease_name, reported_number)

    print('The program is finished!')
    print('-------------------------------------------------------------------')
    input('Please enter any key to exit')


if __name__ == "__main__":
    PDDR(output_for_pyecharts = True,
         re = True,
         path = "output/")
