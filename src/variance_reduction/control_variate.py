import matplotlib.pyplot as plt

from variance_reduction.pricing import BS, Brown, GBM, k, mi, np, r, s0, sigma

import numpy as np

from statistics import variance, covariance, correlation

from math import exp

import pandas as pd

import seaborn

def control_variate(R):
    Xi = np.random.normal(0,1,R)
    GBMs = np.array([GBM(Brown(1)) for _ in range(R)])
    Yi = []
    for vector in GBMs:
        A = np.average(vector)
        Yi.append(np.maximum(A - k, np.zeros_like(A)))
    EXi=0
    Yi=np.array(Yi)
    b=-covariance(Yi,Xi)/np.var(Xi,ddof=1)
    Y_CV=np.average(Yi+b*(Xi-EXi))
    VarY=np.var(Yi,ddof=1)
    VarY_CV=(VarY+2*b*covariance(Yi,Xi))/R
    return exp(-r) * Y_CV, VarY_CV

def antithetic_estimation(R):
    n=int(R/2)
    mi=r-sigma**2/2

    Z=np.random.normal(size=n)

    S = np.array([s0*exp(mi  + sigma*Z[i]) for i in range(n)])
    S2 = np.array([s0*exp(mi  - sigma*Z[i]) for i in range(n)])
    X1 = np.maximum(S - k, np.zeros_like(S))
    X2 = np.maximum(S2 - k, np.zeros_like(S2))
    CorrX1X2=np.corrcoef(X1,X2)[0,1]

    Y_ant=np.average((X1+X2)/2)
    VarY=(np.var(X1,ddof=1))/n
    VarY_ant=(VarY*(1+CorrX1X2))
    return exp(-r) * Y_ant, VarY_ant

def seaborn_plots(df,val):
    lplt=seaborn.relplot(data=df, x='R', y=val, hue='method',aspect=2,kind="line")
    lplt.ax.axhline(y=BS(),color="red")
    plt.show()

    splt=seaborn.relplot(data=df, x='R', y=val, hue='method',aspect=2,kind="scatter")
    splt.ax.axhline(y=BS(),color="red")
    plt.show()

    bplt=seaborn.barplot(data=df, x='R', y=val, hue='method')
    bplt.axhline(y=BS(),color="red")
    plt.show()

"""
colors=['green','blue']
fig, ax = plt.subplots(figsize=(8,6))
ax.set(xlim=(0, max(R_vec)),
       ylim=(10, 15))
for label, df in df.groupby('method'):
    df.plot( ax=ax, label=label,y="MEAN",x="R",color=colors[])
plt.legend()
plt.show()
"""

"""
colors=['green','blue']
fig, ax = plt.subplots(figsize=(8,6))
ax.set(xlim=(0, max(R_vec)), xticks=R_vec,
       ylim=(0, 15))
for label, df in df.groupby('method'):
    i=0
    df.plot(kind="bar", ax=ax, label=label,y="MEAN",x='R',color=colors[i])
    i=1
plt.legend()
plt.show()"""

def main():
    global ANT, CV, R, R_index, R_vec, df, i, method_labels
    R_vec=[100,1000,10000,100000]

    ANT=[antithetic_estimation(R) for R in R_vec]

    CV=[control_variate(R) for R in R_vec]

    R_index=[(R_vec[i],R_vec[i]) for i in range(len(R_vec))]

    method_labels=np.repeat(["antithetic"]+["control variate"],len(R_vec),axis=0)

    df = pd.DataFrame(np.array(ANT+CV), columns=(["MEAN"]+["VARIANCE"]))

    df.insert(2, "method",method_labels, True)

    df.insert(2, "R",R_vec*2, True)

    seaborn.set(style='darkgrid')

    seaborn_plots(df,'MEAN')

    seaborn_plots(df,'VARIANCE')


if __name__ == "__main__":
    main()
