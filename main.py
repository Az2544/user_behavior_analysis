"""
电商用户行为漏斗分析 - 整合脚本
功能：读取数据 -> 清洗 -> 计算转化率 -> 找出流失环节 -> 绘制漏斗柱状图并保存
运行前请确保已安装 pandas 和 matplotlib：
pip install pandas matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. 解决 matplotlib 中文显示乱码问题
# ==========================================
# 设置字体为黑体（SimHei），适用于 Windows 系统
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像时负号 '-' 显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

def main():
    print("=" * 40)
    print("📊 电商用户行为漏斗分析系统")
    print("=" * 40)

    # ============ 第 1 步：读取数据 ============
    print("\n[1/4] 正在读取数据...")
    csv_path = "user_behavior.csv"
    try:
        # encoding="utf-8-sig" 是为了防止中文列名乱码
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"❌ 找不到文件 {csv_path}，请确认当前目录下是否有该文件！")
        return

    print(f"✅ 数据读取成功，共 {len(df)} 条记录。")

    # ============ 第 2 步：检查与清洗缺失值 ============
    print("\n[2/4] 正在检查缺失值...")
    missing_data = df.isnull().sum()
    total_missing = missing_data.sum()

    if total_missing > 0:
        print(f"⚠️ 发现 {total_missing} 个缺失值，正在进行清洗...")
        # 删除包含缺失值的行（inplace=True 表示直接在原数据上修改）
        df.dropna(inplace=True)
        print(f"✅ 清洗完成，剩余 {len(df)} 条记录。")
    else:
        print("✅ 数据非常干净，没有缺失值！")

    # ============ 第 3 步：计算漏斗转化率 ============
    print("\n[3/4] 正在计算漏斗转化率...")
    
    # 统计每种行为的次数（value_counts 会自动按数量降序排列）
    behavior_counts = df["behavior_type"].value_counts()
    
    # 按照漏斗顺序提取数据，使用 .get() 防止某一步为 0 时报错
    steps = ["浏览", "加购", "下单", "支付"]
    values = [behavior_counts.get(step, 0) for step in steps]

    print("\n--- 行为总次数统计 ---")
    for step, val in zip(steps, values):
        print(f"  {step}: {val} 次")

    # 计算每一步的转化率
    # 转化率 = 下一步的次数 / 上一步的次数
    rates = []
    for i in range(len(values) - 1):
        if values[i] > 0:
            rate = values[i + 1] / values[i]
        else:
            rate = 0
        rates.append(rate)

    # 整体转化率（浏览 -> 支付）
    overall_rate = values[-1] / values[0] if values[0] > 0 else 0

    print("\n--- 漏斗转化率 ---")
    for i in range(len(rates)):
        print(f"  {steps[i]} -> {steps[i+1]}: {rates[i] * 100:.2f}%")
    print(f"  整体转化率 (浏览 -> 支付): {overall_rate * 100:.2f}%")

    # 找出流失最严重的环节
    # 流失率 = 1 - 转化率
    losses = [1 - r for r in rates]
    worst_idx = losses.index(max(losses))  # 找到流失率最大的索引
    worst_step = f"{steps[worst_idx]} -> {steps[worst_idx+1]}"
    worst_loss_rate = losses[worst_idx]

    print("\n--- 流失环节诊断 ---")
    print(f"⚠️ 流失最严重的环节是：【{worst_step}】")
    print(f"   该环节流失率高达：{worst_loss_rate * 100:.2f}%")

    # ============ 第 4 步：绘制漏斗柱状图 ============
    print("\n[4/4] 正在绘制漏斗图表...")
    
    # 设置画布大小
    plt.figure(figsize=(10, 6))
    
    # 为了从上到下显示，我们将数据反转
    plot_steps = steps[::-1]
    plot_values = values[::-1]
    # 使用浅蓝色作为柱状图颜色
    colors = ['#87CEEB', '#5B9BD5', '#4472C4', '#2F5597'] 
    
    # 绘制横向柱状图 (barh)
    bars = plt.barh(plot_steps, plot_values, color=colors)
    
    # 设置标题和坐标轴标签
    plt.title("电商用户行为漏斗转化图", fontsize=18, fontweight='bold', pad=20)
    plt.xlabel("用户数量 (人)", fontsize=12)
    plt.ylabel("行为阶段", fontsize=12)
    
    # 在柱状图旁边添加数值和转化率标注
    for i, bar in enumerate(bars):
        # 获取柱子的宽度（即数值）
        width = bar.get_width()
        # 在柱子右侧添加数值文本
        plt.text(width + (max(values) * 0.02), bar.get_y() + bar.get_height()/2, 
                 f"{width}次", va='center', fontsize=11)
        
        # 如果不是最后一步（支付），就添加转化率文本
        if i < len(plot_steps) - 1:
            # 因为是反转的，转化率的顺序也要注意对应
            rate_val = rates[len(plot_steps) - 2 - i] 
            plt.text(width + (max(values) * 0.02), bar.get_y() + bar.get_height()/2 - 0.3, 
                     f"转化率: {rate_val*100:.1f}%", va='center', fontsize=10, color='#d62728')

    # 自动调整布局，防止文字被遮挡
    plt.tight_layout()
    
    # 保存图片，dpi=300 保证图片清晰
    output_file = "funnel_chart.png"
    plt.savefig(output_file, dpi=300)
    print(f"✅ 图表已成功保存为：{output_file}")
    
    # 显示图表（如果在本地 VS Code 运行，会弹出一个窗口）
    plt.show()

    print("\n" + "=" * 40)
    print("🎉 一键分析完成！请查看生成的 funnel_chart.png")
    print("=" * 40)

# 当直接运行该脚本时，执行 main 函数
if __name__ == "__main__":
    main()