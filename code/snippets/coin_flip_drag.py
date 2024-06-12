import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

colors=['#4E9F50FF', '#87D180FF', '#EF8A0CFF', '#FCC66DFF', '#3CA8BCFF', '#98D9E4FF', '#94A323FF', '#C3CE3DFF', '#A08400FF', '#F7D42AFF', '#26897EFF', '#8DBFA8FF',]
plt.style.use('ggplot')
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=colors) 

N_TRAJ = 100
N_DRAWS = 100000

x = np.full((N_TRAJ, N_DRAWS + 1), 100.0)

random_binomial = np.random.binomial(n=1, p=0.5, size=(N_TRAJ, N_DRAWS))

for i in range(1, N_DRAWS + 1):
    x[:, i] = 0.99 * x[:, i - 1] + 2 * 0.01 * x[:, i - 1] * random_binomial[:, i - 1]


fig, ax = plt.subplots(figsize=(12,5))

draws=np.linspace(0, N_DRAWS, N_DRAWS+1)
for traj in x:
    ax.plot(draws, traj, linewidth=1)
ax.plot(draws, [100*(0.99*1.01)**(n/2) for n in draws], linestyle='--', c='black',)
    
ax.set_yscale("log")

fig.savefig("../../tex/img/coin_flip_drag.png", format='png', bbox_inches='tight', dpi=300)