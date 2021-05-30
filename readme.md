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

# 文件规划和命名

## 库文件-复用代码

- 命名(codehub+项目名)
  - codehub_mcapplus.py
- 组成
  - 以后可用的代码放Common类，本项目可用的代码放Project类
  - Common class
  - Project class

## 执行文件（得到论文结果）

- 命名
  - Execute_xxx.py

## 测试文件

- 命名
  - test_xxx.py