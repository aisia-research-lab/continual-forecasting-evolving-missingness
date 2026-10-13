"""Seed-level paired tests; no inference over overlapping origins."""
import itertools
import numpy as np

def sign_flip_pvalue(diffs):
    x=np.asarray(diffs,dtype=float)
    if x.ndim!=1 or x.size==0 or not np.isfinite(x).all():
        raise ValueError("Require a nonempty finite paired-difference vector")
    if x.size>18: raise ValueError("Exact enumeration limited to 18 seeds")
    obs=abs(x.mean()); eps=1e-12
    return sum(abs(np.dot(signs,x)/len(x)) >= obs-eps
               for signs in itertools.product([-1.,1.],repeat=len(x)))/2**len(x)

def holm(pvalues):
    p=np.asarray(pvalues,dtype=float)
    if np.any((p<0)|(p>1)):raise ValueError('pvalues must be in [0,1]')
    order=np.argsort(p); result=np.empty(len(p)); prev=0.
    for j,i in enumerate(order):
        prev=max(prev,min(1.,(len(p)-j)*p[i]));result[i]=prev
    return result
