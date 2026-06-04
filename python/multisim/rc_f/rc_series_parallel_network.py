import matplotlib.pyplot as plt
import numpy as np

# 1. 录入表6-3实验数据
f = np.array([300, 500, 1000, 1600, 2500, 5000, 6000, 10000, 495, 1591, 5756])
U1 = np.array([2964, 2955, 2941, 2929, 2917, 2891, 2885, 2870, 2956, 2929, 2886])
U2 = np.array([486, 693, 918, 972, 938, 738, 666, 464, 690, 972, 681])
A_u = U2 / U1

# 数据按频率升序排序
sort_idx = np.argsort(f)
f_sorted = f[sort_idx]
A_u_sorted = A_u[sort_idx]

# 2. 计算RC串并联选频网络的理论相频特性 (中心频率 f_0 = 1591.55 Hz)
f_0_theoretical = 1591.55
phase_theoretical = -np.degrees(np.arctan(((f_sorted / f_0_theoretical) - (f_0_theoretical / f_sorted)) / 3))

# 3. 开始绘图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

# 上图：幅频特性曲线
ax1.semilogx(f_sorted, A_u_sorted, 'o-', color='green', label='Experimental Data')
ax1.axvline(1591, color='red', linestyle='--', label='Measured f_0 (1591 Hz)')
ax1.axhline(1/3, color='gray', linestyle=':', label='Max Theoretical Gain (1/3)')
ax1.set_ylabel('Amplitude Gain (U2/U1)')
ax1.set_title('RC Series-Parallel Network Frequency Characteristics')
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