import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# 从图片表格中提取的实验数据
C_data = np.array([0, 0.47, 1.0, 1.47, 2.2, 2.67, 3.2, 3.67, 4.7, 4.92, 5.39, 6.39])
cos_phi_data = np.array([0.57, 0.62, 0.71, 0.79, 0.90, 0.98, 0.87, 0.83, 0.66, 0.62, 0.57, 0.45])

# 设置中文字体，防止图表中的中文显示为方块
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows 系统常用
plt.rcParams['axes.unicode_minus'] = False 

# 生成平滑曲线所需的密集 X 轴数据
C_smooth = np.linspace(C_data.min(), C_data.max(), 300)

# 使用 B 样条插值生成平滑的曲线
spline = make_interp_spline(C_data, cos_phi_data, k=3)
cos_phi_smooth = spline(C_smooth)

# 限制平滑曲线的值不超出物理极值 (不能大于 1)
cos_phi_smooth = np.clip(cos_phi_smooth, 0, 1)

# 开始绘图
plt.figure(figsize=(10, 6), dpi=120)

# 绘制平滑曲线和实际散点
plt.plot(C_smooth, cos_phi_smooth, color='#1f77b4', linewidth=2, label='拟合趋势线')
plt.scatter(C_data, cos_phi_data, color='#d62728', s=50, zorder=5, label='实验测量点')

# 找到并标记最大值点
max_idx = np.argmax(cos_phi_data)
max_C = C_data[max_idx]
max_cos = cos_phi_data[max_idx]

# 注意这里加上了 'r' 前缀
plt.annotate(r'最高点 (C={}, $\cos\varphi$={})'.format(max_C, max_cos),
             xy=(max_C, max_cos),
             xytext=(max_C + 0.5, max_cos - 0.05),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6),
             fontsize=11)

# 图表装饰，注意这里都加上了 'r' 前缀
plt.title(r'功率因数 $\cos\varphi$ 与并联电容 $C$ 的关系曲线', fontsize=16, fontweight='bold')
plt.xlabel(r'并联电容 $C \ (\mu F)$', fontsize=14)
plt.ylabel(r'功率因数 $\cos\varphi$', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12, loc='lower left')

# 设定合理的坐标轴范围
plt.ylim(0.4, 1.05)
plt.xlim(-0.2, 7)

# 显示图表
plt.tight_layout()
plt.show()