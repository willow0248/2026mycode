# plot_rc.py —— 运行后弹窗显示并生成 rc_compare.png
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

sns.set_theme(style='whitegrid', font_scale=1.2)

def draw(csv_path, label, color):
    df = pd.read_csv(csv_path, skiprows=4)   # Multisim 前4行是说明
    t = df.iloc[:, 0] * 1e3                 # s -> ms
    v = df.iloc[:, 1]
    plt.plot(t, v, label=label, color=color, lw=2)

draw(r'C:\2026mycode\python\multisim\10KR0.1UF.csv', 'Ideal C', 'steelblue')

plt.xlabel('Time / ms')
plt.ylabel('Vc / V')
plt.title('RC Step Response')
plt.xlim(0, 15)          # 根据你的 Stop Time 调整

ax = plt.gca()                       # 获取当前坐标轴
ax.xaxis.set_major_locator(mtick.MultipleLocator(1))    # 主刻度 1 ms
ax.xaxis.set_minor_locator(mtick.MultipleLocator(0.2))  # 次刻度 0.2 ms，可选
ax.tick_params(axis='x', which='major', length=6)       # 主刻度稍长
ax.tick_params(axis='x', which='minor', length=3)       # 次刻度稍短

plt.legend()
plt.tight_layout()
plt.savefig('rc_compare.png', dpi=300)
plt.show()