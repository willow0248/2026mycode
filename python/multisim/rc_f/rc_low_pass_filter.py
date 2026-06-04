import matplotlib.pyplot as plt
import numpy as np

# 1. 录入表6-1实验数据
f = np.array([100, 200, 500, 1000, 1300, 1500, 1600, 1800, 2000, 5000, 1573])
U1 = np.array([2964, 2967, 2958, 2931, 2916, 2906, 2902, 2895, 2889, 2859, 2904])
U2 = np.array([2963, 2943, 2803, 2452, 2232, 2094, 2029, 1905, 1792, 897, 2047])
A_u = U2 / U1

# 数据按频率升序排序，确保曲线连线平滑
sort_idx = np.argsort(f)
f_sorted = f[sort_idx]
A_u_sorted = A_u[sort_idx]

# 2. 计算对应频率下的理论相频特性 (理论中心截止频率 f_c = 1591.55 Hz)
f_c_theoretical = 1591.55
phase_theoretical = -np.degrees(np.arctan(f_sorted / f_c_theoretical))

# 3. 开始绘图 (采用双子图展示幅频与相频)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

# 上图：幅频特性曲线
ax1.semilogx(f_sorted, A_u_sorted, 'o-', color='blue', label='Experimental Data')
ax1.axhline(0.707, color='red', linestyle='--', label='0.707 Cutoff')
ax1.axvline(1573, color='green', linestyle='--', label='Measured f_c (1573 Hz)')
ax1.set_ylabel('Amplitude Gain (U2/U1)')
ax1.set_title('RC Low-Pass Filter Frequency Characteristics')
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