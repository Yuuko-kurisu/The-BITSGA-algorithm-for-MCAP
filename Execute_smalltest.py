'''
一个小案例的执行代码，顺便测试一下流程
'''
#%% 导入包
import numpy as np
from codehub_mcapplus import Common,Project
#%%
def small_system_p1(type,seed):
    '''
    给定系统的基本信息，如位置，组件
    :return:
    '''
    k = 3
    pattern = 'G'
    positionnum = 7
    pnums = np.array([2,3,2])
    np.random.seed(seed)
    p1 = np.random.random(pnums[0])
    p2 = np.random.random(pnums[1])
    p3 = np.random.random(pnums[2])
    p_before = np.concatenate((p1,p2,p3),axis=None)
    if type == 1:
        p = (p_before * 19 + 80) / 100
    elif type == 2:
        p = (p_before * 19 + 1) / 100
    else:
        p = (p_before * 98 +1) / 100
    region = np.array([np.array([1, 2, 3, 4]), np.array([2, 3, 4, 5, 6]), np.array([6, 7])])
    return k,pattern,p,region,positionnum,pnums
#%%
common_obj = Common()
k,pattern,plist,region,positionnum,pnums = small_system_p1(2,42)
region_dict,position_dict = common_obj.get_regiondict(region_2D=region)
component_type_dict,component_index_dict = common_obj.get_componentdict(pnums)
project_obj = Project(region_dict,position_dict,component_index_dict,component_type_dict,plist,pattern,k)
#%% 测试design
design = np.array([1,2,3,4,5,7,6])
result = project_obj.is_design_true_p1(design)
print(result)
relia = project_obj.transfer_design(design)
sys = project_obj.system_reliability(relia)



#%%
