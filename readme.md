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

## 库文件-复用代码

- 命名(codehub+项目名)
  - codehub_mcapplus.py
- 组成
  - 以后可用的代码放Common类，本项目可用的代码放Project类
  - Common class
    - get_regiondict
      - 获取两个与位置相关的字典
    - get_componentdict
      - 获取两个与组件相关的字典
  - Project class
    - is_design_true_p1	判断p1的design是否合法
    - system_reliability     系统可靠度计算（c++现成的）
    - bi_fun    bi值计算（现成的）
    - transfer_design       design转reliabilitylist（输入design和plist，输出reliabilitylist）
    - 

## 执行文件（得到论文结果）

- 命名
  - Execute_xxx.py

## 测试文件

- 命名
  - test_xxx.py