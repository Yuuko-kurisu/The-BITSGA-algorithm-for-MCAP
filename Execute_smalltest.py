'''
一个小案例的执行代码，顺便测试一下流程
'''
#%% 导入包
import numpy as np
from codehub_mcapplus import Common,Project,Case
import time
import matplotlib.pyplot as plt

# import heartrate
# heartrate.trace(browser=True)

#@profile
def main(seed=1):
    name_list = ['g_3_8_less','f_3_7_less','g_3_9_less','g_3_10_less','g_3_7_more']
    #%%
    name = name_list[2]
    # seed = 1
    type = 1
    
    common_obj = Common()
    case_obj = Case()
    k, pattern, plist, region, positionnum, pnums, problem_type = case_obj.getcase(name, type, seed)
    region_dict, position_dict, position_type_dict, position_index_dict = common_obj.get_regiondict(region_2D=region)
    component_type_dict, component_index_dict = common_obj.get_componentdict(pnums)
    project_obj = Project(region_dict, position_dict, position_type_dict, position_index_dict, component_index_dict,
                          component_type_dict, plist, pattern, k, pnums, seed)
    #%% 测试initial design
    # ini = project_obj.initial_design()
    #%% 测试design
    # design = np.array([1,2,3,4,5,7,6])
    # result = project_obj.is_design_true_p1(design)
    # print(result)
    # relia = project_obj.transfer_design(design)
    # sys = project_obj.system_reliability(relia)
    # print(sys)
    #%% 测试zk算法
    design = project_obj.zk()
    print(design)
    # result = project_obj.is_design_true(design)
    # print(result)
    relia = project_obj.transfer_design(design)
    sys = project_obj.system_reliability(relia)
    zk_sys = sys
    print('zk_sys:{}'.format(sys))
    #%%
    # design = project_obj.lk_p1(design)
    # print(design)
    # result = project_obj.is_design_true_p1(design)
    # print(result)
    # relia = project_obj.transfer_design(design)
    # sys = project_obj.system_reliability(relia)
    # print(sys)
    #%% 测试BITA
    design, sys, index, condition = project_obj.BITA()
    print('sys:{},design:{},condition:{}'.format(sys,design,condition))
    bita_sys = sys
    #%% 测试BIACO
    start = time.process_time()
    design,sys,iter = project_obj.BIACO(problem_type)
    biaco_sys = sys
    end = time.process_time()
    print('biacotime:{}'.format(end-start))
    print('sys:{}'.format(sys))
    print('iter:{}'.format(iter))
    #%% test enumeration
    start = time.process_time()
    (best_design,best_sys),(worst_design,worst_sys) = project_obj.enumeration(problem_type)
    end = time.process_time()
    print('time:{}'.format(end-start))
    print('best design:{},best sys:{}'.format(best_design,best_sys))
    print('worst design:{},worst sys:{}'.format(worst_design,worst_sys))
    #%%
    SSR = (sys - worst_sys) / (best_sys - worst_sys)
    print('SSR:{}'.format(SSR))
    print(name)
    #%% 测试random算法
    # design_pop, method_time = project_obj.random_method()
    return zk_sys,bita_sys,biaco_sys,best_sys
zk_sys_list = []
bita_sys_list = []
biaco_sys_list = []
best_sys_list = []
for seed in range(1,10+1):
    zk_sys, bita_sys, biaco_sys, best_sys = main(seed)
    zk_sys_list.append(zk_sys)
    bita_sys_list.append(bita_sys)
    biaco_sys_list.append(biaco_sys)
    best_sys_list.append(best_sys)
fig = plt.figure(figsize=(6,4))
plt.plot(zk_sys_list)
plt.plot(bita_sys_list)
# plt.plot(biaco_sys_list)
plt.plot(best_sys_list)
plt.legend(['zk','bita','best'])
plt.show()
