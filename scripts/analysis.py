import numpy as np

import matplotlib.pyplot as plt

from variance_reduction.pricing import BS, CMC_asia, CMC_euro, np, optimal_allocation, strat_euro

'''
            Porównanie wariancji (przedziałów ufności) dla CRUDE MONTE CARLO w zalezności od R
            + extra można w zależności od n dla azjatyckich (?)
'''

'''
R = np.array([i for i in range(100, 8001, 50)])
estymatory = np.array([CMC_euro(i) for i in R])
smean = np.array([estymatory[i][0] for i in range(len(R))])
svar = np.array([estymatory[i][1] for i in range(len(R))])
dif = np.array(np.abs(smean - black_scholes))

fig, ax = plt.subplots(2, 1, figsize=(10,6), sharex=True)
fig.suptitle('Estymator CMC dla ceny opcji europejskiej', x=0.51)

ax[0].set_title('Wariancja', fontsize=10)
ax[0].plot(R, svar, color='deepskyblue', marker='.')
ax[0].plot(R, np.array([500/(i) for i in R]), color='red', ls=(0, (5, 10)), alpha=0.7)
ax[0].set_yticks([1, 2, 3, 4, 5, 6])
ax[0].set_ylabel('Wariancja')
ax[0].grid(axis='y', color='midnightblue', alpha=0.1, in_layout=True)
ax[0].legend(['Wariancja', r'Oszacowanie $O(\frac{1}{n})$'])

ax[1].set_title('Błąd bezwzględny w stosunku do formuły Blacka-Scholesa')
ax[1].plot(R, dif, color='crimson', marker='.')
ax[1].grid(axis='y', color='midnightblue', alpha=0.1, in_layout=True)
ax[1].set_xticks([100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000])
ax[1].set_xlabel('Liczba replikacji')

plt.tight_layout()
plt.show()
'''

'''
R = np.array([i for i in range(100, 3001, 100)])

estymatory2 = np.array([CMC_asia(i, 2) for i in R])
estymatory5 = np.array([CMC_asia(i, 5) for i in R])
estymatory10 = np.array([CMC_asia(i, 10) for i in R])
sample2 = np.array([estymatory2[i][1] for i in range(len(R))])
sample5 = np.array([estymatory5[i][1] for i in range(len(R))])
sample10 = np.array([estymatory10[i][1] for i in range(len(R))])

fig, ax = plt.subplots(figsize=(10,6))
fig.suptitle('Wartość wariancji dla estymatora Crude Monte Carlo', x=0.51)
ax.set_title('Opcje azjatyckie', fontsize=10)

ax.plot(R, sample2, color='deepskyblue', marker='.')
ax.plot(R, sample5, color='lime', marker='.')
ax.plot(R, sample10, color='magenta', marker='.')
ax.plot(R, np.array([500/(i) for i in R]), color='red', ls=(0, (5, 10)), alpha=0.7)

ax.set_xticks([100, 500, 1000, 2000, 3000])
ax.set_yticks([1, 2, 3, 4, 5, 6])
ax.set_xlabel('Liczba replikacji')
ax.set_ylabel('Wariancja')
ax.grid(axis='y', color='midnightblue', alpha=0.1, in_layout=True)
ax.legend([r'Wariancja dla dla $n = 2$', r'Wariancja dla dla $n = 5$', r'Wariancja dla dla $n = 10$', r'Oszacowanie $O(\frac{1}{n})$'])

plt.tight_layout()
plt.show()
'''

'''
            Przedziały ufności, CMC Euro i Black Scholes
'''

'''
n = 100
estymatory = np.array([CMC_euro(R) for _ in range(n)])
sample = np.array([[estymatory[i][0] for i in range(n)], [estymatory[i][1] for i in range(n)]])
percent_in_interval = np.mean(np.abs(sample[0] - black_scholes) < np.sqrt(sample[1])*(1.96))
true_values = np.zeros_like(sample[0]) + black_scholes
in_acceptance = (true_values >= sample[0] - np.sqrt(sample[1])*1.96) & (true_values <= sample[0] +  np.sqrt(sample[1])*1.96)


fig, ax = plt.subplots(figsize=(10,6))
fig.suptitle('Procent przedziałów ufności zawierających prawdziwą cenę opcji', x=0.48)
ax.fill_between(range(len(sample[0])), sample[0] -  np.sqrt(sample[1])*1.96, sample[0] + np.sqrt(sample[1])*1.96, color='limegreen', alpha=0.3, ls=(0, (1, 5)), edgecolor='darkgreen', step='mid')
ax.scatter(range(len(sample[0])), true_values, color='darkgreen', marker='o', s=5)
ax.scatter(np.where(~in_acceptance)[0], true_values[~in_acceptance], color='red', marker='x', s=50)
ax.set_title('wyliczoną z formuły Blacka-Scholesa', y=1.05, fontsize=10)


ax.set_yticks([min(sample[0] - np.sqrt(sample[1])*1.96), black_scholes, max(sample[0] +  np.sqrt(sample[1])*1.96)])
ax.set_xlabel('Liczba replikacji')
ax.set_ylabel('Wartości')
ax.legend(['Region akceptacji', 'Prawdziwa cena', 'Wartości spoza przedziału'])
ax.text(0.83, 0.10, f'Procent wartości w przedziale: {round(percent_in_interval*100, 2)}%', transform=plt.gca().transAxes, fontsize=9,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

plt.tight_layout()
plt.show()
'''

'''
            Estymatory warstwowe, optimal i proportional allocation
'''

'''
# EURO, proportional a CMC w zależności od ilości warstw
R = 8000
m = np.arange(0, R + 1, 100)
m[0] = 1

sample = np.array([strat_euro(R, i) for i in m])
smean = np.array([sample[i][0] for i in range(len(m))])
svar = np.array([sample[i][1] for i in range(len(m))])
dif = np.array(np.abs(smean - black_scholes))

fig, ax = plt.subplots(2, 1, figsize=(10,6), sharex=True)
fig.suptitle(f'Estymator warstwowy dla ceny opcji europejskiej z alokacją proporcjonalną (R = {R})', x=0.51)
ax[0].set_title('Wariancja', fontsize=10)
ax[1].set_title('Błąd bezwzględny w stosunku do formuły Blacka-Scholesa', fontsize=10)

ax[0].plot(m, svar, color='deepskyblue', marker='.')
ax[0].vlines(R/2 - 1, colors='r',ymin=0, ymax=max(svar), linestyles='dotted', label='*')
ax[1].plot(m, dif, color='crimson', marker='.')

ax[1].set_xlabel('Liczba warstw')
ax[0].set_ylabel('Wariancja')
ax[1].set_ylabel('Wartość błędu')
ax[0].grid(axis='y', color='midnightblue', alpha=0.1, in_layout=True)
ax[1].grid(axis='y', color='midnightblue', alpha=0.1, in_layout=True)

plt.tight_layout()
plt.show()
'''

'''
R = 8000
Rpilot = 1000
m = np.arange(0, int(R/8), 100)
m[0] = 1
optimals = [optimal_allocation(1000, R, i) for i in m]
sample = np.array([strat_euro(R, i, j) for i, j in zip(m, optimals)])
smean = np.array([sample[i][0] for i in range(len(m))])
svar = np.array([sample[i][1] for i in range(len(m))])
dif = np.array(np.abs(smean - black_scholes))

fig, ax = plt.subplots(2, 1, figsize=(10,6), sharex=True)
fig.suptitle(f'Estymator warstwowy dla ceny opcji europejskiej z alokacją optymalną (R = {R})', x=0.51)
ax[0].set_title('Wariancja', fontsize=10)
ax[0].plot(m, svar, color='lime', marker='.')
ax[0].set_ylabel('Wariancja')
ax[0].grid(axis='y', color='midnightblue', alpha=0.1, in_layout=True)

ax[1].set_title('Błąd bezwzględny w stosunku do formuły Blacka-Scholesa', fontsize=10)
ax[1].plot(m, dif, color='crimson', marker='.')
ax[1].set_xlabel('Liczba warstw')
ax[1].set_ylabel('Wartość błędu')
ax[1].grid(axis='y', color='midnightblue', alpha=0.1, in_layout=True)

plt.tight_layout()
plt.show()
'''


def main():
    global R, Rpilot, allocations, ax, black_scholes, cmc, cmc_asia10, cmc_asia2, cmc_euro, fig, i, j, optimals, osample, ovar, psample, pvar, stratas
    R = 1000

    cmc_euro = CMC_euro(R)

    cmc_asia2 = CMC_asia(R, 2)

    cmc_asia10 = CMC_asia(R, 10)

    black_scholes = BS()

    print(f'Budżet {R}')

    print('CRUDE MONTE CARLO \n'
          f'Euro: {cmc_euro[0]} \n'
          f'Asia2: {cmc_asia2[0]} \n'
          f'Asia10: {cmc_asia10[0]}')

    print(f'Black-Scholes formula (n=1): {black_scholes} \n'
          f'Błąd bezwzględny: {np.abs(cmc_euro[0] - black_scholes)} \n'
          f'Błąd względny: {np.abs(cmc_euro[0] - black_scholes)/black_scholes}')

    Rpilot = 1000

    R = [100, 500, 1000]

    stratas = np.array([np.linspace(i/10, i/4, 10).astype(int) for i in R])

    optimals = [[optimal_allocation(Rpilot, R[i], stratas[i][j], 1) for j in range(len(stratas[0]))] for i in range(len(R))]

    fig, ax = plt.subplots(3, 1, figsize=(10,6))

    fig.suptitle('Porównanie wariancji dla różnych metod alokacji')

    for i in range(len(R)):
          allocations = optimals[i]
          osample = [strat_euro(R[i], stratas[i][j], allocations[j]) for j in range(len(stratas[i]))]
          psample = [strat_euro(R[i], stratas[i][j]) for j in range(len(stratas[i]))]
          ovar = np.array([osample[j][1] for j in range(len(osample))])
          pvar = np.array([psample[j][1] for j in range(len(psample))])
          cmc = CMC_euro(R[i])[1]

          ax[i].plot(stratas[i], ovar, color='lime', marker = '.')
          ax[i].plot(stratas[i], pvar, color='deepskyblue', marker = '.')
          ax[i].hlines(cmc, stratas[i][0], stratas[i][-1], color='orangered', linestyles='--')
          ax[i].set_title(f'Dla R = {R[i]}', fontsize=10)

          ax[i].grid(axis='x', color='midnightblue', alpha=0.1, in_layout=True)
          ax[i].grid(axis='y', color='midnightblue', alpha=0.1, in_layout=True)

    ax[2].set_xlabel('Liczba warstw')

    ax[1].set_ylabel('Wartość błędu')

    ax[0].legend(['Alokacja optymalna', 'Alokacja proporcjonalna', 'CMC'])

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
