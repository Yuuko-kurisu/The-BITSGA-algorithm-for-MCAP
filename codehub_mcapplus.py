'''
mcapplus项目的库文件
'''
import numpy as np
from collections import defaultdict
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
        return region_dict,position_dict
    def get_componentdict(self):
        pass
class Project():
    def __init__(self,region_dict,position_dict,component_index_dict,component_type_dict,plist):
        self.region_dict = region_dict #区域字典：输出类型返回位置列表
        self.position_dict = position_dict#位置字典，输入位置返回类型列表
        self.component_type_dict = component_type_dict#组件字典，输入组件序号，返回类型
        self.component_index_dict = component_index_dict #组件字典，输入类型，返回组件序号列表
        self.plist = plist #可靠度的一维数组，输入序号返回可靠度
    def is_design_true_p1(self,design):
        '''
        输入design判断分配方案是否可行
        :return:bool
        '''
        component_type_dict = self.component_type_dict
        position_dict = self.position_dict
        for index, component_index in enumerate(design):
            position_index = index + 1
            component_type = component_type_dict[component_index]
            position_type = position_dict[position_index]
            if component_type not in position_type:
                return False
        return True
    def zk_p1(self,p):
        '''
        问题1的zk算法（初始化算法）
        :return: 生成可行的初始解
        '''
    def zk_p2(self):
        '''
        问题2的zk算法
        :return:
        '''
#%%
