'''
整理p1，p2问题的不同规模案例，判断是否符合规整
'''
#%% 导入包
import numpy as np
from codehub_mcapplus import Common,Project,Case
import math
import copy
import os
#%% 获得namelist
pattern = ['g','f']
nk = [[2,7],[3,7],[2,8],[3,8],[3,9],[4,9],[3,10],[4,10],[3,12],[4,12],[3,15],[4,15],[4,20],[5,20],[10,20],[12,30],[15,30],[20,30],[22,40],[25,40],[30,40],[32,50],[35,50],[40,50]]
condition = ['less','more']
namelist = []
for p in pattern:
    for n in nk:
        for c in condition:
            namelist.append(p + '_' + str(n[0]) + '_' + str(n[1]) + '_' + c)
print(namelist)
#%%
'''
    为不同的系统确定一个合适的pnums值
'''
# namelist = ['g_2_7_less']
# for seed in range(1):
#     common_obj = Common()
#     case_obj = Case()
#     for name in namelist:
#         # name = 'g_2_7_more'
#         type = 1
#         k,pattern,plist,region,positionnum,pnums,problem_type = case_obj.getcase(name,type,seed)
#         region_dict,position_dict,position_type_dict,position_index_dict = common_obj.get_regiondict(region_2D=region)
#         pnums_list = common_obj.get_true_pnums(region,position_index_dict,positionnum,problem_type)
#         truepnum_list = []
#         for pnums in pnums_list:
#             pnums = np.array(pnums)
#             component_type_dict,component_index_dict = common_obj.get_componentdict(pnums)
#             plist = case_obj.get_plist(pnums,type) # 更改pnums后也需要重新定义plist
#             project_obj = Project(region_dict,position_dict,position_type_dict,position_index_dict,component_index_dict,component_type_dict,plist,pattern,k,pnums,seed)
#             design = project_obj.initial_design(problem_type)
#             result = project_obj.is_design_true(design,designtype=False)
#             truedesign = project_obj.zk(problem_type)
#             trueresult = project_obj.is_design_true(truedesign,designtype=False)
#             if result == True:
#                 # print('system:{},result:{}'.format(name,result))
#                 # print('system:{},trueresult:{}'.format(name, trueresult))
#                 truepnum_list.append(pnums)
#         truepnum_list = np.array(truepnum_list)
#         np.random.shuffle(truepnum_list)
#         # print(truepnum_list)
#         print('----------分割线-------')
#         # print(truepnum_list[0])
#         print('system:{},pnums:{}'.format(name, truepnum_list))
#         print('system:{},region:{}'.format(name, region))
#         print('system:{},pnums:{}'.format(name, truepnum_list[0]))
#         if len(truepnum_list) == 0:
#             print(name)
#%% 验证现有pnums的可行性 结论：目前都符合
for seed in range(1):
    common_obj = Common()
    case_obj = Case()
    for name in namelist:
        type = 1
        k,pattern,plist,region,positionnum,pnums,problem_type = case_obj.getcase(name,type,seed)
        region_dict,position_dict,position_type_dict,position_index_dict = common_obj.get_regiondict(region_2D=region)
        component_type_dict,component_index_dict = common_obj.get_componentdict(pnums)
        project_obj = Project(region_dict,position_dict,position_type_dict,position_index_dict,component_index_dict,component_type_dict,plist,pattern,k,pnums,seed)
        design = project_obj.initial_design(problem_type)
        result = project_obj.is_design_true(design,designtype=False)
        truedesign = project_obj.zk(problem_type)
        trueresult = project_obj.is_design_true(truedesign,designtype=False)
        print('system:{},result:{}'.format(name,result))
        print('system:{},trueresult:{}'.format(name, trueresult))

#%% 获得所有系统的结构图
# path_pic = '.\\pic\\system\\'
# for name in namelist:
#     type = 1
#     case_obj = Case()
#     k,pattern,plist,region,positionnum,pnums,problem_type = case_obj.getcase(name,type,0)
#     filepath = path_pic + name + '.jpg'
#     case_obj.plot_region(region,filepath)
