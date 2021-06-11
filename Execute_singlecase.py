'''
通过单个算例测试算法、算例等
代码结构
待测试任务
    - 缩短biaco时间，调整算法和参数
    - 启发式算法时间调整
    - more问题求解
'''
#%% import
import numpy as np
import pandas as pd
from codehub_mcapplus import Common,Project,Case
import math
import copy
import time
import os
# import heartrate
# heartrate.trace(browser=True)
#%% select system
pattern = ['g','f']
nk = [[2,7],[2,8],[3,7],[3,8],[4,20],[5,20],[10,20],[12,30],[15,30],[20,30],[22,40],[25,40],[30,40],[32,50],[35,50],[40,50]]
condition = ['less','more']
namelist = []
for p in pattern:
    for n in nk:
        time.sleep(0.5)
        for c in condition:
            namelist.append(p + '_' + str(n[0]) + '_' + str(n[1]) + '_' + c)
print(namelist)
name = namelist[0]
name = ['f_3_7_less','g_3_7_less','f_4_9_less'][2]
#%%
ssr_list = []
Seednum = 10
seed_range = np.arange(2,Seednum+1)
df = pd.DataFrame(index=seed_range,
                  columns= pd.MultiIndex.from_product([['low','high','arbitrary'],['ssr','sys','design','max_sys','best_design','min_sys','worst_design','time1','time2']])
                  )
for type in range(1, 3 + 1):
    typename_dict = {1:'low',2:'high',3:'arbitrary'}
    for seed in seed_range:
        common_obj = Common()
        case_obj = Case()
        k,pattern,plist,region,positionnum,pnums,problem_type = case_obj.getcase(name,type,seed)
        region_dict,position_dict,position_type_dict,position_index_dict = common_obj.get_regiondict(region_2D=region)
        component_type_dict,component_index_dict = common_obj.get_componentdict(pnums)
        project_obj = Project(region_dict,position_dict,position_type_dict,position_index_dict,component_index_dict,component_type_dict,plist,pattern,k,pnums,seed)
        #%%
        start_processtime = time.process_time()
        design,sys,iter = project_obj.BIACO()
        end_processtime = time.process_time()
        biaco_processtime = end_processtime - start_processtime
        # print('sys:{}'.format(sys))
        #%% test enumeration
        start_enumerationprotime = time.process_time()
        (best_design,best_sys),(worst_design,worst_sys) = project_obj.enumeration()
        end_enumerationprotime = time.process_time()
        enumeration_protime = end_enumerationprotime - start_enumerationprotime
        # print('best design:{},best sys:{}'.format(best_design,best_sys))
        # print('worst design:{},worst sys:{}'.format(worst_design,worst_sys))
        #%%
        SSR = (sys - worst_sys) / (best_sys - worst_sys)
        # print('SSR:{}'.format(SSR))
        ssr_list.append(SSR)
        # 记录
        typename = typename_dict[type]
        record = np.array([SSR,sys,design,best_sys,best_design,worst_sys,worst_design,biaco_processtime,enumeration_protime])
        df.loc[seed,(typename,slice(None))] = record

print('name:{},SSR:{}'.format(name,np.mean(ssr_list)))
#%% process dataframe
df = df.loc[:,(slice(None),['ssr','time1','time2'])]
print(df)
df = df.mean(axis=0)
print(df)