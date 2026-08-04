# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ========== 脚本目录自动定位 ==========
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# ========== 文件配置 ==========
DATA_FILE = "CUMCM2016-C-Appendix-Chinese.xlsx"
PARAM_FILE = "polynomial_parameters.xlsx"
SHEET_DATA = "附件1"
SHEET_PARAM = "Sheet1"

# ========== 参数 ==========
Um = 9.0
REMOVE_INITIAL = 20
OUTPUT_DIR = "plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

target_currents = [30, 60, 100]
curve_colors = ['#1C75B3', "#78D863", "#D48080"]   # 30, 60, 100
scatter_color = "#4F4949"

# ========== 读取数据 ==========
data = pd.read_excel(DATA_FILE, sheet_name=SHEET_DATA, header=1)
time_col = None
for col in data.columns:
    if "时间" in col or "放电" in col:
        time_col = col
        break
if time_col is None:
    time_col = data.columns[0]

param_df = pd.read_excel(PARAM_FILE, sheet_name=SHEET_PARAM)
coeff_dict = {}
for _, row in param_df.iterrows():
    I = row["Current(A)"]
    coeff_dict[I] = (row["a"], row["b"], row["c"], row["d"])

# ========== 绘图 ==========
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(7, 4))

for idx, I in enumerate(target_currents):
    if I not in coeff_dict:
        print(f"警告：参数表中没有 {I}A，跳过")
        continue
    col_name = f"{I}A"
    if col_name not in data.columns:
        print(f"警告：数据中没有列 '{col_name}'，跳过")
        continue

    a, b, c, d = coeff_dict[I]
    time_series = data[time_col]
    voltage_series = data[col_name]
    df = pd.DataFrame({"time": time_series, "voltage": voltage_series})
    df = df.dropna()
    if len(df) <= REMOVE_INITIAL:
        continue
    df = df.iloc[REMOVE_INITIAL:]

    df["Ur"] = df["voltage"] - Um
    total_time = df["time"].max()
    df["Tr"] = total_time - df["time"]
    valid = df[df["Ur"] > 1e-6]
    if len(valid) == 0:
        continue

    Ur = valid["Ur"].values
    Tr = valid["Tr"].values
    x_min, x_max = Ur.min(), Ur.max()
    if x_max - x_min > 1e-9:
        x_smooth = np.linspace(x_min, x_max, 100)
        y_smooth = a * x_smooth**3 + b * x_smooth**2 + c * x_smooth + d
    else:
        continue

    # 散点：不加 label（图例统一添加）
    ax.scatter(Ur, Tr, s=5, color=scatter_color, alpha=0.6)
    # 拟合曲线：带电流标签
    ax.plot(x_smooth, y_smooth, color=curve_colors[idx], linewidth=1.8, label=f"{I}A 拟合曲线")

# 添加虚拟散点，用于图例中显示“实测点”（只出现一次）
ax.plot([], [], 'o', color=scatter_color, alpha=0.6, label="实测点")

# 图形装饰（无标题）
ax.set_xlabel("剩余电压 Ur (V)", fontsize=10)
ax.set_ylabel("剩余放电时间 Tr (min)", fontsize=10)
ax.legend(fontsize=9, loc='best')
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
save_path = os.path.join(OUTPUT_DIR, "30_60_100_combined.png")
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"组合图已保存：{save_path}")