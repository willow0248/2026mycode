import matplotlib.pyplot as plt

# --- 数据区 (已根据你的实验记录表 2-3, 2-4 和 2-1 提取) ---

# 1. 实验值 (表2-3：有源二端网络外特性数据)
# 对应 R_L = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, ∞]
i_exp = [12.51, 10.20, 8.65, 6.95, 6.78, 5.86, 5.03, 4.71,4.46, 4.37, 0]    # 测得的电流 (mA)
u_exp = [0.02,  1.02,  1.16, 2.04, 2.68, 2.90, 3.01, 3.11, 3.73, 3.88, 6.16] # 测得的电压 (V)

# 2. 等效值 (表2-4：等效电压源的外特性数据)
# 对应 R_L = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, ∞]
i_eq = [12.73, 10.78, 9.26, 8.15, 7.28, 6.28, 6.00, 5.51, 5.10, 4.74, 0]     # 测得的电流 (mA)
u_eq = [0,     1.06,  1.83, 2.42, 2.88, 3.25, 3.56, 3.81, 4.02, 4.22, 6.73]  # 测得的电压 (V)

# 3. 理论值 (根据表2-1的理论值确定的理想直线)
# 取两端点：开路 (I=0, U=Uoc=6.72V) 和 短路 (I=Isc=12.95mA, U=0)
i_theo = [0, 12.95]
u_theo = [6.72, 0]
# -----------------------------------------------------------

# 创建图表
plt.figure(figsize=(10, 6))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 绘制曲线 (注意这里横坐标分别使用了各自的电流列表)
plt.plot(i_exp, u_exp, 'ro-', label='实验外特性 (Original)')
plt.plot(i_eq, u_eq, 'bs--', label='等效外特性 (Equivalent)')
plt.plot(i_theo, u_theo, 'g-', linewidth=2, label='理论外特性 (Theoretical)')

# 图表装饰
plt.title('有源二端网络外特性曲线比较', fontsize=14)
plt.xlabel('负载电流 $I_L$ (mA)', fontsize=12)
plt.ylabel('负载电压 $U_L$ (V)', fontsize=12)

# 设置坐标轴范围让图表更好看
plt.xlim(0, 14)
plt.ylim(0, 8)

plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

# 显示图像
plt.show()