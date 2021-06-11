'''
普通蚁群算法测试
    面向过程编程，之后可以考虑面向对象编程(暂未

'''
#%%
from collections import defaultdict
import numpy as np
import math
import copy
#%%
def transfer_probability(city_i,city_jlist,heu_fac,pheromones,alpha,beta):
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
    transfer_probability_list = np.zeros(len(city_jlist),dtype=float)
    for index,city_j in enumerate(city_jlist):
        transfer_probability_pre = math.pow(heu_fac[city_i-1][city_j-1],alpha) * math.pow(pheromones[city_i-1][city_j-1],beta)
        transfer_probability_list[index] = transfer_probability_pre
    sum = np.sum(transfer_probability_list)
    transfer_probability_list = transfer_probability_list / sum
    return transfer_probability_list
def distance(design,tsp):
    '''
    input design of tsp and tsp data, calculate the distance of design
    :param design:
    :param tsp:
    :return:
    '''
    Distance = 0
    for index in range(1,len(design)):
        start = design[index-1]
        end = design[index]
        Distance = Distance + tsp[start-1][end-1]
    return float(Distance)
def update_pheromones(design,weights):
    '''
    input design and weight of pheromones table,return a delta pheromones tab
    :param design:
    :param weights:
    :return:
    '''
    city_num = len(design)
    Pheromones = np.zeros((city_num, city_num))
    for index in range(1,len(design)):
        start = design[index-1]
        end = design[index]
        Pheromones[start-1][end-1] = weights
    return Pheromones
def ACO(tsp_matrix):
    '''
    自己实现蚁群算法，增加理解
    禁忌表：保证后面的遍历点不与前面相同，普通列表组成的字典即可
    :return: 
    '''

    '''
    step 1 初始化操作
    '''
    # basic parameter
    ant_num = 10
    city_num = tsp_matrix.shape[0] #步数即城市数量
    max_iteration = 100
    Q = 100 #计算信息素时的正常数
    alpha,beta = 1,1 #因子
    rho = 0.5 # 信息素挥发系数
    initial_pheromone = 2
    # 初始化禁忌表
    Tabu = defaultdict(list)
    for ant_index in range(1,ant_num+1):
        Tabu[ant_index] = [i for i in range(1,city_num+1)]
    tabu = copy.deepcopy(Tabu)
    # 初始化信息素表
    Pheromones = np.ones((city_num,city_num)) * initial_pheromone
    # 初始化启发式因子表,为距离倒数
    tsp_plus = np.ones((city_num,city_num)) * 0.001
    tsp_matrix = tsp_matrix + tsp_plus
    heuristic_factor = 1 / tsp_matrix
    '''
    step2 初始化起始点，并根据转移概率更新路线禁忌表，对所有蚂蚁遍历一次，相当于一代
    '''
    iter = 0
    best_design_final = []
    best_distance_final = 9999
    while iter < max_iteration:
        Pheromones_delta = np.zeros((city_num,city_num))
        best_design = []
        best_distance = 9999
        for ant_index in range(1,ant_num+1):
            design = []
            start = np.random.choice(np.arange(1,city_num+1),1)[0]#设置起始点
            tabu_k = tabu[ant_index] # get tabu of ant k
            point = start
            tabu_k.remove(point) # update tabu
            design.append(point)
            # 计算转移概率
            for pointnum in range(len(tabu_k)):
                trans_pro = transfer_probability(point,tabu_k,heuristic_factor,Pheromones,alpha,beta)
                point_next = np.random.choice(tabu_k,1,list(trans_pro))[0]
                point = point_next
                tabu_k.remove(point)  # update tabu
                design.append(point)
            # calculate the pheromone of ant k
            D = distance(design,tsp_matrix)
            if D < best_distance:
                best_design = design
                best_distance = D
            weights = Q / D
            Pheromones_delta_k = update_pheromones(design,weights)
            Pheromones_delta = Pheromones_delta + Pheromones_delta_k
        # update pheronomes
        Pheromones = (1 - rho) * Pheromones + Pheromones_delta
        # record the result
        if best_distance < best_distance_final:
            best_design_final = best_design
            best_distance_final = best_distance
        # clear
        tabu = copy.deepcopy(Tabu)
        iter = iter + 1
    return best_design_final,best_distance_final

#%%
tsp = [[0,2,10,8,3],[1,0,2,5,7],[9,1,0,3,6],[10,4,3,0,2],[2,7,5,1,0]]
tsp = np.array(tsp)
tsp[0][0]
#%%
design,distance_ = ACO(tsp)
print('design:{},distancse:{}'.format(design,distance_))

#%%

import numpy as np
a = [1,2,3]
b = [7,8,9,1,2,3,4,5,6]
c = []
for value in a:
    index = np.where(np.array(b)==value)[0][0]
    c.append(index)
print(c)
A,B = np.array(a),np.array(b)
np.where(np.in1d(B, A))[0]
#%%
a = np.arange(10)
index = np.array([3,5,7,6])
value = np.array([100,100,100,100])
a[index] = value
a