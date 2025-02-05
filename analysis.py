import json
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from output import drug_classify


def classify_targets_wm(Symbol_To_Target, Symbol_list):
    '''
    classify_targets: 根据给定的 Symbol_To_Target 字典和 Symbol_list 列表，对靶标（targets）进行西药分类。

    :param Symbol_To_Target:
    :param Symbol_list:
    :return:
        有药物的靶标（target_have_drug）：这些靶标在 Symbol_To_Target 字典中有对应的条目，即存在与之相关的药物信息。
        无药物的靶标（target_no_drug）：这些靶标在 Symbol_To_Target 字典中没有对应的条目，即没有与之相关的药物信息。
        FDA批准的靶标（target_FDA_approved）：这些靶标不仅有药物，而且这些药物已经成功通过FDA审批。
        临床试验中的靶标（target_clinical_trial）：这些靶标有药物，且这些药物目前处于临床试验阶段。
        其他靶标（target_others）：这些靶标有药物，但药物既不是FDA批准的，也不在临床试验中。
    '''
    target_have_drug, target_no_drug = [], []
    target_FDA_approved, target_clinical_trial, target_others = [], [], []

    for symbol in Symbol_list:
        if symbol in Symbol_To_Target.keys():
            target_have_drug.append(symbol)
        else:
            target_no_drug.append(symbol)

    for symbol in target_have_drug:
        target_phage = [*Symbol_To_Target[symbol].values()][0]
        target_name = [*Symbol_To_Target[symbol].keys()][0]
        drug_phase, drug_ap_cl, drug_ap, drug_cl = drug_classify(target_name)
        # 增加一个判断，如果symbol所在阶段确实存在对应的药物，则将其加入到对应的列表中
        if target_phage == 'Successful target' and drug_ap != []:
            target_FDA_approved.append(symbol)
        elif target_phage == 'Clinical Trial target' and drug_cl != []:
            target_clinical_trial.append(symbol)
        else:
            target_others.append(symbol)

    return target_have_drug, target_no_drug, target_FDA_approved, target_clinical_trial, target_others


def classify_targets_tcm(Symbol_To_Target, Symbol_list):
    '''
    classify_targets: 根据给定的 Symbol_To_Target 字典和 Symbol_list 列表，对靶标（targets）进行中药角度分类。

    :param Symbol_To_Target:
    :param Symbol_list:
    :return:
        有药物的靶标（target_have_drug）：这些靶标在 Symbol_To_Target 字典中有对应的条目，即存在与之相关的药物信息。
        无药物的靶标（target_no_drug）：这些靶标在 Symbol_To_Target 字典中没有对应的条目，即没有与之相关的药物信息。
        FDA批准的靶标（target_FDA_approved）：这些靶标不仅有药物，而且这些药物已经成功通过FDA审批。
        临床试验中的靶标（target_clinical_trial）：这些靶标有药物，且这些药物目前处于临床试验阶段。
        其他靶标（target_others）：这些靶标有药物，但药物既不是FDA批准的，也不在临床试验中。
    '''
    target_have_drug, target_no_drug = [], []
    target_FDA_approved, target_clinical_trial, target_others = [], [], []

    for symbol in Symbol_list:
        if symbol in Symbol_To_Target.keys():
            target_have_drug.append(symbol)
        else:
            target_no_drug.append(symbol)

    for symbol in target_have_drug:
        target_phage = [*Symbol_To_Target[symbol].values()][0]
        target_name = [*Symbol_To_Target[symbol].keys()][0]
        drug_phase, drug_ap_cl, drug_ap, drug_cl = drug_classify(target_name)
        # 增加一个判断，如果symbol所在阶段确实存在对应的药物，则将其加入到对应的列表中
        if target_phage == 'Successful target' and drug_ap != []:
            target_FDA_approved.append(symbol)
        elif target_phage == 'Clinical Trial target' and drug_cl != []:
            target_clinical_trial.append(symbol)
        else:
            target_others.append(symbol)

    return target_have_drug, target_no_drug, target_FDA_approved, target_clinical_trial, target_others


def classify_targets_html(target_have_drug, target_no_drug, target_FDA_approved,
                          target_clinical_trial, target_others, dir_name):
    '''
    将html中的数据进行更改后输出
    :param target_have_drug:
    :param target_no_drug:
    :param target_FDA_approved:
    :param target_clinical_trial:
    :param target_others:
    :param dir_name:
    :return:
    '''
    with open('config.json', 'r') as f:
        config = json.load(f)

    disease_name = config['disease_name']
    reported_number = config['reported_number']

    text_html = open(r'Template/target_pie_template.html',
                     'r', encoding='utf-8').read()
    text_html = text_html.replace(
        'Compound data', str(len(target_have_drug))).replace(
        'No-drug data', str(len(target_no_drug))).replace(
        'FDA Approved data', str(len(target_FDA_approved))).replace(
        'Others data', str(len(target_others))).replace(
        'Clinical data', str(len(target_clinical_trial)))

    soup = BeautifulSoup(text_html, 'html.parser')
    with open('output/' + disease_name + ' reported_number_' + str(
            reported_number) + '/' + dir_name + '/Targets_pie_chart.html', 'w', encoding='utf-8') as fp:
        fp.write(str(soup))


def query_target(symbol, Symbol_To_PubMedID, Symbol_To_UniprotID, Symbol_To_Fullname, keywords, file_path,
                 sheet_name='Sheet1'):
    """
    在指定的 xlsx 文件的 Abstract 列中检索与基因符号相关的摘要数量。
    :param symbol: 基因符号
    :param Symbol_To_PubMedID: 基因符号到 PubMed ID 的映射字典
    :param Symbol_To_UniprotID: 基因符号到 UniProt ID 的映射字典
    :param Symbol_To_Fullname: 基因符号到全称的映射字典
    :param keywords: 关键词列表
    :param file_path: xlsx 文件路径
    :param sheet_name: 工作表名称，默认为 'Sheet1'
    :return: 满足条件的摘要数量
    """
    # 读取 xlsx 文件
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 获取基因符号对应的 PubMed ID 和 UniProt ID
    uniprotID = Symbol_To_UniprotID.get(symbol, "")
    pubMedId = Symbol_To_PubMedID.get(symbol, "")

    # 初始化计数器
    reported_number_1 = 0
    reported_number_2 = 0

    # 检索 Abstract 列
    if 'Abstract' in df.columns:
        # 第一个查询：检索包含 PubMed ID、关键词和基因符号的摘要
        reported_number_1 = df[
            df['Abstract'].str.contains(pubMedId, na=False) &
            df['Abstract'].str.contains(keywords, na=False) &
            df['Abstract'].str.contains(symbol, na=False)
            ].shape[0]

        # 如果第一个查询没有结果，尝试第二个查询
        if reported_number_1 == 0:
            fullName = Symbol_To_Fullname.get(symbol, "")
            if fullName:
                # 第二个查询：检索包含关键词和基因符号或全称的摘要
                reported_number_2 = df[
                    df['Abstract'].str.contains(keywords, na=False) &
                    (df['Abstract'].str.contains(symbol, na=False) | df['Abstract'].str.contains(fullName, na=False))
                    ].shape[0]

    # 返回满足条件的摘要总数
    return reported_number_1 + reported_number_2

# 通过摘要中的关键词进行查询，将靶标分为对于该疾病报道过的靶标和没有报道过的靶标
def report_info(fa, ct, keywords, input_num):
    with open('data\ID_Transformed\Symbol_To_PubMedID.json', 'r') as f:
        Symbol_To_PubMedID = json.load(f)
    with open('data\ID_Transformed\Symbol_To_UniprotID.json', 'r') as f:
        Symbol_To_UniprotID = json.load(f)
    with open('data\ID_Transformed\Symbol_To_Fullname.json', 'r') as f:
        Symbol_To_Fullname = json.load(f)
    fda_no_review, fda_review, ct_no_review, ct_review = [], [], [], []
    for symbol in fa:
        # 存在有的symbol没有对应的uniprotID或者pubMedID 对于这样的symbol进行剔除
        if symbol in Symbol_To_PubMedID.keys() and symbol in Symbol_To_UniprotID.keys():
            query_num = query_target(symbol, Symbol_To_PubMedID, Symbol_To_UniprotID, Symbol_To_Fullname, es, keywords)
            if query_num > input_num:
                fda_review.append(symbol)
            else:
                fda_no_review.append(symbol)
    for symbol in ct:
        if symbol in Symbol_To_PubMedID.keys() and symbol in Symbol_To_UniprotID.keys():
            query_num = query_target(symbol, Symbol_To_PubMedID, Symbol_To_UniprotID, Symbol_To_Fullname, es, keywords)
            if query_num > input_num:
                ct_review.append(symbol)
            else:
                ct_no_review.append(symbol)
    return fda_no_review, fda_review, ct_no_review, ct_review