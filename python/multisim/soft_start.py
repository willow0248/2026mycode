import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
from pathlib import Path

# -------- 1. 读 CSV & 清洗 ---------------------------------
CSV = Path(r'C:\2026mycode\python\multisim\soft_start.csv')

df = pd.read_csv(CSV, skiprows=4, header=None)   # 无表头，前 4 行是注释
df = df.dropna(axis=1, how='all')                # 去掉全空列

# 一般情况下现在只剩 4 列：X1, Y1, X2, Y2
t1, v1 = df.iloc[:, 0], df.iloc[:, 1]
t2, v2 = df.iloc[:, 2], df.iloc[:, 3]

# 转毫秒
t1_ms = t1 * 1e3
t2_ms = t2 * 1e3

# -------- 2. 画图 ------------------------------------------
sns.set_theme(style='ticks', font='Times New Roman', font_scale=1.3)
plt.figure(figsize=(12, 4.5), dpi=160)           # 1920×450 px

plt.plot(t1_ms, v1, lw=2.3, color='steelblue',  label='VOUT  (Drain)')
plt.plot(t2_ms, v2, lw=2.0, color='indianred',  label='VGATE (Gate)')

plt.xlabel('Time  /  ms')
plt.ylabel('Voltage  /  V')

# x 轴范围：自动以一整周期为准
x_end = max(t1_ms.max(), t2_ms.max())
plt.xlim(0, x_end)

# 网格与刻度
ax = plt.gca()
main_step = round(x_end / 10, 2) or 1            # 主刻度≈10 格
ax.xaxis.set_major_locator(mtick.MultipleLocator(main_step))
ax.xaxis.set_minor_locator(mtick.MultipleLocator(main_step / 5))
ax.yaxis.set_major_locator(mtick.MultipleLocator(1))
ax.grid(which='major', color='#DDDDDD')
ax.grid(which='minor', color='#EEEEEE', linestyle=':')

plt.title('P-MOS Soft-Start – RC Transient', loc='left', fontsize=16, weight='bold')
plt.suptitle('R1 = 10 kΩ,  C1 = 0.1 µF   (τ ≈ 1 ms)', x=0.01, y=0.98,
             ha='left', va='top', fontsize=10, color='gray')

plt.legend(frameon=False)
plt.tight_layout()

out_png = CSV.with_suffix('.png').name           # 与 CSV 同名 png
plt.savefig(out_png, dpi=300)
plt.show()
print(f'图已保存为 {out_png}')