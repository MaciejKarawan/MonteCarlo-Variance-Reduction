import math
import random
import argparse
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import norm
from collections import defaultdict
from scipy.stats import chi2


def antithetic_estimation(R,S_0,sigma,r,K):
    n=int(R/2)
    mi=r-sigma**2/2

    Z=np.random.normal(size=n)

    S = np.array([S_0*math.exp(mi  + sigma*Z[i]) for i in range(n)])
    S2 = np.array([S_0*math.exp(mi  - sigma*Z[i]) for i in range(n)])
    X1 = np.maximum(S - K, np.zeros_like(S))
    X2 = np.maximum(S2 - K, np.zeros_like(S2))
    CorrX1X2=np.corrcoef(X1,X2)[0,1]

    EY=np.average((X1+X2)/2)
    VarY=(np.var(X1,ddof=1))/n
    VarI=(VarY*(1+CorrX1X2))
    return [math.exp(-r) * EY,VarI,VarY]

if __name__ == "__main__":
    print(antithetic_estimation(1000,100,0.25,0.05,100))



