## requirement



## 本地端使用方法

## 1. 数据下载
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


## 2. 启动搜索引擎
首先打开`elasticsearch-8.4.3`中的`bin`文件夹，运行`elasticsearch.bat`程序，
最后运行结果如下：

![figures\img_0.png](figures/img_0.png)


## 3. 数据输入
打开`Local OTTM` 文件夹然后把待分析的蛋白质组学数据，以txt格式放入文件夹，并将第一列
作为蛋白质的符号名称，范例如下：

![figures/img_1.png](figures/img_1.png)

## 4. 开始运行
双击`Protein_Driven_Drug_Targeting.exe`，等待运行结束后，可以在`ouput`文件夹中看到结果

## 5.结果分析
- 结果会根据配置中的输入参数（报告的数字）生成具有不同名称的文件夹。 
- 进一步的结果分为直接来自用户输入的蛋白质列表和通过蛋白质相互作用获得的PPI蛋白质列表。
每个文件夹的名称是推荐靶标的名称，文件夹中包含与该靶标对应的药物信息和药物的热度。
- 最后三个html文件显示了完整的靶点分类信息和编号，以及OTTM最终推荐的靶点和对应的药物。
