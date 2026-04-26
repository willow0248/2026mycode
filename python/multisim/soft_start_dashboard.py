import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# ---------------------- 物理模型（简化版） ----------------------
def simulate_softstart(R1, C1, RL, Vin=5, Vth=2.5):
    """
    返回 t, v_gate, v_out 三个 ndarray
    R1, RL  : Ω
    C1      : F
    """
    tau = R1 * C1                      # 栅极 RC 常数
    t_end = 6 * tau or 1e-3            # 至少 1 ms
    t = np.linspace(0, t_end, 1500)    # 1500 点足够平滑

    # VGATE：一阶 RC 充电
    v_gate = Vin * (1 - np.exp(-t / tau))

    # 简化 MOS 导通模型：当 VGATE > Vth，DRAIN 跟随 VGATE
    # 让 VOUT(t) ≈ VIN * (1 - exp(-(t-td)/tau_out))，其中 td 为 VGATE 刚超过 Vth 的时刻
    idx_on = np.argmax(v_gate > Vth)   # 找到第一次超过门限的索引
    if idx_on == 0:
        td = 0.0
    else:
        td = t[idx_on]

    tau_out = RL * 1e-6                # 假设输出端等效电容 1 µF
    v_out = np.zeros_like(t)
    mask = t >= td
    v_out[mask] = Vin * (1 - np.exp(-(t[mask] - td) / tau_out))
    # 关断逻辑（此处用固定占空比 50% 演示）
    # 如果需要 Control 方波，可再加滑条控制；此处只做上电软启动

    return t * 1e3, v_gate, v_out      # 单位：ms, V, V

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title='RC Soft-Start Dashboard', layout='wide')
st.title('P-MOS RC 软启动可视化')

col1, col2 = st.columns([1, 3])        # 左侧参数，右侧图

with col1:
    st.subheader('参数设定')
    R1_k = st.slider('R1 (上拉电阻, kΩ)', 1.0, 100.0, 10.0, 0.5)
    C1_u = st.slider('C1 (启动电容, µF)', 0.01, 10.0, 0.1, 0.01)
    RL_k = st.slider('负载电阻 RL (kΩ)', 1.0, 100.0, 10.0, 1.0)

    # 换算到 SI
    R1, C1, RL = R1_k * 1e3, C1_u * 1e-6, RL_k * 1e3
    tau_ms = R1 * C1 * 1e3            # τ (ms)
    st.markdown(f'**时间常数 τ ≈ {tau_ms:.2f} ms**')

# ---------------------- 计算并画图 ----------------------
t, v_gate, v_out = simulate_softstart(R1, C1, RL)

with col2:
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(t, v_out, lw=2.3, color='steelblue', label='VOUT  (Drain)')
    ax.plot(t, v_gate, lw=2.0, color='indianred', label='VGATE (Gate)')

    ax.set_xlabel('Time  /  ms')
    ax.set_ylabel('Voltage  /  V')
    ax.set_title('Soft-Start Waveform', loc='left', fontsize=14, weight='bold')

    # 主刻度：把横轴分成 10 格
    ax.xaxis.set_major_locator(mtick.MultipleLocator(max(t)/10))
    ax.xaxis.set_minor_locator(mtick.MultipleLocator(max(t)/50))
    ax.yaxis.set_major_locator(mtick.MultipleLocator(1))
    ax.grid(which='major', color='#DDDDDD')
    ax.grid(which='minor', color='#EEEEEE', linestyle=':')

    ax.legend(frameon=False, loc='upper right')
    st.pyplot(fig)

# ---------------------- 异常 / 临界提示 ----------------------
if tau_ms < 0.02:
    st.warning('⚠️ τ 太小，软启动基本失效（几乎是硬上电）')
elif tau_ms > 200:
    st.warning('⚠️ τ 非常大，启动将明显拖慢系统，注意检查参数是否合理')