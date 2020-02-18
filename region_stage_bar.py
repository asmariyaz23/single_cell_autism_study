import json
import numpy as np
import matplotlib.pyplot as plt
import re

def sorted_nicely( l ):
    """ Sorts the given iterable in the way that is expected.
 
    Required arguments:
    l -- The iterable to be sorted.
 
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

barwidth = 0.2
fig, ax = plt.subplots(figsize=(10,10))

with open("mtg/fisher_prenatal.json","r") as p, open("mtg/fisher_early_childhood.json","r") as e, open("mtg/fisher_adulthood.json","r") as a:
    prenatal=json.load(p)
    early_c=json.load(e)
    adulth=json.load(a)
    clusters=sorted_nicely(prenatal.keys())
    pos=range(0,len(prenatal.keys()))
    bars1=[] 
    bars2=[]
    bars3=[]
    for c in clusters:  
        pre_overlap=prenatal[c]["x"]
        pre_shape=prenatal[c]["new_matrix_num_cells"]
        early_overlap=early_c[c]["x"]
        early_shape=early_c[c]["new_matrix_num_cells"]
        adult_overlap=adulth[c]["x"]
        adult_shape=adulth[c]["new_matrix_num_cells"]
        bars1.append((float(pre_overlap)/float(pre_shape)))
        bars2.append((float(early_overlap)/float(early_shape)))
        bars3.append((float(adult_overlap)/float(adult_shape)))
    
    print(bars1)
    print(bars2)
    print(bars3)

    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barwidth for x in r1]
    r3 = [x + barwidth for x in r2]

    plt.bar(r1, bars1, color='#7f6d5f', width=barwidth, edgecolor='white', label='PN')
    plt.bar(r2, bars2, color='#557f2d', width=barwidth, edgecolor='white', label='EC')
    plt.bar(r3, bars3, color='#2d7f5e', width=barwidth, edgecolor='white', label='AD')    
    
    plt.xlabel('Clusters', fontweight='bold')
    plt.xticks([r + barwidth for r in range(len(bars1))], clusters, rotation=45)
    plt.legend()
    plt.savefig("mtg.png")

 
