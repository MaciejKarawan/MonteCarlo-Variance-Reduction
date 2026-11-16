import numpy as np
from scipy.stats import chi2


def strata(R_values, dim_points): # R_values = lista liczb punktów do wygenerowania dla każdej straty
    generated_points = []
    num_points = len(R_values)

    for i, k in enumerate(R_values):
        X = np.random.normal(size=(k, dim_points))
        c = np.linalg.norm(X, axis=1)
        c = np.reshape(c, (k, 1))
        u = np.random.uniform(size=k)
        r2 = chi2.ppf((i + u) / num_points, dim_points)
        r2 = np.reshape(r2, (k, 1))
        Z = np.sqrt(r2) * X / c
        generated_points.append(Z)


    #transform to brown motion
    if dim_points > 1:
        A = np.tril(np.ones((dim_points, dim_points)) / np.sqrt(dim_points))
        generated_points = np.array([np.matmul(A, vector) for strata in generated_points for vector in strata])
        generated_points = np.array_split(generated_points, len(R_values))


    return generated_points



