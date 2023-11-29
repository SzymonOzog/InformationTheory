import math
import numpy as np
import sys
EPS = 1e-10
def HY(p):
    ret=0.0
    for i in range(p.shape[0]):
        for j in range(p.shape[1]):
            ret -= p[i,j] * math.log2(np.sum(p[:,j])+EPS)
    return ret

def HX(p):
    ret=0.0
    for i in range(p.shape[0]):
        for j in range(p.shape[1]):
            ret -= p[i,j] * math.log2(np.sum(p[i,:])+EPS)
    return ret

def HXY(p):
    ret=0.0
    for i in range(p.shape[0]):
        for j in range(p.shape[1]):
            ret -= p[i,j] * math.log2(p[i,j]+EPS)
    return ret

def HX_g_Y(p):
    ret = 0.0
    for i in range(p.shape[0]):
        for j in range(p.shape[1]):
            pi_g_j = p[i,j]/np.sum(p[i,:])
            ret -= p[i,j] * math.log2(pi_g_j+EPS)
    return ret
    

def HY_g_X(p):
    ret = 0.0
    for i in range(p.shape[0]):
        for j in range(p.shape[1]):
            pj_g_i = p[i,j]/np.sum(p[:,j])
            ret -= p[i,j] * math.log2(pj_g_i+EPS)
    return ret

def I(p):
    return HY(p) - HY_g_X(p)
