# 对算法的运行结果记录进行汇总，输出最终结果


## colab setting
- extra code for execute in colab
    - import module
    - modify path


```python
try:
    from google.colab import drive
    drive.mount('/content/drive')
except ImportError:
    pass

# 修改当前文件夹位置 假定notebook文件就在项目文件夹根目录
import os
def get_root_dir():
    pathname = '/mcapplus/' # the name of sync folder
    if os.path.exists('/content/drive/MyDrive'+pathname):
        return '/content/drive/MyDrive/' + pathname #在Colab里
    else:
        return './' #在本地

#调用系统命令，相当于cd，但是直接!cd是不行的
os.chdir(get_root_dir())
```

    Drive already mounted at /content/drive; to attempt to forcibly remount, call drive.mount("/content/drive", force_remount=True).
    


```python
# 当前路径
import os
path_sync = os.getcwd()
```

## small system result
- 小系统结果汇总


### component condition is less
组件不够情况


```python
import numpy as np
import pandas as pd
from codehub_mcapplus import Common,Project,Case
import math
import copy
import time
import os
from collections import defaultdict
```

首先读取各个系统的pandas,以系统名字为key保存为字典


```python
pattern = ['g','f']
nk = [[2,7],[3,7],[2,8],[3,8],[3,9],[4,9],[3,10]]
# ,[3,10],[4,10]
condition = ['less']
namelist_small = []

for n in nk:
    for p in pattern:
        for c in condition:
            namelist_small.append(p + '_' + str(n[0]) + '_' + str(n[1]) + '_' + c)
# 路径

path_small = path_sync + '//result//now//smallsystem//'
# 文件读取
df_dict = defaultdict(list)
Seednum = 50
for name in namelist_small:
    filepath = path_small + name + '_seed_'+ str(Seednum) + '.csv'
    df = pd.read_csv(filepath,index_col=0,header=None)
    df.columns = pd.MultiIndex.from_product([
        ['low','high','arbitrary'],
        ['ssr','sys','design','max_sys','best_design','min_sys','worst_design','processtime','time','enumerationprotime','enumerationtime']
    ])
    df = df.loc[:,(slice(None),['ssr','processtime','enumerationprotime'])]
    df_dict[name] = df
```


```python
# df_dict[namelist_small[0]]
```


```python
summary = pd.DataFrame(index = namelist_small,
                      columns= pd.MultiIndex.from_product([
        ['low','high','arbitrary'],
        ['mssr','time1','time2']
    ]))
# summary
```


```python
for name in namelist_small:
    df = df_dict[name].sum(axis=0)
    summary.loc[name,:] = np.array(df)
summary.loc[:,(slice(None),'mssr')] = summary.loc[:,(slice(None),'mssr')] / Seednum

summary.loc[:,(slice(None),'time1')] = summary.loc[:,(slice(None),'time1')] / Seednum
summary.loc[:,(slice(None),'time2')] = summary.loc[:,(slice(None),'time2')] / Seednum
summary
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="3" halign="left">low</th>
      <th colspan="3" halign="left">high</th>
      <th colspan="3" halign="left">arbitrary</th>
    </tr>
    <tr>
      <th></th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>g_2_7_less</th>
      <td>0.992887</td>
      <td>0.208437</td>
      <td>0.0590625</td>
      <td>0.951671</td>
      <td>0.210625</td>
      <td>0.055</td>
      <td>0.992955</td>
      <td>0.211562</td>
      <td>0.0559375</td>
    </tr>
    <tr>
      <th>f_2_7_less</th>
      <td>0.986575</td>
      <td>0.203125</td>
      <td>0.053125</td>
      <td>0.969293</td>
      <td>0.195625</td>
      <td>0.0546875</td>
      <td>0.990572</td>
      <td>0.205</td>
      <td>0.0534375</td>
    </tr>
    <tr>
      <th>g_3_7_less</th>
      <td>0.956412</td>
      <td>0.179063</td>
      <td>0.0534375</td>
      <td>0.936875</td>
      <td>0.215312</td>
      <td>0.0528125</td>
      <td>0.967322</td>
      <td>0.196875</td>
      <td>0.0540625</td>
    </tr>
    <tr>
      <th>f_3_7_less</th>
      <td>0.971316</td>
      <td>0.221562</td>
      <td>0.058125</td>
      <td>0.873093</td>
      <td>0.211562</td>
      <td>0.058125</td>
      <td>0.967133</td>
      <td>0.21875</td>
      <td>0.054375</td>
    </tr>
    <tr>
      <th>g_2_8_less</th>
      <td>0.999116</td>
      <td>0.27375</td>
      <td>0.427812</td>
      <td>0.995954</td>
      <td>0.25</td>
      <td>0.43</td>
      <td>0.994103</td>
      <td>0.2525</td>
      <td>0.41375</td>
    </tr>
    <tr>
      <th>f_2_8_less</th>
      <td>0.969481</td>
      <td>0.2625</td>
      <td>0.440312</td>
      <td>0.983581</td>
      <td>0.259375</td>
      <td>0.434063</td>
      <td>0.978234</td>
      <td>0.263125</td>
      <td>0.427187</td>
    </tr>
    <tr>
      <th>g_3_8_less</th>
      <td>0.997592</td>
      <td>0.2475</td>
      <td>0.44125</td>
      <td>0.988288</td>
      <td>0.237187</td>
      <td>0.427812</td>
      <td>0.994232</td>
      <td>0.24125</td>
      <td>0.4375</td>
    </tr>
    <tr>
      <th>f_3_8_less</th>
      <td>0.983174</td>
      <td>0.234063</td>
      <td>0.43625</td>
      <td>0.948581</td>
      <td>0.21875</td>
      <td>0.415</td>
      <td>0.956977</td>
      <td>0.230313</td>
      <td>0.407187</td>
    </tr>
    <tr>
      <th>g_3_9_less</th>
      <td>0.999394</td>
      <td>0.282813</td>
      <td>3.62438</td>
      <td>0.998168</td>
      <td>0.299375</td>
      <td>3.74375</td>
      <td>0.997689</td>
      <td>0.31875</td>
      <td>3.83719</td>
    </tr>
    <tr>
      <th>f_3_9_less</th>
      <td>0.994394</td>
      <td>0.34</td>
      <td>3.80906</td>
      <td>0.990835</td>
      <td>0.317188</td>
      <td>3.7</td>
      <td>0.985247</td>
      <td>0.313437</td>
      <td>3.59344</td>
    </tr>
    <tr>
      <th>g_4_9_less</th>
      <td>0.967181</td>
      <td>0.269688</td>
      <td>3.61531</td>
      <td>0.992013</td>
      <td>0.2925</td>
      <td>3.5975</td>
      <td>0.987516</td>
      <td>0.301563</td>
      <td>3.59219</td>
    </tr>
    <tr>
      <th>f_4_9_less</th>
      <td>0.995387</td>
      <td>0.299687</td>
      <td>3.61313</td>
      <td>0.905475</td>
      <td>0.2475</td>
      <td>3.61469</td>
      <td>0.98811</td>
      <td>0.320312</td>
      <td>3.55469</td>
    </tr>
    <tr>
      <th>g_3_10_less</th>
      <td>0.988877</td>
      <td>0.324688</td>
      <td>34.8884</td>
      <td>0.996169</td>
      <td>0.37875</td>
      <td>35.4894</td>
      <td>0.997481</td>
      <td>0.421875</td>
      <td>35.7437</td>
    </tr>
    <tr>
      <th>f_3_10_less</th>
      <td>0.990516</td>
      <td>0.400313</td>
      <td>36.9712</td>
      <td>0.919114</td>
      <td>0.35625</td>
      <td>38.0706</td>
      <td>0.981714</td>
      <td>0.433125</td>
      <td>37.9297</td>
    </tr>
  </tbody>
</table>
</div>




```python
from collections import defaultdict
code_dict = defaultdict(list)
for name in namelist_small:
    pattern,k,n,_ = name.split('_')
    num = nk.index([int(k),int(n)]) + 1
    code = pattern + str(num)
    code_dict[name] = code
# code_dict
```


```python
code_index = []
for name in summary.index: 
    code_index.append(code_dict[name])
summary.index = code_index
summary
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="3" halign="left">low</th>
      <th colspan="3" halign="left">high</th>
      <th colspan="3" halign="left">arbitrary</th>
    </tr>
    <tr>
      <th></th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>g1</th>
      <td>0.992887</td>
      <td>0.208437</td>
      <td>0.0590625</td>
      <td>0.951671</td>
      <td>0.210625</td>
      <td>0.055</td>
      <td>0.992955</td>
      <td>0.211562</td>
      <td>0.0559375</td>
    </tr>
    <tr>
      <th>f1</th>
      <td>0.986575</td>
      <td>0.203125</td>
      <td>0.053125</td>
      <td>0.969293</td>
      <td>0.195625</td>
      <td>0.0546875</td>
      <td>0.990572</td>
      <td>0.205</td>
      <td>0.0534375</td>
    </tr>
    <tr>
      <th>g2</th>
      <td>0.956412</td>
      <td>0.179063</td>
      <td>0.0534375</td>
      <td>0.936875</td>
      <td>0.215312</td>
      <td>0.0528125</td>
      <td>0.967322</td>
      <td>0.196875</td>
      <td>0.0540625</td>
    </tr>
    <tr>
      <th>f2</th>
      <td>0.971316</td>
      <td>0.221562</td>
      <td>0.058125</td>
      <td>0.873093</td>
      <td>0.211562</td>
      <td>0.058125</td>
      <td>0.967133</td>
      <td>0.21875</td>
      <td>0.054375</td>
    </tr>
    <tr>
      <th>g3</th>
      <td>0.999116</td>
      <td>0.27375</td>
      <td>0.427812</td>
      <td>0.995954</td>
      <td>0.25</td>
      <td>0.43</td>
      <td>0.994103</td>
      <td>0.2525</td>
      <td>0.41375</td>
    </tr>
    <tr>
      <th>f3</th>
      <td>0.969481</td>
      <td>0.2625</td>
      <td>0.440312</td>
      <td>0.983581</td>
      <td>0.259375</td>
      <td>0.434063</td>
      <td>0.978234</td>
      <td>0.263125</td>
      <td>0.427187</td>
    </tr>
    <tr>
      <th>g4</th>
      <td>0.997592</td>
      <td>0.2475</td>
      <td>0.44125</td>
      <td>0.988288</td>
      <td>0.237187</td>
      <td>0.427812</td>
      <td>0.994232</td>
      <td>0.24125</td>
      <td>0.4375</td>
    </tr>
    <tr>
      <th>f4</th>
      <td>0.983174</td>
      <td>0.234063</td>
      <td>0.43625</td>
      <td>0.948581</td>
      <td>0.21875</td>
      <td>0.415</td>
      <td>0.956977</td>
      <td>0.230313</td>
      <td>0.407187</td>
    </tr>
    <tr>
      <th>g5</th>
      <td>0.999394</td>
      <td>0.282813</td>
      <td>3.62438</td>
      <td>0.998168</td>
      <td>0.299375</td>
      <td>3.74375</td>
      <td>0.997689</td>
      <td>0.31875</td>
      <td>3.83719</td>
    </tr>
    <tr>
      <th>f5</th>
      <td>0.994394</td>
      <td>0.34</td>
      <td>3.80906</td>
      <td>0.990835</td>
      <td>0.317188</td>
      <td>3.7</td>
      <td>0.985247</td>
      <td>0.313437</td>
      <td>3.59344</td>
    </tr>
    <tr>
      <th>g6</th>
      <td>0.967181</td>
      <td>0.269688</td>
      <td>3.61531</td>
      <td>0.992013</td>
      <td>0.2925</td>
      <td>3.5975</td>
      <td>0.987516</td>
      <td>0.301563</td>
      <td>3.59219</td>
    </tr>
    <tr>
      <th>f6</th>
      <td>0.995387</td>
      <td>0.299687</td>
      <td>3.61313</td>
      <td>0.905475</td>
      <td>0.2475</td>
      <td>3.61469</td>
      <td>0.98811</td>
      <td>0.320312</td>
      <td>3.55469</td>
    </tr>
    <tr>
      <th>g7</th>
      <td>0.988877</td>
      <td>0.324688</td>
      <td>34.8884</td>
      <td>0.996169</td>
      <td>0.37875</td>
      <td>35.4894</td>
      <td>0.997481</td>
      <td>0.421875</td>
      <td>35.7437</td>
    </tr>
    <tr>
      <th>f7</th>
      <td>0.990516</td>
      <td>0.400313</td>
      <td>36.9712</td>
      <td>0.919114</td>
      <td>0.35625</td>
      <td>38.0706</td>
      <td>0.981714</td>
      <td>0.433125</td>
      <td>37.9297</td>
    </tr>
  </tbody>
</table>
</div>



### component condition is more
组件不完全够情况


```python
import numpy as np
import pandas as pd
from codehub_mcapplus import Common,Project,Case
import math
import copy
import time
import os
from collections import defaultdict
```


```python
import os
path_sync = os.getcwd()
```


```python
pattern = ['g','f']
nk = [[2,7],[3,7],[2,8],[3,8]]
# ,[4,9],[3,10]
# ,[3,10],[4,10]
condition = ['more']
namelist_small = []

for n in nk:
    for p in pattern:
        for c in condition:
            namelist_small.append(p + '_' + str(n[0]) + '_' + str(n[1]) + '_' + c)
# 路径

path_small = path_sync + '//result//now//smallsystem//'
# 文件读取
df_dict = defaultdict(list)
Seednum = 50
for name in namelist_small:
    filepath = path_small + name + '_seed_'+ str(Seednum) + '.csv'
    df = pd.read_csv(filepath,index_col=0,header=None)
    df.columns = pd.MultiIndex.from_product([
        ['low','high','arbitrary'],
        ['ssr','sys','design','max_sys','best_design','min_sys','worst_design','processtime','time','enumerationprotime','enumerationtime']
    ])
    df = df.loc[:,(slice(None),['ssr','processtime','enumerationprotime'])]
    df_dict[name] = df
```


```python
summary = pd.DataFrame(index = namelist_small,
                      columns= pd.MultiIndex.from_product([
        ['low','high','arbitrary'],
        ['mssr','time1','time2']
    ]))
summary
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="3" halign="left">low</th>
      <th colspan="3" halign="left">high</th>
      <th colspan="3" halign="left">arbitrary</th>
    </tr>
    <tr>
      <th></th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>g_2_7_more</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>f_2_7_more</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>g_3_7_more</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>f_3_7_more</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>g_2_8_more</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>f_2_8_more</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>g_3_8_more</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>f_3_8_more</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
for name in namelist_small:
    df = df_dict[name].sum(axis=0)
    summary.loc[name,:] = np.array(df)
summary.loc[:,(slice(None),'mssr')] = summary.loc[:,(slice(None),'mssr')] / Seednum
summary.loc[:,(slice(None),'time1')] = summary.loc[:,(slice(None),'time1')] / Seednum
summary.loc[:,(slice(None),'time2')] = summary.loc[:,(slice(None),'time2')] / Seednum
summary
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="3" halign="left">low</th>
      <th colspan="3" halign="left">high</th>
      <th colspan="3" halign="left">arbitrary</th>
    </tr>
    <tr>
      <th></th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>g_2_7_more</th>
      <td>0.964654</td>
      <td>0.319063</td>
      <td>0.48</td>
      <td>0.855438</td>
      <td>0.312812</td>
      <td>0.472813</td>
      <td>0.955223</td>
      <td>0.341562</td>
      <td>0.482812</td>
    </tr>
    <tr>
      <th>f_2_7_more</th>
      <td>0.916198</td>
      <td>0.360625</td>
      <td>0.47875</td>
      <td>0.812094</td>
      <td>0.355625</td>
      <td>0.467813</td>
      <td>0.86406</td>
      <td>0.345625</td>
      <td>0.474375</td>
    </tr>
    <tr>
      <th>g_3_7_more</th>
      <td>0.944737</td>
      <td>0.279687</td>
      <td>0.47125</td>
      <td>0.836713</td>
      <td>0.340313</td>
      <td>0.473438</td>
      <td>0.887341</td>
      <td>0.287813</td>
      <td>0.4725</td>
    </tr>
    <tr>
      <th>f_3_7_more</th>
      <td>0.949924</td>
      <td>0.290312</td>
      <td>0.471562</td>
      <td>0.871437</td>
      <td>0.275313</td>
      <td>0.469062</td>
      <td>0.928409</td>
      <td>0.28</td>
      <td>0.458437</td>
    </tr>
    <tr>
      <th>g_2_8_more</th>
      <td>0.963923</td>
      <td>0.363438</td>
      <td>4.01438</td>
      <td>0.826605</td>
      <td>0.349062</td>
      <td>4.05312</td>
      <td>0.961159</td>
      <td>0.34625</td>
      <td>4.005</td>
    </tr>
    <tr>
      <th>f_2_8_more</th>
      <td>0.890105</td>
      <td>0.342813</td>
      <td>4.01594</td>
      <td>0.759219</td>
      <td>0.349687</td>
      <td>4.05844</td>
      <td>0.857254</td>
      <td>0.356875</td>
      <td>4.0575</td>
    </tr>
    <tr>
      <th>g_3_8_more</th>
      <td>0.953013</td>
      <td>0.29875</td>
      <td>3.94062</td>
      <td>0.790431</td>
      <td>0.3175</td>
      <td>4.02125</td>
      <td>0.886915</td>
      <td>0.323437</td>
      <td>4.015</td>
    </tr>
    <tr>
      <th>f_3_8_more</th>
      <td>0.924149</td>
      <td>0.31125</td>
      <td>4.01187</td>
      <td>0.820997</td>
      <td>0.323437</td>
      <td>3.92313</td>
      <td>0.892337</td>
      <td>0.351562</td>
      <td>4.04844</td>
    </tr>
  </tbody>
</table>
</div>




```python
from collections import defaultdict
code_dict = defaultdict(list)
for name in namelist_small:
    pattern,k,n,_ = name.split('_')
    num = nk.index([int(k),int(n)]) + 1
    code = pattern + str(num)
    code_dict[name] = code
# code_dict
code_index = []
for name in summary.index: 
    code_index.append(code_dict[name])
summary.index = code_index
summary
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="3" halign="left">low</th>
      <th colspan="3" halign="left">high</th>
      <th colspan="3" halign="left">arbitrary</th>
    </tr>
    <tr>
      <th></th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
      <th>mssr</th>
      <th>time1</th>
      <th>time2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>g1</th>
      <td>0.964654</td>
      <td>0.319063</td>
      <td>0.48</td>
      <td>0.855438</td>
      <td>0.312812</td>
      <td>0.472813</td>
      <td>0.955223</td>
      <td>0.341562</td>
      <td>0.482812</td>
    </tr>
    <tr>
      <th>f1</th>
      <td>0.916198</td>
      <td>0.360625</td>
      <td>0.47875</td>
      <td>0.812094</td>
      <td>0.355625</td>
      <td>0.467813</td>
      <td>0.86406</td>
      <td>0.345625</td>
      <td>0.474375</td>
    </tr>
    <tr>
      <th>g2</th>
      <td>0.944737</td>
      <td>0.279687</td>
      <td>0.47125</td>
      <td>0.836713</td>
      <td>0.340313</td>
      <td>0.473438</td>
      <td>0.887341</td>
      <td>0.287813</td>
      <td>0.4725</td>
    </tr>
    <tr>
      <th>f2</th>
      <td>0.949924</td>
      <td>0.290312</td>
      <td>0.471562</td>
      <td>0.871437</td>
      <td>0.275313</td>
      <td>0.469062</td>
      <td>0.928409</td>
      <td>0.28</td>
      <td>0.458437</td>
    </tr>
    <tr>
      <th>g3</th>
      <td>0.963923</td>
      <td>0.363438</td>
      <td>4.01438</td>
      <td>0.826605</td>
      <td>0.349062</td>
      <td>4.05312</td>
      <td>0.961159</td>
      <td>0.34625</td>
      <td>4.005</td>
    </tr>
    <tr>
      <th>f3</th>
      <td>0.890105</td>
      <td>0.342813</td>
      <td>4.01594</td>
      <td>0.759219</td>
      <td>0.349687</td>
      <td>4.05844</td>
      <td>0.857254</td>
      <td>0.356875</td>
      <td>4.0575</td>
    </tr>
    <tr>
      <th>g4</th>
      <td>0.953013</td>
      <td>0.29875</td>
      <td>3.94062</td>
      <td>0.790431</td>
      <td>0.3175</td>
      <td>4.02125</td>
      <td>0.886915</td>
      <td>0.323437</td>
      <td>4.015</td>
    </tr>
    <tr>
      <th>f4</th>
      <td>0.924149</td>
      <td>0.31125</td>
      <td>4.01187</td>
      <td>0.820997</td>
      <td>0.323437</td>
      <td>3.92313</td>
      <td>0.892337</td>
      <td>0.351562</td>
      <td>4.04844</td>
    </tr>
  </tbody>
</table>
</div>



- 大系统结果汇总


```python
pattern = ['g','f']
nk = [[4,20],[5,20],[10,20],[12,30],[15,30],[20,30],[22,40],[25,40],[30,40],[32,50],[35,50],[40,50]]
condition = ['less']
namelist_large = []
for p in pattern:
    for n in nk:
        for c in condition:
            namelist_large.append(p + '_' + str(n[0]) + '_' + str(n[1]) + '_' + c)
print(namelist_large)
# 路径
path_large = '.\\result\\now\\largesystem\\'
# 文件读取
df_dict = defaultdict(list)
Seednum = 10
for name in namelist_large:
    filepath = path_large + name + '_seed_'+ str(Seednum) + '.csv'
    df = pd.read_csv(filepath,index_col=0,header=None)
    df.columns = pd.MultiIndex.from_product([
        ['low','high','arbitrary'],
        ['ssr','sys','design','max_sys','best_design','min_sys','worst_design','processtime','time','enumerationprotime','enumerationtime']
    ])
    df = df.loc[:,(slice(None),['ssr','processtime','enumerationprotime'])]
    df_dict[name] = df
```


```python
df_dict[namelist_large[0]]
```


```python
summary = pd.DataFrame(index = namelist_large,
                      columns= pd.MultiIndex.from_product([
        ['low','high','arbitrary'],
        ['mssr','time1','time2']
    ]))
summary
```


```python
for name in namelist_large:
    df = df_dict[name].sum(axis=0)
    summary.loc[name,:] = np.array(df)
summary.loc[:,(slice(None),'mssr')] = summary.loc[:,(slice(None),'mssr')] / Seednum
summary
```


```python

```
