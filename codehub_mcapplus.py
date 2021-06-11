'''
mcapplus项目的库文件
'''
import numpy as np
from collections import defaultdict
from ctypes import *
import pandas as pd
import copy
import itertools
import math
import pandas as pd
import time
import matplotlib.pyplot as plt
#%%
class Common():
    def main(self):
        pass
    def get_regiondict(self,region_2D):
        '''
        输入两层编码，字典
        case ： region = np.array([np.array([1, 2, 3]), np.array([3, 4, 5, 6, 7]), np.array([5, 6, 7, 8])])
        return ： region_1D = np.array([np.array([1, 2, 3]), np.array([3, 4, 5, 6, 7]), np.array([5, 6, 7, 8])])
        :param region_2D:
        :return:
        '''
        # 获取region_dict
        Length = len(region_2D)
        region_dict = defaultdict(list)
        for index in range(1,Length+1):
            region_dict[index] = region_2D[index-1]
        # 获取position_dict
        position_dict = defaultdict(list)

        for type in range(1,len(region_2D)+1):
            position_list = region_2D[type-1]
            for position_index in position_list:
                if position_index not in position_dict.keys():
                    position_dict[position_index] = np.array([type])
                else:
                    type_list = position_dict[position_index]
                    position_dict[position_index] = np.append(type_list,type)
        # position_type_dict
        position_type_dict = defaultdict(list)
        position_index_dict = defaultdict(list)
        positionnum = max(position_dict.keys())
        count = 0
        for position_index in range(1, positionnum + 1):
            if position_index == 1:
                count = count + 1
            elif (position_dict[position_index] == position_dict[position_index - 1]).all() == False:
                count = count + 1
            position_typenum = count
            position_type_dict[position_index] = position_typenum
            if position_typenum not in position_index_dict.keys():
                position_index_dict[position_typenum] = np.array([position_index])
            else:
                position_indexlist = position_index_dict[position_typenum]
                position_index_dict[position_typenum] = np.append(position_indexlist,np.array([position_index]))
        return region_dict,position_dict,position_type_dict,position_index_dict
    def get_componentdict(self,pnums):
        '''

        '''
        component_type_dict = defaultdict(list)
        component_index_dict = defaultdict(list)
        #1
        pnum = pnums.cumsum()
        pnum = np.append(np.array([0]), pnum)
        for type in range(1, len(pnums) + 1):
            start = pnum[type - 1] + 1
            end = pnum[type] + 1
            component_list = np.arange(start, end)
            component_index_dict[type] = component_list
            for component_index in component_list:
                component_type_dict[component_index] = type
        return component_type_dict,component_index_dict
    def get_true_pnums(self,region,position_index_dict,positionnum,problem_type=1):
        typenum = len(region)
        pnums_list = []
        position_typeonly = defaultdict(list)
        position_max = defaultdict(list)
        for type_index in range(1,typenum+1):
            position_list = position_index_dict[2 * type_index - 1]
            position_typeonly[type_index] = len(position_list)
            position_max[type_index] = len(region[type_index-1])
        if problem_type == 1:
            if typenum == 3:
                for a in range(position_typeonly[1],position_max[1]+1):
                    for b in range(position_typeonly[2],position_max[2]+1):
                        for c in range(position_typeonly[3], position_max[3] + 1):
                            if a + b + c == positionnum:
                                pnums_list.append([a,b,c])
        else:
            if typenum == 3:
                for a in range(position_typeonly[1],position_max[1]+1):
                    for b in range(position_typeonly[2],position_max[2]+1):
                        for c in range(position_typeonly[3], position_max[3] + 1):
                            if a + b + c > positionnum:
                                pnums_list.append([a,b,c])
        return pnums_list
class Project():
    def __init__(self,region_dict,position_dict,position_type_dict,position_index_dict,component_index_dict,component_type_dict,plist,pattern,k,pnums,seed):
        self.region_dict = region_dict #区域字典：输入组件类型返回位置列表
        self.position_dict = position_dict#位置字典，输入位置返回类型列表
        self.position_type_dict = position_type_dict#位置字典，输入位置，返回位置类型（num）
        self.position_index_dict = position_index_dict#位置字典，输入位置类型（typenum），输出位置列表（交叉位置单独一类）
        self.component_type_dict = component_type_dict#组件字典，输入组件序号，返回类型
        self.component_index_dict = component_index_dict #组件字典，输入类型，返回组件序号列表
        self.plist = plist #可靠度的一维数组，输入序号返回可靠度
        self.pattern = pattern
        self.k = k
        self.typenum = len(region_dict)
        self.positionnum = region_dict[self.typenum][-1]
        self.pnums = pnums
        self.seed = seed
        #c++
        dll = cdll.LoadLibrary('D:\\users\\yukko\\Documents\\Visual Studio 2015\\Projects\\Win32Project2\\x64\\Debug\\Win32Project2.dll')
        sysfun = dll.system_reliability
        sysfun.argtype = [c_int, c_int, c_int, POINTER(c_double)]
        sysfun.restype = c_double
        self.sysfun = sysfun
    #@profile
    def is_design_true(self,design,designtype=True):
        '''
        输入design判断分配方案是否可行
        designtype : 是否为可行解，如果为false说明是占位解（initial design）
        :return:bool
        '''
        if len(design) != len(set(design)):
            if designtype == True:
                return False
        component_type_dict = self.component_type_dict
        position_dict = self.position_dict
        for index, component_index in enumerate(design):
            position_index = index + 1
            component_type = component_type_dict[component_index]
            position_type = position_dict[position_index]
            if component_type not in position_type:
                return False
        return True
    def transfer_design(self,design):
        '''
        输入design输出reliabilitylist
        :param design:
        :return:
        '''
        plist = self.plist
        try:
            a = plist[design - 1]
        except:
            print('error')
        return plist[design-1]
    def system_reliability(self, reliability_list):
        n = len(reliability_list)
        Pattern = ord(self.pattern)
        LIST = (c_double * n)(*reliability_list)
        sys = self.sysfun(self.k, n, Pattern, LIST)
        return sys
    #@profile
    def bi_fun(self, reliability_list):
        BI = []
        k = self.k
        pattern = self.pattern
        length = len(reliability_list)
        delta = 0.001
        for i in range(0, len(reliability_list)):
            new_reliability_list = reliability_list.copy()
            new_reliability_list[i] = reliability_list[i] + delta
            bi_i = (self.system_reliability(new_reliability_list) - self.system_reliability(reliability_list)) / delta
            BI.append(bi_i)
        return np.array(BI)
    def initial_design(self,problem_type=1,funtype='largest'):
        '''
        初始化一个可行解,为了节省算力还是区分两个问题
        对于largest，选同类型最小组件
        :return:
        '''
        component_index_dict = self.component_index_dict
        typenum = self.typenum
        funindex = 0
        if funtype != 'largest':
            funindex = 1
        design = np.array([])#在空数组基础上append会导致改变数组元素类型至float
        if problem_type == 1:
            for typeindex in range(1,typenum+1):
                component_index_list = component_index_dict[typeindex]#类型为i的组件列表
                component_num = len(component_index_list)#该类型组件数量
                component_select = component_index_list[funindex]#选择组件（最大或者最小）
                design_i = [component_select] * component_num
                design = np.append(design,design_i)
            return design.astype(int)
        else:
            region_dict = self.region_dict
            positionnum = self.positionnum
            #需要控制组件数量：min(组件数量，剩余可选位置)
            for typeindex in range(1,typenum+1):
                component_index_list = component_index_dict[typeindex]#类型为i的组件列表
                component_num0 = len(component_index_list)
                # 剩余可选位置>>>该类型可分配位置和目前未分配位置的交集
                position_available = region_dict[typeindex]#可分配位置
                position_notassign = np.arange(len(design)+1,positionnum+1)#待分配位置
                position_select = set(position_available) & set(position_notassign)
                component_num1 = len(position_select)
                component_num = min(component_num0,component_num1)
                component_select = component_index_list[funindex]
                design_i = [component_select] * component_num
                design = np.append(design,design_i)
            return design.astype(int)
    #@profile
    def zk(self,problem_type=1,funtype='largest'):
        '''
        默认largest，初始化最小可靠度，从最大可靠度组件开始交换
        zk算法（初始化算法）(p1和p2共用)
        问题p1已测试正确性
        :return: 生成可行的初始解
        '''
        # 类变量
        positionnum = self.positionnum
        pnums = self.pnums
        component_type_dict = self.component_type_dict
        component_index_dict = self.component_index_dict
        # 生成初始解（适用于p2问题的）
        design = self.initial_design(problem_type,funtype)

        reliability_list = self.transfer_design(design)

        # 初始化可分配组件和位置集
        # position_available = np.arange(1,positionnum+1)
        # component_available = np.arange(1,sum(pnums)+1)
        position_available = [i for i in range(1,positionnum+1)]
        component_available = [i for i in range(1,sum(pnums)+1)]
        if funtype == 'largest':
            # 从最大可靠度开始分配
            for relia_index in range(positionnum,0,-1):
                #计算该类型中各位置BI值
                bi_list = self.bi_fun(reliability_list)
                try:
                    bi_list_available = bi_list[np.array(position_available)-1]
                except:
                    print('error')
                #找到该类型中BI值最大的位置
                position_select = position_available[np.argmax(bi_list_available)]
                #找到该位置上目前分配的组件和类型
                component_assigned = design[position_select-1]
                type_assigned = component_type_dict[component_assigned]
                #找到同类型组件中，未分配且可靠度最大的组件
                component_withsametype = component_index_dict[type_assigned]#同类型组件
                component_selectlist = set(component_available) & set(component_withsametype)#取交集
                component_select = max(component_selectlist)
                # 更新design，更新待分配组件集和位置集,position_select和component_select
                design[position_select-1] = component_select
                # position_available = np.delete(position_available,np.where(position_available==position_select))
                # component_available = np.delete(component_available, np.where(component_available == component_select))
                position_available.remove(position_select)
                component_available.remove(component_select)
            return design
        else:
            # 从最小可靠度开始分配
            for relia_index in range(positionnum,0,-1):
                #计算该类型中各位置BI值
                bi_list = self.bi_fun(reliability_list)
                bi_list_available = bi_list[position_available-1]
                #找到该类型中BI值最大的位置
                position_select = position_available[np.argmin(bi_list_available)]
                #找到该位置上目前分配的组件和类型
                component_assigned = design[position_select-1]
                type_assigned = component_type_dict[component_assigned]
                #找到同类型组件中，未分配且可靠度最大的组件
                component_withsametype = component_index_dict[type_assigned]#同类型组件
                component_selectlist = set(component_available) & set(component_withsametype)#取交集
                component_select = min(component_selectlist)
                # 更新design，更新待分配组件集和位置集,position_select和component_select
                design[position_select-1] = component_select
                position_available = np.delete(position_available,np.where(position_available==position_select))
                component_available = np.delete(component_available, np.where(component_available == component_select))
            return design
    #@profile
    def lk_p1(self,design,funtype='largest'):
        '''
        p1问题的lk算法
        largest:从较大BI值位置处开始交换
        :return:
        '''
        # 初始化和配置
        problem_type = 1
        plist = self.plist
        position_dict = self.position_dict
        component_type_dict = self.component_type_dict
        component_index_dict = self.component_index_dict
        position_type_dict = self.position_type_dict
        position_index_dict = self.position_index_dict
        is_circulation = True
        if funtype == 'largest':
            while is_circulation == True:
                # step1 计算各个位置的BI值
                reliability_list = self.transfer_design(design)
                bi_list = self.bi_fun(reliability_list)
                # step2 从最大BI值位置开始分配
                for bi_index in range(len(reliability_list) - 1, -1, -1):#位置的bi值索引
                    # 找到bi索引值index的位置（升序）
                    '''
                    提供索引选取的位置和组件分别定义为position_index and component_index
                    '''
                    position_index = np.argsort(bi_list)[bi_index]  # 该位置的编号
                    position_index_type = position_dict[position_index]
                    # 该位置上的组件编号和类型
                    component_index = design[position_index-1]
                    component_index_type = component_type_dict[component_index]
                    relia_index = plist[component_index-1]
                    # BI 值不如当前位置上的同类型组件
                    position_lessBI = np.argsort(bi_list)[0:bi_index-1]# BI值不如当前位置的集合
                    component_lessBI = design[position_lessBI-1]
                    component_withsametype = component_index_dict[component_index_type]#同类型组件
                    # 位置集上的同类型组件
                    component_selectlist = set(component_lessBI) & set(component_withsametype)
                    '''
                    如果为空集，说明同类型组件中无更适合的
                    '''
                    if len(component_selectlist) > 0:
                        component_select = max(component_selectlist)#同类型最大可靠度组件
                        component_select_relia = plist[component_select-1]
                    else:
                        component_select = 0
                        component_select_relia = 0
                    # 位置集上同类型位置（且为交叉）
                    if len(position_index_type) > 1:
                        position_index_typenum = position_type_dict[position_index]
                        position_withsametypenum = position_index_dict[position_index_typenum]
                        position_selectlist = set(position_lessBI) & set(position_withsametypenum)
                        '''
                        如果为空集
                        '''
                        if len(position_selectlist) == 0:
                            component_select1 = 0
                            component_select1_relia = 0
                        else:
                            component_selectlist1 = design[np.array(list(position_selectlist))-1]
                            component_selectlist1_relia = plist[component_selectlist1-1]
                            component_select1 = component_selectlist1[np.argsort(component_selectlist1_relia)[-1]]#最大可靠度的组件号
                            component_select1_relia = plist[component_select1-1]

                        # 判断是否有空集
                        if component_select_relia >= component_select1_relia:
                            component_select_final = component_select
                        else:
                            component_select_final = component_select1
                    else:
                        component_select_final = component_select
                    # 判断最终选定组件是否为0
                    if component_select_final == 0:
                        pass
                    else:
                        #进行交换测试
                        relia_select = plist[component_select_final-1]
                        if relia_index >= relia_select:#此时BI值顺序和可靠度顺序相同，不需要交换
                            pass
                        else:
                            design_test = copy.copy(design)
                            position_select = np.where(design == component_select_final)[0][0]
                            design_test[position_index-1] = component_select_final
                            design_test[position_select] = component_index#已经是索引不需要减一
                            sys = self.system_reliability(self.transfer_design(design))
                            sys_test = self.system_reliability(self.transfer_design(design_test))
                            improve = sys_test - sys
                            if improve > 0 :#跳出循环
                                design = copy.copy(design_test)
                                break
                    if bi_index == 0:#结束
                        return design
        else:
            while is_circulation == True:
                # step1 计算各个位置的BI值
                reliability_list = self.transfer_design(design)
                bi_list = self.bi_fun(reliability_list)
                # step2 从最小BI值位置开始分配
                for bi_index in range(0,len(reliability_list)):#位置的bi值索引
                    # 找到bi索引值index的位置（升序）
                    '''
                    提供索引选取的位置和组件分别定义为position_index and component_index
                    '''
                    position_index = np.argsort(bi_list)[bi_index]  # 该位置的编号
                    position_index_type = position_dict[position_index]
                    # 该位置上的组件编号和类型
                    component_index = design[position_index-1]
                    component_index_type = component_type_dict[component_index]
                    relia_index = plist[component_index-1]
                    # BI 值优于当前位置上的同类型组件
                    position_moreBI = np.argsort(bi_list)[bi_index+1:]# BI值不如当前位置的集合
                    component_moreBI = design[position_moreBI-1]
                    component_withsametype = component_index_dict[component_index_type]#同类型组件
                    # 位置集上的同类型组件
                    component_selectlist = set(component_moreBI) & set(component_withsametype)
                    '''
                    如果为空集，说明同类型组件中无更适合的
                    '''
                    if len(component_selectlist) > 0:
                        component_select = min(component_selectlist)#同类型最大可靠度组件
                        component_select_relia = plist[component_select-1]
                    else:
                        component_select = 0
                        component_select_relia = 2
                    # 位置集上同类型位置（且为交叉）
                    if len(position_index_type) > 1:
                        position_index_typenum = position_type_dict[position_index]
                        position_withsametypenum = position_index_dict[position_index_typenum]
                        position_selectlist = set(position_moreBI) & set(position_withsametypenum)
                        '''
                        如果为空集
                        '''
                        if len(position_selectlist) == 0:
                            component_select1 = 0
                            component_select1_relia = 2
                        else:
                            component_selectlist1 = design[np.array(list(position_selectlist))-1]
                            component_selectlist1_relia = plist[component_selectlist1-1]
                            component_select1 = component_selectlist1[np.argsort(component_selectlist1_relia)[-1]]#最大可靠度的组件号
                            component_select1_relia = plist[component_select1-1]

                        # 判断是否有空集
                        if component_select_relia <= component_select1_relia:
                            component_select_final = component_select
                        else:
                            component_select_final = component_select1
                    else:
                        component_select_final = component_select
                    # 判断最终选定组件是否为0
                    if component_select_final == 0:
                        pass
                    else:
                        #进行交换测试
                        relia_select = plist[component_select_final-1]
                        if relia_index <= relia_select:#此时BI值顺序和可靠度顺序相同，不需要交换
                            pass
                        else:
                            design_test = copy.copy(design)
                            position_select = np.where(design == component_select_final)[0][0]
                            design_test[position_index-1] = component_select_final
                            design_test[position_select] = component_index#已经是索引不需要减一
                            sys = self.system_reliability(self.transfer_design(design))
                            sys_test = self.system_reliability(self.transfer_design(design_test))
                            improve = sys_test - sys
                            if improve > 0 :#跳出循环
                                design = copy.copy(design_test)
                                break
                    if bi_index == 0:#结束
                        return design

    def lk_p2(self,design,funtype='largest'):
        '''
        问题p2的lk算法
        :param design:
        :param funtype:
        :return:
        '''
        # 初始化和配置
        problem_type = 1
        plist = self.plist
        position_dict = self.position_dict
        component_type_dict = self.component_type_dict
        component_index_dict = self.component_index_dict
        position_type_dict = self.position_type_dict
        position_index_dict = self.position_index_dict
        is_circulation = True
        if funtype == 'largest':
            while is_circulation == True:
                # step1 计算各个位置的BI值
                reliability_list = self.transfer_design(design)
                bi_list = self.bi_fun(reliability_list)
                # step2 从最大BI值位置开始分配
                for bi_index in range(len(reliability_list) - 1, -1, -1):#位置的bi值索引
                    # 找到bi索引值index的位置（升序）
                    '''
                    提供索引选取的位置和组件分别定义为position_index and component_index
                    '''
                    position_index = np.argsort(bi_list)[bi_index]  # 该位置的编号
                    position_index_type = position_dict[position_index]
                    # 该位置上的组件编号和类型
                    component_index = design[position_index-1]
                    component_index_type = component_type_dict[component_index]
                    relia_index = plist[component_index-1]
                    # BI 值不如当前位置上的同类型组件
                    position_lessBI = np.argsort(bi_list)[0:bi_index-1]# BI值不如当前位置的集合
                    component_lessBI = design[position_lessBI-1]
                    component_withsametype = component_index_dict[component_index_type]#同类型组件
                    component_notassigned = set(component_withsametype) & (set(np.arange(1,len(plist)+1)) - set(design)) #同类型未分配组件集#p2修改位置
                    # 位置集上的同类型组件
                    component_selectlist = set(component_lessBI) & set(component_withsametype)
                    component_selectlist = component_selectlist | component_notassigned #p2修改位置
                    '''
                    如果为空集，说明同类型组件中无更适合的
                    '''
                    if len(component_selectlist) > 0:
                        component_select = max(component_selectlist)#同类型最大可靠度组件
                        component_select_relia = plist[component_select-1]
                    else:
                        component_select = 0
                        component_select_relia = 0
                    # 位置集上同类型位置（且为交叉）
                    if len(position_index_type) > 1:
                        position_index_typenum = position_type_dict[position_index]
                        position_withsametypenum = position_index_dict[position_index_typenum]
                        position_selectlist = set(position_lessBI) & set(position_withsametypenum)
                        '''
                        如果为空集
                        '''
                        if len(position_selectlist) == 0:
                            component_select1 = 0
                            component_select1_relia = 0
                        else:
                            component_selectlist1 = design[np.array(list(position_selectlist))-1]
                            component_selectlist1_relia = plist[component_selectlist1-1]
                            component_select1 = component_selectlist1[np.argsort(component_selectlist1_relia)[-1]]#最大可靠度的组件号
                            component_select1_relia = plist[component_select1-1]

                        # 判断是否有空集
                        if component_select_relia >= component_select1_relia:
                            component_select_final = component_select
                        else:
                            component_select_final = component_select1
                    else:
                        component_select_final = component_select
                    # 判断最终选定组件是否为0
                    if component_select_final == 0:
                        pass
                    else:
                        #进行交换测试
                        relia_select = plist[component_select_final-1]
                        if relia_index >= relia_select:#此时BI值顺序和可靠度顺序相同，不需要交换
                            pass
                        else:
                            design_test = copy.copy(design)
                            # 判断是否为未分配组件# 本if语句为p2增加
                            if component_select_final not in design:#未分配组件
                                design_test[position_index - 1] = component_select_final
                            else:
                                position_select = np.where(design == component_select_final)[0][0]
                                design_test[position_index-1] = component_select_final
                                design_test[position_select] = component_index#已经是索引不需要减一
                            sys = self.system_reliability(self.transfer_design(design))
                            sys_test = self.system_reliability(self.transfer_design(design_test))
                            improve = sys_test - sys
                            if improve > 0 :#跳出循环
                                design = copy.copy(design_test)
                                break
                    if bi_index == 0:#结束
                        return design
        else:
            while is_circulation == True:
                # step1 计算各个位置的BI值
                reliability_list = self.transfer_design(design)
                bi_list = self.bi_fun(reliability_list)
                # step2 从最小BI值位置开始分配
                for bi_index in range(0,len(reliability_list)):#位置的bi值索引
                    # 找到bi索引值index的位置（升序）
                    '''
                    提供索引选取的位置和组件分别定义为position_index and component_index
                    '''
                    position_index = np.argsort(bi_list)[bi_index]  # 该位置的编号
                    position_index_type = position_dict[position_index]
                    # 该位置上的组件编号和类型
                    component_index = design[position_index-1]
                    component_index_type = component_type_dict[component_index]
                    relia_index = plist[component_index-1]
                    # BI 值优于当前位置上的同类型组件
                    position_moreBI = np.argsort(bi_list)[bi_index+1:]# BI值不如当前位置的集合
                    component_moreBI = design[position_moreBI-1]
                    component_withsametype = component_index_dict[component_index_type]#同类型组件
                    component_notassigned = set(component_withsametype) & (set(np.arange(1,len(plist)+1)) - set(design)) #同类型未分配组件集#p2修改位置
                    # 位置集上的同类型组件
                    component_selectlist = set(component_moreBI) & set(component_withsametype)
                    component_selectlist = component_selectlist | component_notassigned #p2修改位置
                    '''
                    如果为空集，说明同类型组件中无更适合的
                    '''
                    if len(component_selectlist) > 0:
                        component_select = min(component_selectlist)#同类型最大可靠度组件
                        component_select_relia = plist[component_select-1]
                    else:
                        component_select = 0
                        component_select_relia = 2
                    # 位置集上同类型位置（且为交叉）
                    if len(position_index_type) > 1:
                        position_index_typenum = position_type_dict[position_index]
                        position_withsametypenum = position_index_dict[position_index_typenum]
                        position_selectlist = set(position_moreBI) & set(position_withsametypenum)
                        '''
                        如果为空集
                        '''
                        if len(position_selectlist) == 0:
                            component_select1 = 0
                            component_select1_relia = 2
                        else:
                            component_selectlist1 = design[np.array(list(position_selectlist))-1]
                            component_selectlist1_relia = plist[component_selectlist1-1]
                            component_select1 = component_selectlist1[np.argsort(component_selectlist1_relia)[-1]]#最大可靠度的组件号
                            component_select1_relia = plist[component_select1-1]

                        # 判断是否有空集
                        if component_select_relia <= component_select1_relia:
                            component_select_final = component_select
                        else:
                            component_select_final = component_select1
                    else:
                        component_select_final = component_select
                    # 判断最终选定组件是否为0
                    if component_select_final == 0:
                        pass
                    else:
                        #进行交换测试
                        relia_select = plist[component_select_final-1]
                        if relia_index <= relia_select:#此时BI值顺序和可靠度顺序相同，不需要交换
                            pass
                        else:
                            design_test = copy.copy(design)
                            # 判断是否为未分配组件# 本if语句为p2增加
                            if component_select_final not in design:#未分配组件
                                design_test[position_index - 1] = component_select_final
                            else:
                                position_select = np.where(design == component_select_final)[0][0]
                                design_test[position_index-1] = component_select_final
                                design_test[position_select] = component_index#已经是索引不需要减一
                            sys = self.system_reliability(self.transfer_design(design))
                            sys_test = self.system_reliability(self.transfer_design(design_test))
                            improve = sys_test - sys
                            if improve > 0 :#跳出循环
                                design = copy.copy(design_test)
                                break
                    if bi_index == 0:#结束
                        return design
    #@profile
    def BIACO(self,problem_type = 1):
        '''
        BIACO算法
            尽可能封装好
        终止条件：
            到达最大代数或者最优解10代不改变
        :return:
        '''

        # class variable
        plist = self.plist
        typenum = self.typenum
        component_index_dict = self.component_index_dict
        '''
        step 1 初始化操作
        '''
        # basic parameter
        ant_num = 20
        city_num = len(plist)  # 步数即城市数量
        max_iteration = 100
        max_nochange_iteration = 10
        pheromone_elism_factor = 1 # 精英蚂蚁的额外权重（更新信息素）
        Q = 10  # 计算信息素时的正常数
        alpha, beta = 1, 1  # 因子
        rho = 0.8  # 信息素挥发系数
        initial_pheromone = 2
        # 初始化信息素表  初始化n个初始路径，据此更新信息素表
        Pheromones = np.zeros((city_num, city_num))
        design_dict = defaultdict(list)
        sys_list = np.zeros(ant_num)
        for index in range(1,ant_num+1):
            initial_design = self.zk(problem_type)
            initial_sys = self.system_reliability(self.transfer_design(initial_design))
            design_dict[index] = initial_design
            sys_list[index-1] = initial_sys
            weight_i = Q * initial_sys
            Pheromones_initial_delta_k = self.update_pheromones(initial_design,weight_i)
            Pheromones = Pheromones + Pheromones_initial_delta_k
        weight_elism = Q * np.max(sys_list) * pheromone_elism_factor
        design_elism = design_dict[np.argmax(sys_list)+1]
        Pheromones_initial_delta_elism = self.update_pheromones(design_elism,weight_elism)
        Pheromones = Pheromones + Pheromones_initial_delta_elism

        # 初始化启发式因子表,为距离倒数，不需要初始化，算转移概率的时候再说

        '''
        step2 初始化起始点，并根据转移概率更新路线禁忌表，对所有蚂蚁遍历一次，相当于一代
        每次只更改一种类型的组件，然后记录
        '''
        iter = 0
        best_design_final = []
        best_sys_final = 0
        nochange_iteration = 0
        while iter < max_iteration:
            Pheromones_delta = np.zeros((city_num, city_num))
            best_design = []
            best_sys = 0
            sys_list = np.zeros(ant_num)
            for ant_index in range(1, ant_num + 1):
                '''
                随机选择一种类型的组件
                '''
                typeindex = np.random.choice(np.arange(1, typenum + 1), 1)[0]
                component_thistype = component_index_dict[typeindex]
                pre_design = design_dict[ant_index]
                bi_list_static = self.bi_fun(self.transfer_design(pre_design)) # 对于上一代design的bilist
                pre_design_thistype = list(set(pre_design) & set(component_thistype))#上一代design中同类型组件列表
                pre_design_thistype_index = np.where(np.in1d(pre_design, np.array(pre_design_thistype)))[0] # 该类型组件在上一代design中的索引
                design_thistype = []#本代design中同类型组件
                start = np.random.choice(component_thistype, 1)[0]  # 设置起始点
                tabu_k = list(component_thistype)  # get tabu of ant k
                point = start
                tabu_k.remove(point)  # update tabu
                design_thistype.append(point)
                pre_design_thistype.remove(point)
                # 计算转移概率
                for position_index in range(1,len(pre_design_thistype)+1):
                    # bi 为下一个位置的bi值，此时design可按初始design来，也可以按动态design
                    bi_static = bi_list_static[position_index] # 该位置的静态bi值

                    bi = bi_static
                    trans_pro = self.transfer_probability(point, tabu_k, bi, Pheromones, alpha, beta)
                    point_next = np.random.choice(tabu_k, 1, list(trans_pro))[0]
                    point = point_next
                    tabu_k.remove(point)  # update tabu
                    design_thistype.append(point)
                # calculate the pheromone of ant k
                pre_design[pre_design_thistype_index] = np.array(design_thistype) # 还原design
                design = copy.copy(pre_design)
                '''
                lk算法进行再优化
                '''
                if problem_type == 1:
                    design = self.lk_p1(design)
                else:
                    design = self.lk_p2(design)
                sys = self.system_reliability(self.transfer_design(design))
                sys_list[ant_index-1] = sys
                design_dict[ant_index] = design
                if sys > best_sys:
                    best_design = design
                    best_sys = sys
                weights = Q * sys
                Pheromones_delta_k = self.update_pheromones(design, weights)
                Pheromones_delta = Pheromones_delta + Pheromones_delta_k
            # update pheronomes
            design_elism = design_dict[np.argmax(sys_list) + 1]
            if problem_type == 1:
                design_elism = self.lk_p1(design_elism,'less')
            else:
                design_elism = self.lk_p2(design_elism,'less')
            max_sys = self.system_reliability(self.transfer_design(design_elism))
            weight_elism = Q * max_sys * pheromone_elism_factor

            Pheromones_delta_elism = self.update_pheromones(design_elism, weight_elism)
            Pheromones = (1 - rho) * Pheromones + Pheromones_delta + Pheromones_delta_elism
            # record the result
            if best_sys > best_sys_final:
                best_design_final = best_design
                best_sys_final = best_sys
                nochange_iteration = 0
            elif max_sys > best_sys_final:
                best_design_final = design_elism
                best_sys_final = max_sys
                nochange_iteration = 0
            else:
                nochange_iteration = nochange_iteration + 1
            if nochange_iteration > max_nochange_iteration:
                break
            # clear
            iter = iter + 1
        return best_design_final, best_sys_final,iter

    def update_pheromones(self,design, weights):
        '''
        input design and weight of pheromones table,return a delta pheromones tab
        :param design:
        :param weights:
        :return:
        '''
        city_num = len(self.plist)
        Pheromones = np.zeros((city_num, city_num))
        for index in range(1, city_num):
            start = design[index - 1]
            end = design[index]
            Pheromones[start - 1][end - 1] = weights
        return Pheromones

    def transfer_probability(self,city_i, city_jlist, bi, pheromones, alpha, beta):
        '''
        input city i and available city j list，calculate transfer probability of all city j
        :param city_i:
        :param city_jlist:
        :param heu_fac:
        :param pheromones:
        :param alpha:
        :param beta:
        :return:
        '''
        transfer_probability_list = np.zeros(len(city_jlist), dtype=float)
        for index, city_j in enumerate(city_jlist):
            probability_j = self.plist[city_j-1]
            transfer_probability_pre = math.pow(pheromones[city_i - 1][city_j - 1], alpha) * math.pow(
                probability_j / bi, beta)
            transfer_probability_list[index] = transfer_probability_pre
        sum = np.sum(transfer_probability_list)
        if sum == 0:
            length = len(city_jlist)
            value = 1 / length
            transfer_probability_list = [value] * length
            transfer_probability_list = np.array(transfer_probability_list)
        else:
            transfer_probability_list = transfer_probability_list / sum
        return transfer_probability_list
    #@profile
    def enumeration(self,problem_type=1):
        if problem_type == 1:
            length = len(self.plist)
            cases = itertools.permutations(np.arange(1, length + 1), length)
        else:
            position_length = len(self.positionnum)
            component_length = len(self.plist)
            cases = itertools.permutations(np.arange(1, component_length + 1), position_length)
        design = np.array([])
        sys_list = np.array([])
        for case in cases:
            design_k = np.array(case)
            if self.is_design_true(design_k):
                if len(design) == 0:
                    design = design_k
                else:
                    design = np.vstack((design,design_k))
                sys_list = np.append(sys_list,self.system_reliability(self.transfer_design(design_k)))
        best_design,worst_design = design[np.argmax(sys_list)],design[np.argmin(sys_list)]
        best_sys,worst_sys = np.max(sys_list),np.min(sys_list)
        return (best_design,best_sys),(worst_design,worst_sys)
    def random_method(self,problem_type=1):
        '''
        输出1w个合法解和时间
        :return:
        '''
        start = time.process_time()
        # seed = self.seed
        # np.random.seed(seed)
        count = 0
        design = np.array([])
        while count < 5:
            print(count)
            if problem_type == 1:
                length = len(self.plist)
                case = np.arange(1,length+1)
                np.random.shuffle(case)
            else:
                position_length = len(self.positionnum)
                component_length = len(self.plist)
                case = np.arange(1,component_length+1)
                np.random.shuffle(case)
                case = case[0:position_length]
            design_k = case
            if self.is_design_true(design_k):
                if len(design) == 0:
                    design = design_k
                else:
                    design = np.vstack((design,design_k))
                count = count + 1
                print(count)
        end = time.process_time()
        method_time = end - start
        return design,method_time


class Case():
    def __init__(self):
        '''
        region 字典，输入位置数，输出region
        pnums 输入位置数和more less
        '''
        self.Region = {
            7 : np.array([np.array([1, 2, 3, 4]), np.array([2, 3, 4, 5, 6]), np.array([6, 7])],dtype=object),
            8 : np.array([np.array([1, 2, 3]), np.array([3, 4, 5, 6, 7]), np.array([5, 6, 7, 8])],dtype=object),
            9 : np.array([np.array([1, 2, 3, 4, 5]), np.array([3, 4, 5, 6, 7]), np.array([7, 8, 9])],dtype=object),
            10: np.array([np.array([1, 2, 3, 4]), np.array([3, 4, 5, 6, 7, 8]), np.array([7, 8, 9, 10])],dtype=object),
            12: np.array([np.array([1, 2, 3, 4, 5, 6]), np.array([3, 4, 5, 6, 7, 8, 9]), np.array([8, 9, 10, 11, 12])],dtype=object),
            15: np.array([np.array([1, 2, 3, 4, 5, 6, 7]), np.array([4, 5, 6, 7, 8, 9, 10,11,12]), np.array([10, 11, 12, 13, 14, 15])],dtype=object),
        }
        positionnum_list = [20,30,40,50]
        for positionnum in positionnum_list:
            if positionnum == 20:
                design0 = np.array([8, 11, 9])
                design0_point = [5]
            elif positionnum == 30:
                design0 = np.array([12, 12, 11])
                design0_point = [9]
            elif positionnum == 40:
                design0 = np.array([15, 23, 17])
                design0_point = [9]  # [8,7,8,8,9],15
            else:
                design0 = np.array([18, 26, 31])
                design0_point = [14]
            region_k = np.array([np.arange(1,design0[0]+1), np.arange(design0_point[0], design0[1] + design0_point[0]), np.arange(positionnum-design0[2] +1,positionnum+1)],dtype=object)
            self.Region[positionnum] = region_k
        Pnums = pd.DataFrame(columns=['less','more'],index=[7,8,9,10,12,15,20,30,40,50])
        Pnums['less'] = [
            np.array([2, 3, 2]),
            np.array([3, 3, 2]),

            np.array([3, 4, 2]),
            np.array([3, 4, 3]),
            np.array([4, 4, 4]),
            np.array([5, 5, 5]),

            np.array([7, 4, 9]),
            np.array([10, 10, 10]),
            np.array([13, 15, 12]),
            np.array([16, 17, 17]),
        ]
        Pnums['more'] = [
            np.array([3, 4, 2]),
            np.array([3, 3, 4]),

            np.array([4, 4, 3]),
            np.array([4, 5, 3]),
            np.array([6, 6, 4]),
            np.array([6, 7, 4]),

            np.array([8, 9, 8]),
            np.array([11, 11, 11]),
            np.array([15, 16, 13]),
            np.array([17, 18, 24]),
        ]

        self.Pnums = Pnums
    def getcase(self,name,type,seed):
        try:
            pattern,k,position,condition = name.split('_')
        except:
            print('yes')
        pattern = pattern.upper()
        k = int(k)
        positionnum = int(position)
        if condition == 'less':
            problem_type = 1
        else:
            problem_type = 2
        pnums = self.Pnums[condition][positionnum]
        region = self.Region[positionnum]
        np.random.seed(seed)
        p1 = np.sort(np.random.random(pnums[0]))
        p2 = np.sort(np.random.random(pnums[1]))
        p3 = np.sort(np.random.random(pnums[2]))
        p_before = np.concatenate((p1, p2, p3), axis=None)
        if type == 1:
            p = (p_before * 19 + 80) / 100
        elif type == 2:
            p = (p_before * 19 + 1) / 100
        else:
            p = (p_before * 98 + 1) / 100
        return k, pattern, p, region, positionnum, pnums,problem_type
    def get_plist(self,pnums,type):
        '''
        输入pnums，设置plist
        :param pnums:
        :param type:
        :return:
        '''
        p1 = np.sort(np.random.random(pnums[0]))
        p2 = np.sort(np.random.random(pnums[1]))
        p3 = np.sort(np.random.random(pnums[2]))
        p_before = np.concatenate((p1, p2, p3), axis=None)
        if type == 1:
            p = (p_before * 19 + 80) / 100
        elif type == 2:
            p = (p_before * 19 + 1) / 100
        else:
            p = (p_before * 98 + 1) / 100
        return p
    def plot_region(self,region,filepath):
        colorlist = ['r', 'g', 'y']
        positionnum = region[-1][-1]
        # region = np.array([np.array([1, 2, 3, 4]), np.array([2, 3, 4, 5, 6]), np.array([6, 7])])

        # 配置背景
        fig = plt.figure(figsize=(10, 2))
        ax = fig.add_subplot(111)
        ax.set_ylim(-2, 2)
        ax.set_xlim(0, positionnum + 1)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_yticks([])
        ax.set_xticks(np.arange(1, positionnum + 1))
        # ax.yaxis.set_ticks_position('left')
        ax.spines['bottom'].set_position(('data', 0))
        # ax.spines['left'].set_position(('data',0))

        # 添加矩形 待修改h和y的值
        height = [4, 3.6, 4]
        for i in range(len(region)):
            y, h = -(height[i] / 2), height[i]
            x, weight = region[i][0] - 0.5, len(region[i])
            rect = plt.Rectangle((x, y), weight, h, color=colorlist[i], alpha=0.2)
            ax.add_patch(rect)


        plt.savefig(filepath)
        plt.show()


#%%

#%%

#%%

#%%

