import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np
import re
import math
import matplotlib as mpl

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
#mpl.rcParams['axes.linewidth'] = 0.1

ce_matrix=sys.argv[1]
title=sys.argv[2]

def sorted_nicely( l ):
    """ Sorts the given iterable in the way that is expected.

    Required arguments:
    l -- The iterable to be sorted.

    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)


d={}
ce=pd.read_csv(ce_matrix)
clusters=sorted_nicely(ce['pathwayname'])
for index,row in ce.iterrows():
    d[row['pathwayname']]={'pval':row['p_val'],
                           'Odds_ratio':row['Odds_ratio'],
                           'Lower_CI':row['Lower_CI'],
                           'Upper_CI':row['Upper_CI']}


y=ce['p_val']
x=ce['Odds_ratio']

#fig, ax = plt.subplots()
plt.figure(figsize=(15,15))
ax = plt.axes() 
ax.xaxis.set_tick_params(length=10,pad=10)
ax.yaxis.set_tick_params(length=10,pad=10)
#ACC and VISP color list
color_d=["salmon","chocolate","darkgoldenrod",
         "gold","yellow","chartreuse",
         "mediumseagreen","springgreen","lightseagreen",
         "turquoise","deepskyblue","dodgerblue",
         "mediumpurple","mediumorchid","orchid",
         "hotpink","deeppink"]

#MTG color list
'''
color_d=["salmon","chocolate","darkgoldenrod",
         "gold","yellow","chartreuse",
         "mediumseagreen","springgreen","lightseagreen",
         "turquoise","deepskyblue","dodgerblue",
         "cornflowerblue","mediumpurple","mediumorchid", 
         "orchid","hotpink","deeppink"] 
'''
for i,c in enumerate(clusters):
    a=d[c]['Odds_ratio']-d[c]['Lower_CI']
    b=d[c]['Upper_CI']-d[c]['Odds_ratio']
    num=[s for s in list(c) if s.isdigit()]
    clus="C"+"".join(num)
    ax.errorbar(d[c]['Odds_ratio'], -(math.log10(d[c]['pval'])), xerr=np.array([[a,b]]).T, 
        fmt='ko',ecolor=color_d[i],label=clus,marker='o',mfc=color_d[i],markersize=5,elinewidth=1)
    ax.text(d[c]['Upper_CI']+0.001,-(math.log10(d[c]['pval'])),clus,fontsize=25)
    

#ax.legend(loc='upper left', numpoints=1)
ax.set_title(title,pad=30,fontweight='bold',fontsize=60)
#ax.set_xlim(right=1.46) 
ax.set_xlabel('Odds ratio',labelpad=30,fontsize=50)
ax.set_ylabel('-log10(P)'.translate(SUB),labelpad=30,fontsize=50)
#ax.set_yscale('log')

'''
# get handles
handles, labels = ax.get_legend_handles_labels()
# remove the errorbars
handles = [h[0] for h in handles]
# use them in the legend
ax.legend(handles, labels,numpoints=1,
          bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=20)
'''

plt.xticks(fontsize=40,rotation=90)
plt.yticks(fontsize=40)
plt.tight_layout()
plt.savefig("_".join(title.split(" "))+".svg")
plt.show()


