# %%
import pandas as pd
import numpy as np
import re
import networkx as nx
import matplotlib.pyplot as plt

from matplotlib import font_manager, rc
from itertools import permutations

# %%
## 폰트 문제 해결하기
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
 
plt.text(0.3, 0.3, '한글', size=100)

# %%
df = pd.read_csv('data\dart_data.csv')
df = df[['nm', 'corp_name', 'ofcps', 'main_career']]
df['temp'] = df['main_career']
df = df.drop_duplicates()

# %%
df = df[df['corp_name'] == '삼성전자']
df = df[['nm', 'main_career', 'temp']]

# %%
df['temp'] = df['temp'].str.replace('(전)', '', regex=False)
df['temp'] = df['temp'].str.replace('[ㆍ前-]', '')
df['temp'] = df['temp'].str.replace(' ', '')
df['temp'] = df['temp'].str.lower()
df['university'] = df[df['temp'].str.contains('대')]['temp'].str.split('대').str[0]

univ_list = df.university.to_list()
univ_list = list(set(univ_list))
univ_list = univ_list[1:]

#%%
df_univ = df[['nm', 'university']].drop_duplicates()

network_dict = {}

for univ in univ_list:
    network_dict[univ] = df_univ[df_univ['university'] == univ].nm.to_list()

col_A = []
col_B = []

for univ in network_dict:
    if len(network_dict[univ]) == 1:
        col_A.append(network_dict[univ][0])
        col_B.append(None)
    else:
        comb_list = list(permutations(network_dict[univ], 2))
        for comb in comb_list:
            col_A.append(comb[0])
            col_B.append(comb[1])

df_net = pd.DataFrame(list(zip(col_A, col_B)), columns =['to', 'from'])
df_net['weight'] = 1
df_net.loc[df_net.iloc[:,1] == None, 'weight'] = 0

# %%
df_result = df_net.dropna().reset_index(drop=True)

g = nx.from_pandas_edgelist(df_result, 'to', 'from', create_using = nx.DiGraph())
pos = nx.shell_layout(g)

nx.draw_shell(g)
nx.draw_networkx_labels(g, pos, font_family=font, font_size=10)
plt.show()


#%%

# # %%
# df['temp'] = df['temp'].str.replace('ㆍ', '')
# df['temp'] = df['temp'].str.replace('(주)', '', regex=False)
# df['temp'] = df['temp'].str.replace('-', '')
# df['temp'] = df['temp'].str.replace('현)', '', regex=False)
# df['temp'] = df['temp'].str.replace('現', '')
# df['temp'] = df['temp'].str.replace('美', '')
# df['temp'] = df['temp'].str.replace('.', '')
# df['temp'] = df['temp'].str.replace('\d+', '')
# df['temp'] = df['temp'].str.replace(':', '')
# df['temp'] = df['temp'].str.replace('ㅇ', '')
# df['temp'] = df['temp'].str.replace('대표', '')
# df['temp'] = df['temp'].str.replace('대학교', '대')
# df['temp'] = df['temp'].str.replace('대유에이텍', '')
# # %%
# df['university'] = df[df['temp'].str.contains('대')]['temp'].str.split('대').str[0]
# df['university'] = df['university'].str.replace(' ', '')
# df['university'] = df['university'].str.lower()
# # %%
# df = df.drop(columns=['temp'])
# df.to_csv('data/dart_data_main.csv', encoding='utf-8-sig')
# # %%
# df = pd.read_csv('data\dart_data_main.csv')
# df = df[['nm', 'university']]
# # %%
# univ_list = df.university.to_list()
# univ_list = list(set(univ_list))
# univ_list
# # %%

# %%
