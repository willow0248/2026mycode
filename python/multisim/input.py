import matplotlib.pyplot as plt
import networkx as nx

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建有向图
G = nx.DiGraph()

# 定义节点
nodes = ["外部需求", "阅读输入：\n人文+技术", "大脑核心：\n算法重构", "执行器：\n创新实践", "结果反馈"]
G.add_nodes_from(nodes)

# 定义主链条边缘
edges = [(nodes[i], nodes[i+1]) for i in range(len(nodes)-1)]
G.add_edges_from(edges)

# --- 核心调整区 ---
# 1. 缩小间隙：横坐标步长从 2 降为 1.5
pos = {
    nodes[0]: (0, 0),
    nodes[1]: (1.5, 0),
    nodes[2]: (3.0, 0),
    nodes[3]: (4.5, 0),
    nodes[4]: (6.0, 0)
}

plt.figure(figsize=(10, 3)) # 缩小画布高度，显得更紧凑

# 绘制节点和主逻辑线
nx.draw(G, pos, with_labels=True, 
        node_size=2800,       # 略微调整节点大小适配间距
        node_color='white',    # 改为白色背景更像正式报告
        edgecolors='black',    # 边框黑色
        node_shape='s',        # 正方形
        font_size=9, 
        arrowsize=15, 
        width=1.2,
        edge_color='black')    # 主线全部黑色

# 2. 修改反馈线：由红弧线改为黑直线
# 我们通过 annotate 画一条带箭头的直线，稍微向下偏移一点点避免穿过文字
ax = plt.gca()
ax.annotate("",
            xy=pos[nodes[2]], xycoords='data',    # 终点：大脑核心
            xytext=pos[nodes[4]], textcoords='data', # 起点：结果反馈
            arrowprops=dict(arrowstyle="->", 
                            color="black",        # 黑色
                            connectionstyle="arc3,rad=0", # rad=0 就是直线
                            linestyle='-',        # 实线，如需虚线改为 '--'
                            linewidth=1.2))

# 添加反馈标注
plt.text(4.5, -0.15, "反馈回路", fontsize=9, ha='center', color='black')

# 隐藏坐标轴
plt.axis('off')
plt.tight_layout()
plt.show()