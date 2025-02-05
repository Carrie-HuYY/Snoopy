## 目录

[背景](#背景)
- [现行方案](#ottm设计思路)
- [优化方案](#snoopy优化方案)

[项目介绍](#snoopy整体介绍)
- [药物可用性评价](#1药物可用性评估)
- [文献挖掘](#2文献挖掘)
- [输出结果](#3输出结果)

[安装](#安装)

[使用](#使用)
- [配置文件与数据](#配置文件与数据)
- [使用](#使用)

[附1：Snnopy的支撑数据](#附1snnopy的支撑数据)

[附2：OTTM本地端使用方法](#附2ottm本地端使用方法)

## 背景
[OTTM项目](https://github.com/YXB-OTTM/OTTM)给出一个很有趣的思路，基于文献计量学进行“以靶找药”的药物推荐。
所以学习OTTM做一个“中西结合”的，更适用于中药宝宝体质的项目：Snoopy

### OTTM设计思路

### [Snoopy](https://github.com/Carrie-HuYY/Snoopy)优化方案

- 对数据集进行优化更新，添加中药和药监局信息
- 推荐用药中增加推荐的中药及中药方剂信息，并给出NMPA安全检测
- 更改其使用的Elasticsearch，采用本地端形式保存数据
- 优化拆分代码结构，提高代码可读性，便于本地运行
- 优化可视化方案并将整体包装成Python包的形式

## Snoopy整体介绍

Snoopy通过药物可用性评估和文献挖掘，将大量候选蛋白或基因分类，以缩小需要进一步
验证的范围，从而提高从组学数据中发现有效药物和靶点的效率。Snoopy主要步骤如下：
### 1.药物可用性评估

#### 1.1 基于TTD的DEP/DEG对应药物检查
首先检查每个差异表达蛋白（DEP）或差异表达基因（DEG）是否有对应的药物。
这一过程基于[TTD数据库](https://db.idrblab.net/)中的药物-靶点配对信息。
Snoopy将候选蛋白分为两类：
- `With Drug`：有对应药物的蛋白
- `No Drug`：没有对应药物的蛋白

#### 1.2 基于[NBSD](https://github.com/Carrie-HuYY/Snoopy)的DEP/DEG对应中药/方剂检查
其次检查每个差异表达蛋白（DEP）或差异表达基因（DEG）是否有对应的中药及方剂。
这一过程基于各数据库中的中药-化合物-靶点配对信息（数据与检索功能来自于NBSD项目），
Snoopy将候选蛋白分为两类：
- `with TCM`：有对应中药的蛋饼
- `No TCM`：没有对应中药的蛋白

#### 1.3 基于FDA的是否批准检查
对于有对应药物的蛋白，Snoopy进一步将其分为三个子类：

- `FDA Approved`：已获得FDA批准的药物的靶点
- `Clinical Trials`：正在进行临床试验的药物的靶点
- `Others`：不属于上述两类的靶点。

#### 1.4 基于[NMPA国家药监局](https://www.nmpa.gov.cn/)的安全性检查
对于有对应中药的蛋白，Snoopy进一步将其分为两个子类：
- `NMPA Approved TCM`: 已有对应作用并获得NMPA批准中药的靶点
- `NMPA Approved Formula`: 已有对应作用并获得NMPA批准方剂的靶点
- `Others`：不属于上述两类的靶点


### 2.文献挖掘
Snoopy通过文献挖掘进一步筛选出那些尚未被报道与疾病相关的蛋白。

首先，Snoopy在PubMed数据库中搜索所有可用的摘要，使用疾病名称（如“肝细胞癌”）作为关键词。
如果候选蛋白或其对应的药物与指定的疾病关键词出现在同一篇PubMed摘要中，
则该蛋白或药物被认为`Reported`，并被排除在进一步评估之外。

### 3.输出结果
OTTM的输出结果包括四种类型：
- WM靶点分类饼图：展示有无药物的蛋白统计，以及不同药物状态`FDA Approved/Clinical Trials/Others`的蛋白统计。
- TCM靶点分类饼图：展示有无中药、方剂的蛋白统计，以及不同药物状态`NMPA Approved TCM/NMPA Approved Formula/Others`的蛋白统计。
- 靶点分类树状图：以树状图形式展示靶点的分类，便于用户直观了解分类结果。
- 药物推荐旭日图：以旭日图形式展示推荐药物/中药/方剂及其对应靶点，不同颜色区分不同分类。
- 每个靶点蛋白的药物树状图：为每个靶点蛋白生成一个树状图，展示其对应的药物分类和文献流行度。


## 安装

暂未开放，准备用Python包的形式用pip下载

## 使用

### 配置文件与数据
此外，OTTM还提供了一个配置文件，用户可以通过该文件控制推荐药物的数量。

### 核心代码
Snoopy包含三个主程序以及核心代码：
- `PDDR.py`：(Protein_Driven_Drug_Targeting.py, PDDR)主程序，用于配置环境，生成运行流。


- `get.py`:读取目标靶点以及PPI列表以进行后续分
  - get_drug_report_info: 查询与特定疾病相关的药物报告信息，并将这些信息分类为已报道和未报道的药物
  - get_drug_frequency: 从药物列表获取药物的频率
  - get_PPI_Symbol_List: 获取PPI列表
  - get_Symbol：获取目标靶点列表
  

- `analysis.py`:
  - classify_targets:据给定的 Symbol_To_Target 字典和 Symbol_list 列表，对靶标（targets）进行分类
  - classify_targets_html:将html中的数据进行更改后输出
  - query_target:查询既要满足摘要在限定的列表中 又要满足这些摘要中存在HCC这个词组，还要在全部的摘要中输入的symbol和uniprotID
  - report_info:通过摘要中的关键词进行查询，将靶标分为对于该疾病报道过的靶标和没有报道过的靶标


- `output.py`:
  - all_targets_tree:
  - get_excel
  - get_sunburst_tree_bar
  - sort_targets
  - get_sunburst



### 附1：Snnopy的支撑数据
整体大小为9个G，由于百度网盘限制，所以拆分成三个压缩包，解压后放data/文件夹即可

[下载链接1](#https://pan.baidu.com/s/1w0cHqaoUaa_FtPPDLFTrAQ?pwd=jkd7) 提取码: jkd7

[下载链接2](#https://pan.baidu.com/s/1tg8WQtJiJi70A8HIRYG_PA?pwd=9bvh) 提取码: 9bvh

[下载链接3](#https://pan.baidu.com/s/1tg8WQtJiJi70A8HIRYG_PA?pwd=9bvh) 提取码: 9bvh


### 附2：OTTM本地端使用方法

#### 1. 数据下载
从[OTTM官网](http://otter-simm.com/downloads.html)下载以下两个文件，
并且将其解压到相同的文件夹中，数据展示如下：

| Data      | 描述            | 压缩文件名          | 解压后文件名              |
|-----------|---------------|----------------|---------------------|
| 2023-3-20 | Abstract Data | OTTM_AD_20230320 | elasticsearch-8.4.3 |
| 2023-3-20 | Local Program | OTTM_LP_20230320 | Local OTTM          |

[OTTM_AD_20230320.zip](https://pan.baidu.com/s/12gSqSnTNkKnfcv45qul-JA?pwd=r314)
(**提取码: r314**)

[OTTM_LP_20230320.zip](https://pan.baidu.com/s/1PioCFwmTPOuv9Ib02yGPmA?pwd=swvy)
(**提取码: swvy**)


#### 2. 启动搜索引擎
首先打开`elasticsearch-8.4.3`中的`bin`文件夹，运行`elasticsearch.bat`程序，
最后运行结果如下：

![figures\img_0.png](figures/img_0.png)

如果执行elasticsearch时报错：
java.nio.file.NoSuchFileException: D:XXXX\Java\jdk-17\lib\tools.jar。 

解决方法：直接删除系统环境变量中的CLASSPATH。

#### 3. 数据输入
打开`Local OTTM` 文件夹然后把待分析的蛋白质组学数据，以txt格式放入文件夹，并将第一列
作为蛋白质的符号名称，范例如下：

![figures/img_1.png](figures/img_1.png)

#### 4. 开始运行
双击`Protein_Driven_Drug_Targeting.exe`，等待运行结束后，可以在`ouput`文件夹中看到结果

#### 5.结果分析
- 结果会根据配置中的输入参数（报告的数字）生成具有不同名称的文件夹。 
- 进一步的结果分为直接来自用户输入的蛋白质列表和通过蛋白质相互作用获得的PPI蛋白质列表。
每个文件夹的名称是推荐靶标的名称，文件夹中包含与该靶标对应的药物信息和药物的热度。
- 最后三个html文件显示了完整的靶点分类信息和编号，以及OTTM最终推荐的靶点和对应的药物。
