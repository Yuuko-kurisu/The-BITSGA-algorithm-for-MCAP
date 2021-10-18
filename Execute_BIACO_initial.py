'''
尝试实现biaco
    结果记录
大系统实验思路
    对于每个系统，生成10000个合法解（此时不知道哪个解好哪个解不好），然后存储起来，等到确定type和seed之后才能计算知道最优和最差解

'''
#%% 导入包
import numpy as np
import pandas as pd
from codehub_mcapplus import Common,Project,Case
import math
import copy
import time
import os
# import heartrate
# heartrate.trace(browser=True)
#%% small system
pattern = ['g','f']
nk = [[2,7],[3,7],[2,8],[3,8],[3,9],[4,9]]
# ,[3,10],[4,10],[3,12],[4,12],[3,15],[4,15] 小系统不需要
condition = ['less','more']
namelist_small = []

for n in nk:
    for p in pattern:
        for c in condition:
            namelist_small.append(p + '_' + str(n[0]) + '_' + str(n[1]) + '_' + c)
print(namelist_small)
# path
path_small = '.\\result\\now\\smallsystem\\'
#%% largesystem
pattern = ['g','f']
nk = [[4,20],[5,20],[10,20],[12,30],[15,30],[20,30],[22,40],[25,40],[30,40],[32,50],[35,50],[40,50]]
condition = ['less']
namelist_large = []
for p in pattern:
    for n in nk:
        for c in condition:
            namelist_large.append(p + '_' + str(n[0]) + '_' + str(n[1]) + '_' + c)
print(namelist_large)
# path
path_large = '.\\result\\now\\largesystem\\'
#%% 记录小系统结果
def saveDataFrame(df,path,savetype):
    if savetype == 'cover':
        df.to_csv(path,header=None)
    elif os.path.exists(path) != True:#不覆盖且不存在文件
        df.to_csv(path,header=None)

def smallsystem(namelist):

    Seednum = 50
    bias = 2
    seed_range = np.arange(bias,Seednum+bias)
    for name_index in range(0,len(namelist)):
        ssr_list = []
        name = namelist[name_index]
        filepath = path_small + name + '_seed_' + str(Seednum) + '.csv'
        if not os.path.exists(filepath): # 有相同的则跳过
            df = pd.DataFrame(index=seed_range,
                              columns= pd.MultiIndex.from_product([['low','high','arbitrary'],['ssr','sys','design','max_sys','best_design','min_sys','worst_design','processtime','time','enumerationprotime','enumerationtime']])
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
                    start_time = time.time()
                    design,sys,iter = project_obj.BIACO(problem_type)
                    end_processtime = time.process_time()
                    end_time = time.time()
                    biaco_time = end_time - start_time
                    biaco_processtime = end_processtime - start_processtime
                    # print('sys:{}'.format(sys))
                    #%% test enumeration
                    start_enumerationprotime = time.process_time()
                    start_enumerationtime = time.time()
                    (best_design,best_sys),(worst_design,worst_sys) = project_obj.enumeration(problem_type)
                    end_enumerationprotime = time.process_time()
                    end_enumerationtime = time.time()
                    enumeration_time = end_enumerationtime - start_enumerationtime
                    enumeration_protime = end_enumerationprotime - start_enumerationprotime
                    # print('best design:{},best sys:{}'.format(best_design,best_sys))
                    # print('worst design:{},worst sys:{}'.format(worst_design,worst_sys))
                    #%%
                    SSR = (sys - worst_sys) / (best_sys - worst_sys)
                    # print('SSR:{}'.format(SSR))
                    ssr_list.append(SSR)
                    # 记录
                    typename = typename_dict[type]
                    record = np.array([SSR,sys,design,best_sys,best_design,worst_sys,worst_design,biaco_processtime,biaco_time,enumeration_protime,enumeration_time])
                    df.loc[seed,(typename,slice(None))] = record
            filepath = path_small + name + '_seed_'+ str(Seednum) + '.csv'
            saveDataFrame(df,filepath,savetype='nocover')
            print('name:{},SSR_list:{}'.format(name, ssr_list))
            print('name:{},SSR:{}'.format(name,np.mean(ssr_list)))
    # 汇总内容,做一个函数
def largesystem(namelist):

    Seednum = 1
    seed_range = np.arange(Seednum)
    for name_index in range(0,len(namelist)):
        ssr_list = []
        name = namelist[name_index]
        df = pd.DataFrame(index=seed_range,
                          columns= pd.MultiIndex.from_product([['low','high','arbitrary'],['ssr','sys','design','max_sys','best_design','min_sys','worst_design','processtime','time','randomprotime','randomtime']])
                          )
        common_obj = Common()
        case_obj = Case()
        k_r, pattern_r, plist_r, region_r, positionnum_r, pnums_r, problem_type = case_obj.getcase(name, 1, 0)
        region_dict_r, position_dict_r, position_type_dict_r, position_index_dict_r = common_obj.get_regiondict(
            region_2D=region_r)
        component_type_dict_r, component_index_dict_r = common_obj.get_componentdict(pnums_r)
        project_obj_r = Project(region_dict_r, position_dict_r, position_type_dict_r, position_index_dict_r, component_index_dict_r,
                              component_type_dict_r, plist_r, pattern_r, k_r, pnums_r, 0)
        # print('yes1')
        design_pop, method_time = project_obj_r.random_method(problem_type)
        # print('yes2')
        for type in range(1, 3 + 1):
            typename_dict = {1:'low',2:'high',3:'arbitrary'}
            for seed in range(len(seed_range)):
                common_obj = Common()
                case_obj = Case()
                k,pattern,plist,region,positionnum,pnums,problem_type = case_obj.getcase(name,type,seed)
                region_dict,position_dict,position_type_dict,position_index_dict = common_obj.get_regiondict(region_2D=region)
                component_type_dict,component_index_dict = common_obj.get_componentdict(pnums)
                project_obj = Project(region_dict,position_dict,position_type_dict,position_index_dict,component_index_dict,component_type_dict,plist,pattern,k,pnums,seed)
                #%%
                # print('yes')
                start_processtime = time.process_time()
                start_time = time.time()
                print('before')
                design,sys,iter = project_obj.BIACO(problem_type)
                end_processtime = time.process_time()
                end_time = time.time()
                biaco_time = end_time - start_time
                biaco_processtime = end_processtime - start_processtime
                print('biacotime:{}'.format(biaco_time))
                print('type:{},iter:{}'.format(type, iter))
                # print('sys:{}'.format(sys))
                #%% test enumeration
                start_enumerationprotime = time.process_time()
                start_enumerationtime = time.time()
                random_sys = np.array([project_obj.system_reliability(project_obj.transfer_design(i)) for i in design_pop])
                best_sys = np.max(random_sys)
                best_design = design_pop[np.argmax(random_sys)]
                worst_sys = np.min(random_sys)
                worst_design = design_pop[np.argmin(random_sys)]
                end_enumerationprotime = time.process_time()
                end_enumerationtime = time.time()
                enumeration_time = end_enumerationtime - start_enumerationtime + method_time / Seednum
                enumeration_protime = end_enumerationprotime - start_enumerationprotime + method_time / Seednum
                print('randomtime:{}'.format(enumeration_time))
                # print('best design:{},best sys:{}'.format(best_design,best_sys))
                # print('worst design:{},worst sys:{}'.format(worst_design,worst_sys))
                #%%
                SSR = (sys - worst_sys) / (best_sys - worst_sys)
                # print('SSR:{}'.format(SSR))
                print('type:{},name:{},SSR:{}'.format(type, name, SSR))
                ssr_list.append(SSR)
                # 记录
                typename = typename_dict[type]
                record = np.array([SSR,sys,design,best_sys,best_design,worst_sys,worst_design,biaco_processtime,biaco_time,enumeration_protime,enumeration_time])
                df.loc[seed,(typename,slice(None))] = record
        filepath = path_small + name + '_seed_'+ str(Seednum) + '.csv'
        saveDataFrame(df,filepath,savetype='cover')
        print('type:{},name:{},SSRlist:{}'.format(type,name,ssr_list))


#%%

# smallsystem(namelist_small)
namelist_large = ['g_3_8_more','f_3_7_less','f_3_7_more','g_3_7_less','f_4_9_less','f_4_15_less'][-1:]
largesystem(namelist_large)

