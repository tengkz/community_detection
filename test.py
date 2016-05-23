#!/usr/bin/python
#coding:utf-8

import sys
from fast_greedy import fast_greedy

with open('data.txt','r') as f:
    data = []
    for line in f.readlines():
        v1,v2 = line.strip().split("\t")
        data.append((v1,v2))
    ret = fast_greedy(data)
    for x in ret:
        print "\t".join(x)
