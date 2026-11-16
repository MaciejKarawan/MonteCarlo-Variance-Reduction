import matplotlib.pyplot as plt

from variance_reduction.pricing import BS, Brown, CMC_euro, GBM, k, mi, np, optimal_allocation, r, s0, sigma, strat_euro

import numpy as np

from statistics import variance, covariance, correlation

from math import exp

import pandas as pd

import seaborn

from scipy.stats import binom

def control_variate(R):
    Xi = np.random.normal(0,1,R)
    GBMs = np.array([GBM(Brown(1)) for _ in range(R)])
    Yi = []
    for vector in GBMs:
        A = np.average(vector)
        Yi.append(exp(-r)*np.maximum(A - k, np.zeros_like(A)))
    EXi=0
    Yi=np.array(Yi)
    b=-covariance(Yi,Xi)/np.var(Xi,ddof=1)
    Y_CV=np.average(Yi+b*(Xi-EXi))
    VarY=np.var(Yi,ddof=1)
    VarY_CV=(VarY+2*b*covariance(Yi,Xi))/R
    return  Y_CV, VarY_CV

def antithetic(R):
    n=int(R/2)
    mi=r-sigma**2/2

    Z=np.random.normal(size=n)

    S = np.array([s0*exp(mi  + sigma*Z[i]) for i in range(n)])
    S2 = np.array([s0*exp(mi  - sigma*Z[i]) for i in range(n)])
    X1 = exp(-r)*np.maximum(S - k, np.zeros_like(S))
    X2 = exp(-r)*np.maximum(S2 - k, np.zeros_like(S2))
    CorrX1X2=correlation(X1,X2)

    Y_ant=np.average((X1+X2)/2)
    VarY=(np.var(X1,ddof=1))/n
    VarY_ant=(VarY*(1+CorrX1X2))
    return Y_ant, VarY_ant

def seaborn_plots(df,val):
    fig, ax = plt.subplots()
    bplt=seaborn.barplot(data=df, x='R', y=val, hue='method')
    bplt.axhline(y=BS(),color="black",linestyle="dashed",label="Prawdziwa cena opcji europejskiej")
    fig.suptitle('Porównanie estymatorów w zależności od R dla różnych metod estymacji')
    ax.set_title('cena opcji europejskiej wyliczona  z formuły Blacka-Scholesa', y=1.02, fontsize=10)
    ax.text(0.85, 0.80, f'Prawdziwa cena opcji europejskiej',
            transform=plt.gca().transAxes, fontsize=6,
            verticalalignment='top',bbox=dict( facecolor='white', alpha=0.5))
    plt.tight_layout()
    plt.show()

"""
seaborn_plots(df.query('R==10000'),'MEAN')

fig, ax = plt.subplots()
bplt=seaborn.barplot(data=df.query('R==10000'), x='R', y='VARIANCE', hue='method')
fig.suptitle('Porównanie wariancji estymatorów dla różnych metod estymacji')
bplt.axhline(y=float(VAR_CMC), color="black",linestyle="dashed")
ax.text(0.1, 0.98, "Wariancja estymatora CMC",
        transform=plt.gca().transAxes, fontsize=6,
        verticalalignment='top', bbox=dict( facecolor='white', alpha=0.5))
plt.tight_layout()
plt.show()"""

"""
colors=['green','blue']
fig, ax = plt.subplots(figsize=(8,6))
ax.set(xlim=(0, max(R_vec)),
       ylim=(10, 15))
for label, df in df.groupby('method'):
    df.plot( ax=ax, label=label,y="MEAN",x="R",color=colors[])
plt.legend()
plt.show()

colors=['green','blue']
fig, ax = plt.subplots(figsize=(8,6))
ax.set(xlim=(0, max(R_vec)), xticks=R_vec,
       ylim=(0, 15))
for label, df in df.groupby('method'):
    i=0
    df.plot(kind="bar", ax=ax, label=label,y="MEAN",x='R',color=colors[i])
    i=1
plt.legend()
plt.show()
"""

def confidence_intervals_plot(method,R,n,caption):


    estymatory = np.array([method(R) for _ in range(n)])
    sample = np.array([[estymatory[i][0] for i in range(n)], [estymatory[i][1] for i in range(n)]])
    percent_in_interval = np.mean(np.abs(sample[0] - BS()) < np.sqrt(sample[1])*(1.96))
    true_values = np.zeros_like(sample[0]) + BS()
    in_acceptance = (true_values >= sample[0] -  np.sqrt(sample[1])*1.96) & (true_values <= sample[0] +  np.sqrt(sample[1])*1.96)


    fig, ax = plt.subplots(figsize=(10,6))
    fig.suptitle('Procent przedziałów ufności zawierających prawdziwą cenę opcji', x=0.48)
    ax.fill_between(range(len(sample[0])), sample[0] -  np.sqrt(sample[1])*1.96, sample[0] +  np.sqrt(sample[1])*1.96, color='limegreen',
                    alpha=0.3, ls=(0, (1, 5)), edgecolor='darkgreen', step='mid')
    ax.scatter(range(len(sample[0])), true_values, color='darkgreen', marker='o', s=5)
    ax.scatter(np.where(~in_acceptance)[0], true_values[~in_acceptance], color='red', marker='x', s=50)
    ax.set_title('wyliczoną z formuły Blacka-Scholesa', y=1.05, fontsize=10)


    ax.set_yticks([min(sample[0] -  np.sqrt(sample[1])*1.96), BS(), max(sample[0] +  np.sqrt(sample[1])*1.96)])
    ax.set_xlabel('Liczba przedziałów ufności')
    ax.set_ylabel('Wartości')
    ax.legend(['Region akceptacji', 'Prawdziwa cena', 'Wartości spoza przedziału'])
    ax.text(0.83, 0.10, f'Procent wartości w przedziale: {round(percent_in_interval*100, 2)}%',
            transform=plt.gca().transAxes, fontsize=9,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
    ax.text(0.05,0.90, "Metoda "+caption,
           transform=plt.gca().transAxes, fontsize=14,
           verticalalignment='top',color="red",bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
    plt.tight_layout()
    plt.show()

"""confidence_intervals_plot(antithetic,10000,100,"zmiennych antytetycznych")
confidence_intervals_plot(control_variate,10000,100,'zmiennych kontrolnych')
confidence_intervals_plot(strat_euro,10000,100,'warstwowa[10] z proporcjonalną alokacją')
confidence_intervals_plot(CMC_euro,10000,100,'Crude Monte Carlo')
"""


def main():
    global ANT, CMC, CV, R, R_index, R_vec, STRATA_O, STRATA_P, VAR_CMC, df, i, m, method_labels, table
    np.random.seed(666)

    R_vec=[100,1000,10000,100000]

    ANT=[antithetic(R) for R in R_vec]

    CV=[control_variate(R) for R in R_vec]

    CMC=[CMC_euro(R) for R in R_vec]

    m=10

    STRATA_P=[strat_euro(R,m=int(min(m,R*0.1))) for R in R_vec]

    STRATA_O=[strat_euro(R,m=int(min(m,R*0.1)),allocation=optimal_allocation(int(R*0.5),R,m=int(min(m,R*0.1)),n=1)) for R in R_vec]

    R_index=[(R_vec[i],R_vec[i]) for i in range(len(R_vec))]

    method_labels=np.repeat(["antithetic"]+["control variate"]+["CMC"]+["stratified proportional["+str(m)+"]"]+["stratified optimal ["+str(m)+"]"],len(R_vec),axis=0)

    df = pd.DataFrame(np.array(ANT+CV+CMC+STRATA_P+STRATA_O), columns=(["MEAN"]+["VARIANCE"]))

    df.insert(2, "method",method_labels, True)

    df.insert(2, "R",R_vec*len(np.unique(method_labels)), True)

    df.insert(2, "confidence interval length",1.96*np.sqrt(df.VARIANCE)/np.sqrt(df.R), True)

    table=df.query('R==10000')

    VAR_CMC=table.query('method=="CMC"').VARIANCE

    print(table.to_latex())

    print(table)

    seaborn.set(style='darkgrid')


if __name__ == "__main__":
    main()
