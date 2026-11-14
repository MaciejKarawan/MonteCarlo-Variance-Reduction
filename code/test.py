import numpy as np
from scipy.stats import norm
from math import log, e
from STRATA import strata
from random import seed

r = 0.05
sigma = 0.25
mi = r - (sigma**2)/2
s0 = 100
k = 100


def Brown(n): # Vector of Brown Motion from 0 to 1 with 1/n step
    NormalRV = np.random.standard_normal(n)
    Brown = np.cumsum(NormalRV * np.sqrt(1/n))

    return Brown

def BS(): #Black - Scholes
    d1 = (1/sigma) * (log(s0/k) + r + (sigma**2)/2)
    d2 = d1 - sigma
    result = s0 * norm.cdf(d1) - k * e**(-r) * norm.cdf(d2)

    return result


def GBM(Brown): # Geometric Brown Motion
    n = len(Brown)
    moments = np.array([i/n for i in range(1, n+1)])
    gbm = s0 * np.exp(mi * moments + sigma * Brown)

    return gbm



def CMC_euro(R): # Crude Monte Carlo Estimator - European Option
    GBMs = np.array([GBM(Brown(1)) for _ in range(R)])
    Y = float((1/R) * e**(-r) *  sum(np.maximum(GBMs - k, np.zeros_like(GBMs))))
    var = np.var(e**(-r) * np.maximum(GBMs - k, np.zeros_like(GBMs))) / R

    return [Y, var]


def CMC_asia(R, n):
    GBMs = np.array([GBM(Brown(n)) for _ in range(R)])
    Obs = []

    for vector in GBMs:
        A = np.average(vector)
        Obs.append(e**(-r) * np.maximum(A - k, np.zeros_like(A)))

    Y = sum(Obs) / R
    var = np.var(Obs) / R

    return [Y, var]


def estimator(bvector):
    n = len(bvector)
    return e**(-r) * 1/n * sum(np.maximum(bvector - k, np.zeros_like(bvector)))



def optimal_allocation(Rpilot, R, m, n=1):
    stratas = strata(np.array([int(np.ceil(Rpilot / m))] * m), n)
    stds = []

    if n == 1:
        for strat in stratas:
            gbms = np.array([GBM(N) for N in strat])
            transformed = e**(-r) * np.maximum(gbms - k, np.zeros_like(gbms))
            stds.append(np.std(transformed))

    elif n > 1:
        for strat in stratas:
            gbms = np.array([GBM(vector) for vector in strat])
            A = np.array([np.mean(gvector) for gvector in gbms])
            transformed = e**(-r) * np.maximum(A - k, np.zeros_like(A))
            stds.append(np.std(transformed))

    stds = np.array(stds, dtype=np.float64)
    Rj = R * stds / np.sum(stds)

    return np.ceil(Rj).astype(int)


def strat_euro(R, m, allocation=np.array([])): # allocation: Not None <=> optimal ; None <=> proportional

    if not allocation.any():
        NrForEachStrata = np.array([int(np.ceil(R/m))] * m)

    elif len(allocation) == m:
        NrForEachStrata = allocation

    else:
        raise ValueError('Number of stratas is not equal length of allocation list!')

    Y = []
    vars = []
    stratas = strata(NrForEachStrata, 1)

    for strat in stratas:
        if strat.tolist() != []:
            gbms = np.array([GBM(N) for N in strat if N != 0])
            Y.append(estimator(gbms))
            vars.append(np.var(e**(-r) * np.maximum(gbms - k, np.zeros_like(gbms))))
        else:
            vars.append(0)

    vars = np.array(vars)

    if not allocation.any():
        var = np.sum(np.array(vars) / m) / R

    elif len(allocation) == m:
        mask = (vars != 0) & (allocation != 0)
        var = np.sum(np.array(vars[mask]) / allocation[mask]) / m**2

    return [float((1/m) * sum(Y)), var]


def strat_asia(R, m, n, allocation=np.array([])): # m = number of stratas, n = dimension of a brown vector

    if not allocation.any():
        NrForEachStrata = np.array([int(np.floor(R / m))] * m)

    elif len(allocation) == m:
        NrForEachStrata = allocation

    else:
        raise ValueError('Number of stratas is not equal length of allocation list!')

    Y = []
    vars = []
    stratas = strata(NrForEachStrata, n)

    for strat in stratas:
        gbms = np.array([GBM(vector) for vector in strat])
        A = np.array([np.mean(gvector) for gvector in gbms])
        Y.append(estimator(A))

        vars.append(np.var(e**(-r) * np.maximum(A - k, np.zeros_like(A))))

    if not allocation.any():
        var = np.sum(np.array(vars) / m) / R

    elif len(allocation) == m:
        var = np.sum(np.array(vars) / (m**2 * allocation)) / R


    return [(1/m) * sum(Y), var]








