import numpy as np
import matplotlib.pyplot as plt

# 设置 matplotlib 支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows 常用中文字体
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

# ==================== 1. 实验数据输入与初始化 ====================
# 线电压基准值 (V)
U_val = 220
# 实验测得的三个相电流幅值 (mA)
I_AB_mag = 78.8
I_BC_mag = 149.3
I_CA_mag = 75.0

# 设定线电压相量（以 U_AB 为参考相量，角度为 0°，正序系统）
U_AB = U_val * np.exp(1j * np.deg2rad(0))
U_BC = U_val * np.exp(1j * np.deg2rad(-120))
U_CA = U_val * np.exp(1j * np.deg2rad(120))

# 纯阻性负载下，相电流与对应的相电压同相位
I_AB = I_AB_mag * np.exp(1j * np.deg2rad(0))
I_BC = I_BC_mag * np.exp(1j * np.deg2rad(-120))
I_CA = I_CA_mag * np.exp(1j * np.deg2rad(120))

# 根据 KCL（基尔霍夫电流定律）计算三个线电流相量
I_A = I_AB - I_CA
I_B = I_BC - I_AB
I_C = I_CA - I_BC

# ==================== 2. 开始绘制相量图 ====================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))

# ----- 左子图：各相电压相量图 -----
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.axhline(0, color='black', linewidth=1)
ax1.axvline(0, color='black', linewidth=1)

# 绘制电压向量
ax1.quiver(0, 0, U_AB.real, U_AB.imag, angles='xy', scale_units='xy', scale=1, color='r', label='U_AB')
ax1.quiver(0, 0, U_BC.real, U_BC.imag, angles='xy', scale_units='xy', scale=1, color='g', label='U_BC')
ax1.quiver(0, 0, U_CA.real, U_CA.imag, angles='xy', scale_units='xy', scale=1, color='b', label='U_CA')

# 文本标注
ax1.text(U_AB.real+5, U_AB.imag, f'U_AB\n{abs(U_AB):.1f}V', color='r', fontsize=11, va='center')
ax1.text(U_BC.real-25, U_BC.imag-15, f'U_BC\n{abs(U_BC):.1f}V', color='g', fontsize=11)
ax1.text(U_CA.real-25, U_CA.imag+5, f'U_CA\n{abs(U_CA):.1f}V', color='b', fontsize=11)

ax1.set_xlim(-260, 260)
ax1.set_ylim(-260, 260)
ax1.set_aspect('equal')
ax1.set_title('各相电压相量图 (V)', fontsize=14, pad=15)
ax1.legend(loc='upper right')

# ----- 右子图：相电流与线电流相量图 -----
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.axhline(0, color='black', linewidth=1)
ax2.axvline(0, color='black', linewidth=1)

# 绘制相电流向量（细实线）
ax2.quiver(0, 0, I_AB.real, I_AB.imag, angles='xy', scale_units='xy', scale=1, color='orange', label='相电流 I_ph')
ax2.quiver(0, 0, I_BC.real, I_BC.imag, angles='xy', scale_units='xy', scale=1, color='orange')
ax2.quiver(0, 0, I_CA.real, I_CA.imag, angles='xy', scale_units='xy', scale=1, color='orange')

# 绘制线电流向量（粗箭头，用于区分）
ax2.quiver(0, 0, I_A.real, I_A.imag, angles='xy', scale_units='xy', scale=1, color='r', width=0.007, label='线电流 I_l')
ax2.quiver(0, 0, I_B.real, I_B.imag, angles='xy', scale_units='xy', scale=1, color='g', width=0.007)
ax2.quiver(0, 0, I_C.real, I_C.imag, angles='xy', scale_units='xy', scale=1, color='b', width=0.007)

# 文本标注
ax2.text(I_AB.real+5, I_AB.imag-10, f'I_AB={abs(I_AB):.1f}mA', color='orange', fontsize=10)
ax2.text(I_BC.real-15, I_BC.imag-15, f'I_BC={abs(I_BC):.1f}mA', color='orange', fontsize=10)
ax2.text(I_CA.real-65, I_CA.imag+10, f'I_CA={abs(I_CA):.1f}mA', color='orange', fontsize=10)

ax2.text(I_A.real+5, I_A.imag+5, f'I_A={abs(I_A):.1f}mA', color='r', fontsize=11, fontweight='bold')
ax2.text(I_B.real-15, I_B.imag-20, f'I_B={abs(I_B):.1f}mA', color='g', fontsize=11, fontweight='bold')
ax2.text(I_C.real+5, I_C.imag+10, f'I_C={abs(I_C):.1f}mA', color='b', fontsize=11, fontweight='bold')

ax2.set_xlim(-240, 240)
ax2.set_ylim(-240, 240)
ax2.set_aspect('equal')
ax2.set_title('相电流与线电流相量图 (mA)', fontsize=14, pad=15)
ax2.legend(loc='upper right')

# 调整布局并展示
plt.tight_layout()
plt.suptitle('不对称三角形连接负载有功数据定量验证相量图', fontsize=16, y=1.02)
plt.show()

# ==================== 3. 打印数据定量对比数据 ====================
print("======= 实验数据正确性定量校验 (KCL 验证) =======")
print(f"A线电流 -> 理论计算值: {abs(I_A):.2f} mA | 实验测得值: 134.0 mA")
print(f"B线电流 -> 理论计算值: {abs(I_B):.2f} mA | 实验测得值: 207.0 mA")
print(f"C线电流 -> 理论计算值: {abs(I_C):.2f} mA | 实验测得值: 204.5 mA")