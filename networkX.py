# %%
import pandas as pd
import numpy as np
import re
import networkx as nx
import matplotlib.pyplot as plt
import math
import itertools

from collections import Counter
from matplotlib import font_manager, rc
from itertools import permutations

# %%
# Calculate bachelor university and major relation weights
def calculateUniversityWeights(Univ, df):
    net_list = list(set(df[Univ].to_list()))

    # Consider multiple element
    del_list = []
    for word in net_list:
        if ',' in word:
            temp = word.split(',')
            del_list.append(word)

            for sub in temp:
                net_list.append(sub)

    for word in del_list:
        net_list.remove(word)

    net_list.remove('-')
    net_list = list(set(net_list))

    from_list = []
    to_list = []
    weight_list = []

    # If two people are from same university, add 0.5 weights
    for univ in net_list:
        name = df[df[Univ].isin([univ])].nm
        name_list = list(itertools.combinations(name, 2))

        for line in name_list:
            from_list.append(line[0])
            to_list.append(line[1])
            weight_list.append(0.5)

    df_net = pd.DataFrame(list(zip(from_list, to_list, weight_list)), columns =['to', 'from', 'weight'])

    # If two people have same major, add 0.5 weights
    # Also consider whether they have multiple degrees
    for i in range(0, df_net.shape[0]):
        p_from = df_net.iloc[i,0]
        p_to = df_net.iloc[i,1]

        major_1 = df[df['nm'] == p_from].bachelor_major.values[0]
        major_2 = df[df['nm'] == p_to].bachelor_major.values[0]

        if ',' in major_1 and ',' in major_2:
            temp = major_1.split(',')
            temp2 = major_2.split(',')

            if temp[0] == temp2[0] and temp[1] == temp2[1]:
                df_net.iloc[i,2] = 2

            elif temp[0] == temp2[0]:
                df_net.iloc[i,2] = 1
                
            elif temp[1] == temp2[1]:
                df_net.iloc[i,2] = 1

        elif ',' in major_1:
            temp = major_1.split(',')
            if major_2 in temp:
                df_net.iloc[i,2] = 1

        elif ',' in major_2:
            temp = major_2.split(',')
            if major_1 in temp:
                df_net.iloc[i,2] = 1
        else:
            if major_1 == major_2:
                df_net.iloc[i,2] = 1

    return df_net

# Calculate career relation weights
def calculateCareerWeights(df):
    career_list = []
    for sent in df_1.career.to_list():
        for word in sent.split(','):
            career_list.append(word)

    career_list = list(set(career_list))

    from_list = []
    to_list = []
    weight_list = []

    # If two people have same career, add 1 weights
    for company in career_list:
        name = df[df.career.str.contains(company)].nm
        name_list = list(itertools.combinations(name, 2))

        for line in name_list:
            from_list.append(line[0])
            to_list.append(line[1])
            weight_list.append(1)

    df_net = pd.DataFrame(list(zip(from_list, to_list, weight_list)), columns =['to', 'from', 'weight'])
    
    return df_net
# %%
# Resolve Korean font error
# font_path = "C:/Windows/Fonts/NGULIM.TTF"                         # window
font_path = '/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf'     # Ubuntu
font = font_manager.FontProperties(fname=font_path).get_name()

# rc('font', family=font)
# plt.text(0.3, 0.3, '한글', size=100)

# %%
# Create dataframe
df = pd.read_csv('data/dart_data_processed7.csv', encoding='utf-8').drop(columns=['Unnamed: 0', 'main_career', 'ofcps', 'chrg_job'])
df = df.fillna('-')

corp = df.corp_name.to_list()
career = df.career.to_list()

for i in range(0, len(corp)):
    if career[i] == '-':
        career[i] = corp[i]
    else:
        career[i] = career[i] + ',' + corp[i]

df_1 = df.copy()
df_1.nm = df.nm + '_' + df.corp_name
df_1.career = career

# %%
# Calculate weights
df_bachelor = calculateUniversityWeights('bachelor', df_1.drop(columns='corp_name'))
df_master = calculateUniversityWeights('master', df_1.drop(columns='corp_name'))
df_career = calculateCareerWeights(df_1.drop(columns='corp_name'))

# %%
# Combine weights
df_network = df_bachelor.set_index(['from', 'to']).add(df_master.set_index(['from', 'to']), fill_value=0).reset_index()
df_network = df_network.set_index(['from', 'to']).add(df_career.set_index(['from', 'to']), fill_value=0).reset_index()

# Save results
# df_network.to_csv('data/networkX.csv', encoding='utf-8-sig')
# print(df_network)

# %%
df_network = df_network[df_network.weight > 1]      # Consider weights more than 1
df_network.weight = df_network.weight * 1.5         # x1.5 for edge visualization 

# Initialize networkx
g = nx.from_pandas_edgelist(df_network, 'to', 'from', edge_attr = 'weight', create_using = nx.Graph())
pos = nx.kamada_kawai_layout(g)

# Add color to nodes
carac = df_1[['corp_name', 'nm']]
carac = carac[carac['nm'].isin(list(g.nodes()))].drop_duplicates()
carac = carac.set_index('nm')
carac = carac.reindex(g.nodes())
carac['corp_name'] = pd.Categorical(carac['corp_name'])

# Add weights
edges = g.edges()
weights = [g[u][v]['weight'] for u,v in edges]

# Draw Graph
nx.draw(g, pos, node_color=carac['corp_name'].cat.codes, width = weights)
nx.draw_networkx_labels(g, pos, font_family=font, font_size=10)

fig = plt.gcf()
fig.set_size_inches(20, 15)

plt.tight_layout()
plt.show()
# %%
# Calculate betweenness / closeness / cetrality / eigenvector / pagerank
# Betweeness: 노드 간의 최단 경로에서 얼마나 빈번하게 해당 노드를 지나가는지를 평가
# Closeness: 다른 노드까지의 평균 거리를 평가
# Centrality: 한 노드에 연결된 모든 Edge의 개수로 중심성 평가
# Eigenvector: 중요한 노드와 많이 연결됬는지를 평가 (Centrality 단점 보완)
# PageRank: 한 노드의 영향력이 다른 노드에 미치는 것을 방지하여 노드의 중요도 평가

dgr = Counter(nx.degree_centrality(g)).most_common(5)
btw = Counter(nx.betweenness_centrality(g)).most_common(5)
cls = Counter(nx.closeness_centrality(g)).most_common(5)
egv = Counter(nx.eigenvector_centrality(g)).most_common(5)
pgr = Counter(nx.pagerank(g)).most_common(5)

print(f'Betweenness: {btw}\n')
print(f'Closeness: {cls}\n')
print(f'Cetrality: {dgr}\n')
print(f'Eigenvector: {egv}\n')
print(f'Pagerank: {pgr}\n')

# %%
