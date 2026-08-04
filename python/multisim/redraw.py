# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ========== 获取脚本所在目录 ==========
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)   # 将工作目录切换到脚本目录，方便后续相对路径

# ========== 文件配置（请根据实际文件名修改） ==========
DATA_FILE = "CUMCM2016-C-Appendix-Chinese.xlsx"      # 原始数据文件名
PARAM_FILE = "polynomial_parameters.xlsx"            # 拟合参数文件名
SHEET_DATA = "附件1"                                 # 原始数据的工作表名
SHEET_PARAM = "Sheet1"                               # 参数表的工作表名

# ========== 其他参数 ==========
Um = 9.0
REMOVE_INITIAL = 20          # 剔除前20个数据点
OUTPUT_DIR = "plots"         # 图片保存文件夹
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== 检查文件是否存在 ==========
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"原始数据文件 '{DATA_FILE}' 未找到，请放在 '{script_dir}' 目录下")
if not os.path.exists(PARAM_FILE):
    raise FileNotFoundError(f"参数文件 '{PARAM_FILE}' 未找到，请放在 '{script_dir}' 目录下")

# ========== 读取原始数据（附件1） ==========
data = pd.read_excel(DATA_FILE, sheet_name=SHEET_DATA, header=1)
print("原始数据列名：", data.columns.tolist())

# 自动识别时间列
time_col = None
for col in data.columns:
    if "时间" in col or "放电" in col:
        time_col = col
        break
if time_col is None:
    time_col = data.columns[0]
    print(f"未识别到时间列，将使用第一列 '{time_col}' 作为时间")
else:
    print(f"时间列识别为：'{time_col}'")

# 自动识别电流电压列
current_cols = [col for col in data.columns if "A" in col and col != time_col]
if not current_cols:
    raise ValueError("未找到包含 'A' 的电压列，请检查数据格式")
print("识别到的电流列：", current_cols)

# ========== 读取拟合参数表 ==========
param_df = pd.read_excel(PARAM_FILE, sheet_name=SHEET_PARAM)
print("参数表列名：", param_df.columns.tolist())

# 构建电流 -> (a,b,c,d) 字典
coeff_dict = {}
for _, row in param_df.iterrows():
    I = row["Current(A)"]
    coeff_dict[I] = (row["a"], row["b"], row["c"], row["d"])

# ========== 中文显示设置 ==========
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 循环绘制 ==========
for col in current_cols:
    I_str = col.replace("A", "").strip()
    try:
        I = int(I_str)
    except ValueError:
        print(f"无法解析电流值 '{col}'，跳过")
        continue

    if I not in coeff_dict:
        print(f"参数表中没有 {I}A，跳过")
        continue

    a, b, c, d = coeff_dict[I]

    time_series = data[time_col]
    voltage_series = data[col]
    df = pd.DataFrame({"time": time_series, "voltage": voltage_series})
    df = df.dropna()

    if len(df) <= REMOVE_INITIAL:
        print(f"{I}A 数据少于 {REMOVE_INITIAL+1} 行，跳过")
        continue

    df = df.iloc[REMOVE_INITIAL:]

    df["Ur"] = df["voltage"] - Um
    total_time = df["time"].max()
    df["Tr"] = total_time - df["time"]

    valid = df[df["Ur"] > 1e-6]
    if len(valid) == 0:
        print(f"{I}A 过滤后无有效数据")
        continue

    Ur = valid["Ur"].values
    Tr = valid["Tr"].values

    x_min, x_max = Ur.min(), Ur.max()
    if x_max - x_min < 1e-9:
        continue
    x_smooth = np.linspace(x_min, x_max, 100)
    y_smooth = a * x_smooth**3 + b * x_smooth**2 + c * x_smooth + d

    plt.figure(figsize=(9, 5))
    plt.scatter(Ur, Tr, s=12, c="#A5AEB7", label="实测样本点")
    plt.plot(x_smooth, y_smooth, color="#7AB656", linewidth=2.5, label="三次多项式拟合曲线")
    plt.xlabel("剩余电压 Ur (V)", fontsize=12)
    plt.ylabel("剩余放电时间 Tr (min)", fontsize=12)
    plt.title(f"{I} A 放电剩余电压 剩余时间曲线", fontsize=13)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()

    save_path = os.path.join(OUTPUT_DIR, f"{I}A.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"{I}A 图片已保存：{save_path}")

print(f"\n全部完成！图片保存在 '{os.path.join(script_dir, OUTPUT_DIR)}' 文件夹中")