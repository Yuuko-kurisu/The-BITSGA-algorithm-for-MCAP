#%%
import itertools
import numpy as np
import matplotlib.pyplot as plt

#%%
# a = itertools.permutations(np.arange(1,5+1),5)
# for i in a:
#     print(np.array(i))
#
# #%%
# a = np.array([1,2,3,4,5])
# print(a.shape)
# b = np.array([[1,2,3,4,5],[2,3,5,6,5]])
# print(b.shape)
# a.reshape(1,a.shape[0])
# print(a.shape)
# #%%
# cases = itertools.permutations(np.arange(1, 5+ 1), 5)
# cases = list(cases)
# np.random.shuffle(cases)
# for i in cases:
#     print(i)
# #%%
# plist = [0.90427457, 0.91452504, 0.93588598, 0.88049441, 0.88314157, 0.9035278, 0.92271988 ,0.96943687, 0.98309592]
# plist = np.array(plist)
# design = np.array([ 1 , 1 , 1 , 1 , 5 , 5 ,10])
# a = plist[design-1]
#%% 绘制矩形测试
colorlist = ['r','g','y']
positionnum = 7
region = np.array([np.array([1, 2, 3, 4]), np.array([2, 3, 4, 5, 6]), np.array([6, 7])])

# 配置背景
fig = plt.figure(figsize=(10,2))
ax = fig.add_subplot(111)
ax.set_ylim(-2,2)
ax.set_xlim(0,positionnum+1)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.set_yticks([])
ax.set_xticks(np.arange(1,positionnum+1))
# ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data',0))
# ax.spines['left'].set_position(('data',0))

# 添加矩形 待修改h和y的值
height = [4,3.6,4]
for i in range(len(region)):
    y,h = -(height[i] / 2),height[i]
    x,weight = region[i][0] - 0.5,len(region[i])
    rect = plt.Rectangle((x,y),weight,h,color=colorlist[i],alpha = 0.2)
    ax.add_patch(rect)

plt.show()
#%%
import numpy as np
a = np.arange(2,5)
for i in a:
    print(i)
