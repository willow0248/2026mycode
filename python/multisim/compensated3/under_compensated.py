import matplotlib.pyplot as plt
import numpy as np

# 解决中文和负号显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 基础数据
I_R = 0.136  # 日光灯有功电流
I_L = 0.203  # 日光灯感性无功电流

# 全部 12 组实验数据：(电容C, 电容电流Ic)
data = [
    (0, 0), (0.47, 0.032), (1.0, 0.071), (1.47, 0.105),
    (2.2, 0.159), (2.67, 0.192), (3.2, 0.228), (3.67, 0.261),
    (4.7, 0.335), (4.92, 0.349), (5.39, 0.382), (6.39, 0.407)
]

fig, ax = plt.subplots(figsize=(10, 8), dpi=150)

# 1. 绘制参考电压 U (X轴柔和橙色矢量)
ax.axhline(0, color='gray', linestyle='-', linewidth=0.5)
ax.annotate("", xy=(0.3, 0), xytext=(0, 0), 
            arrowprops=dict(color='#e67e22', width=1.5, headwidth=6))
ax.text(0.26, 0.01, r'$U$ (电源电压)', color='#e67e22', fontsize=12, fontweight='bold')

# 2. 绘制固定的日光灯电流 I_RL
ax.annotate("", xy=(I_R, -I_L), xytext=(0, 0), 
            arrowprops=dict(color='black', width=1.5, headwidth=6))
ax.text(I_R/2 - 0.02, -I_L/2 - 0.02, r'$I_{RL}$', color='black', fontsize=12)

# 3. 颜色映射设定 (生成从浅蓝到深蓝的连续渐变色)
cmap = plt.get_cmap('Blues')
# 从 0.4 开始取色，避免最初的颜色太浅在白底上看不清
colors = [cmap(0.4 + 0.6 * i / (len(data) - 1)) for i in range(len(data))]

# 4. 循环绘制各组数据
for i, (C, I_C) in enumerate(data):
    color = colors[i]
    
    # 绘制总电流 I (细实线箭头)
    ax.annotate("", xy=(I_R, -I_L + I_C), xytext=(0, 0), 
                arrowprops=dict(color=color, width=0.8, headwidth=4))
    
    # 绘制电容电流 Ic 辅助线 (细虚线)
    ax.plot([I_R, I_R], [-I_L, -I_L + I_C], color=color, linestyle='--', linewidth=0.8, alpha=0.8)
    
    # 交错标注 C 的值，防止文字重叠
    if i % 2 == 0:
        # 偶数索引标在右侧
        ax.text(I_R + 0.005, -I_L + I_C, f'{C}μF', color=color, fontsize=8, va='center')
    else:
        # 奇数索引标在左侧
        ax.text(I_R - 0.035, -I_L + I_C, f'{C}μF', color=color, fontsize=8, va='center')

# 5. 图表边界与装饰设定
ax.set_xlim(-0.02, 0.32)
ax.set_ylim(-0.25, 0.25)
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_title('相量图：并联电容全过程轨迹变化', fontsize=16, fontweight='bold')
ax.set_xlabel('有功电流 (A)', fontsize=12)
ax.set_ylabel('无功电流 (A)', fontsize=12)

plt.tight_layout()
plt.show()