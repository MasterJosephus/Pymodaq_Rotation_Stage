from matplotlib import pyplot as plt    
import numpy as np 
from scipy.optimize import curve_fit

def fit_func(x, a, b, c):
    return a * np.sin(4 * np.pi * (x - b) / 180) + c

data = np.loadtxt('data_scan.csv', skiprows=1, delimiter=',')  
x = data[:, 0]
y = data[:, 1]

popt, pcov = curve_fit(fit_func, x, y)

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.plot(x, y, 'or', markerfacecolor='w', label='Data')

xfine = np.linspace(0, 360, 1000)
yfit = fit_func(xfine, *popt)
parallel = xfine[yfit==np.min(yfit)][0]  # find the angle corresponding to the minimum of the fit function}
perp = parallel + 45
MA = parallel + 54.7/2
ax.plot(xfine, yfit, '-b', label='Fit')


ax.axvline(parallel, color='k', linestyle='--', label=f'Parallel ({parallel:.2f}°)')
ax.axvline(perp, color='r', linestyle='--', label=f'Perpendicular ({perp:.2f}°)')
ax.axvline(MA, color='g', linestyle='--', label=f'Magic Angle ({MA:.2f}°)')

ax.set_xlabel('Position (°)')
ax.set_ylabel('Intensity (a.u.)')
ax.set_title('Scan Data')
ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
fig.tight_layout()
fig.savefig('scan_data_fit.png', dpi=300)
plt.show()