import matplotlib.pyplot as plt
import numpy as np

# 1. 录入表6-2实验数据
f = np.array([100, 500, 1000, 1300, 1500, 1600, 2500, 4000, 10000, 20000, 1549])
U1 = np.array([2964, 2958, 2935, 2916, 2907, 2903, 2878, 2862, 2858, 2859, 2905])
U2 = np.array([196.6, 909, 1561, 1835, 1977, 2040, 2399, 2635, 2814, 2847, 2073])
A_u = U2 / U1

# 数据按频率升序排序
sort_idx = np.argsort(f)
f_sorted = f[sort_idx]
A_u_sorted = A_u[sort_idx]

# 2. 计算对应频率下的理论相频特性 (f_c = 1591.55 Hz)
f_c_theoretical = 1591.55
phase_theoretical = np.degrees(np.arctan(f_c_theoretical / f_sorted))

# 3. 开始绘图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

# 上图：幅频特性曲线
ax1.semilogx(f_sorted, A_u_sorted, 'o-', color='orange', label='Experimental Data')
ax1.axhline(0.707, color='red', linestyle='--', label='0.707 Cutoff')
ax1.axvline(1549, color='green', linestyle='--', label='Measured f_c (1549 Hz)')
ax1.set_ylabel('Amplitude Gain (U2/U1)')
ax1.set_title('RC High-Pass Filter Frequency Characteristics')
ax1.grid(True, which="both", linestyle="--")
ax1.legend()

# 下图：相频特性曲线
ax2.semilogx(f_sorted, phase_theoretical, 's--', color='purple', label='Theoretical Phase')
ax2.set_xlabel('Frequency f (Hz)')
ax2.set_ylabel('Phase Shift (Degrees)')
ax2.grid(True, which="both", linestyle="--")
ax2.legend()

plt.tight_layout()
plt.show()