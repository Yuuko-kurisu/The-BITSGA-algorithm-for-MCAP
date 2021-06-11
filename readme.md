# Introduction

- Mcapplus项目的代码文件，暂分为以下三个部分
  - 整体思路
  - 编码方案
  - 文件介绍和命名格式（包括文件内函数）
  - 如何运行

# 整体思路

思路（按ctrl+单击跳转）

​	初始问题思路和蚁群+LKZK启发式

​		[初始思路](.//初始思路.pptx)

思路更改：

- 2021/6/3 把两个问题合二为一
- 蚁群算法优化
  - 对每种类型单独优化（不能跨类型，效果可能不好）
    - 方法1，可以考虑，因为局部交换算法也会嵌入，可以互补
  - 考虑基于交换的蚁群算法（另外参考cai论文）

# 编码方案

- 放弃mcap项目中的两层编码，改用一层编码，且为了兼容性，提供一个两层和一层编码转换的代码
  - 编码和region互相转换的代码（region复杂的话可以先不写）
  - region使用一层编码（使用字典实现）
    - 
  - 方案使用一层编码（一维数组，以及列表的相互转换）
    - 说明哪个组件在哪个位置即可
  - 组件选择
    - 可交换组件集
      - 如果组件非交叉位置，则可交换组件为同类型组件
      - 如果组件在交叉位置，可交换组件定义为同组组件和同类型组件（）

# 文件规划和命名

## 结果记录

### 小系统

路径
```python
'./result//now//smallsystem//'
# 记录文件用系统名字命名
# 总结文件命名为summary
# 修改算法或者其他操作后如果需要覆盖旧结果，先将旧结果转移到past文件夹，md文件表明实现来源
```

- 结果记录方式
  - 记录文件：index为seed，column为多层索引，第一层为type，第二层为sys和design
  - 总结文件：index为系统，column多层索引，第一层type，第二层MSSR，time1，time2

### 大系统

## 库文件-复用代码

- 命名(codehub+项目名)
  - codehub_mcapplus.py
- 组成
  - 以后可用的代码放Common类，本项目可用的代码放Project类
  - Common class
    - get_regiondict
      - 获取两个与位置相关的字典
      - 增加了两个与位置相关的字典 20210603
    - get_componentdict
      - 获取两个与组件相关的字典
    - ACO
      - 普通蚁群算法实现
  - Project class
    - is_design_true_p1	判断p1的design是否合法
    - system_reliability     系统可靠度计算（c++现成的）
    - bi_fun    bi值计算（现成的）
    - transfer_design       design转reliabilitylist（输入design和plist，输出reliabilitylist）
    - initial_design
      - 生成可行解
      - 参数为问题类型和初始类型（从最大或者最小开始）
    - zk zk算法
    - lk_p1
    - lk_p2
  - Case class
    - 整理需要的case

## 执行文件（得到论文结果）

- 命名
  - Execute_xxx.py
- 目录
  - Execute_smalltest.py
    - 选定一个小系统
    - 测试初始化design方法
    - 计算design可靠度
    - 测试zk算法
    - 测试BIACO算法
  - Execute_singlecase.py
    - 对单个算例执行BIACO，查看结果，用于调试（注意封装性）
    - 调试任务
      - 缩短biaco时间，调整算法和参数
      - 启发式算法时间调整
      - more问题求解
  - Execute_BIACO_initial.py
    - 执行普通的BIACO算法，记录各个系统的结果（大系统和小系统）
      - **如何记录结果**
        - 记录所有结果
        - 记录结果总结

## 测试文件

- 命名
  - test_xxx.py
- 目录
  - test_aco
    - 普通aco算法的测试
  - test_casestudy
    - 为不同系统选定组件数量pnums
    - 验证现有pnums的可行性
  - test_test.py
    - 测试文件

# 展示文件

- 一般是jupyter文件，用于展示或者运行结果
- 目录
  - result_process.ipynb
    - 读取记录的结果，并汇总各个系统对比

# 疑难

- 20210609
  - random方法，不能使用itertools，因为遍历太花时间，考虑其他方法
    - random.shuffle解决
      - 大多数解不符合要求，写一个生成可行随机真实解的方法
  
- 20210610

  - 代码分析

    [代码分析](.//代码分析结果.md)

