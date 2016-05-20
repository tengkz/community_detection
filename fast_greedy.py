#!/usr/bin/python
#coding:utf-8

import sys
import copy

"""Fast greedy algorithm for community detection in complex network.

Input edges information, one per line, output group id and vertice.
Refs: Finding community structure in very large networks. Newman, 2004.

Input format:
    data: edges information, a_id and b_id, one per line, sep by TAB.

Output:
    ret: list of group id and vertice.
"""

def fast_greedy(data):

    #community attribute
    com_v = []
    com_Q = []

    #vertice attribute
    ver_degree = {}
    ver_com = {}

    #edge attribute
    edge_com = {}

    m = len(data)
    m2 = m*2
    Q = 0
    QQ_max = 0
    COM_v_max = 0

    #initialize
    for v1,v2 in data:
        ver_degree[v1] = ver_degree.get(v1,0)+1
        ver_degree[v2] = ver_degree.get(v2,0)+1
        edge_com[(v1,v2)] = -1

    index = 0
    for v in ver_degree.keys():
        ver_com[v] = index
        com_v.append(set([v]))
        com_Q.append(0)
        index += 1

    while True:
        if len(data) == 0:
            break
        maxQ = -1000000
        maxIndex = -1
        for index,(v1,v2) in enumerate(data):
            com1 = ver_com[v1]
            com2 = ver_com[v2]
            new_e = set()
            tmpQ = 0
            #edges between com1 and com2 are new
            #in the combined community
            for vlast1 in com_v[com1]:
                for vlast2 in com_v[com2]:
                    if (vlast1,vlast2) in edge_com or (vlast2,vlast1) in edge_com:
                        tmpQ += m2-ver_degree[vlast1]*ver_degree[vlast2]
                    else:
                        tmpQ += -ver_degree[vlast1]*ver_degree[vlast2]
            if tmpQ > maxQ:
                maxQ = tmpQ
                maxIndex = index
        if maxQ == -1000000:
            break
        #combine com1 and com2
        v1,v2 = data[maxIndex]
        com1 = ver_com[v1]
        com2 = ver_com[v2]
        for vlast1 in com_v[com1]:
            for vlast2 in com_v[com2]:
                if (vlast1,vlast2) in edge_com:
                    edge_com[(vlast1,vlast2)] = com1
                if (vlast2,vlast1) in edge_com:
                    edge_com[(vlast2,vlast1)] = com1
        com_v[com1] = com_v[com1].union(com_v[com2])
        com_Q[com1] = com_Q[com1]+com_Q[com2]+maxQ
        com_Q[com2] = 0
        Q+=maxQ
        if Q > QQ_max:
            QQ_max = Q
            COM_v_max = copy.deepcopy(com_v)
        for tmpv in com_v[com2]:
            ver_com[tmpv] = com1
        com_v[com2].clear()
        datacopy = []
        for v1,v2 in data:
            if edge_com[(v1,v2)] == -1:
                datacopy.append((v1,v2))
        data = datacopy

    index = 0
    ret = []
    for community in COM_v_max:
        if len(community) > 0:
            index += 1
            for vertice in community:
                ret.append((str(index),vertice))
        else:
            continue
    return ret
