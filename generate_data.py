"""
生成模拟电商用户行为数据集，保存为 user_behavior.csv
运行环境：Python 3.6 以上，无需安装任何第三方库
"""

import csv          # 用来写 CSV 文件
import random       # 用来生成随机数
from datetime import datetime, timedelta   # 用来处理时间

# ============ 第 1 步：设置随机种子 ============
# 设置种子后，每次运行生成的随机数据都一样，方便复现结果
# 如果想每次运行结果都不同，把这一行删掉或改成 random.seed()
random.seed(42)

# ============ 第 2 步：配置参数 ============
TOTAL_ROWS = 5000        # 总共生成 5000 条数据
USER_NUM = 800           # 模拟 800 个不同的用户
START_DATE = datetime(2025, 1, 1, 0, 0, 0)      # 数据起始时间
END_DATE   = datetime(2025, 1, 31, 23, 59, 59)  # 数据结束时间
TOTAL_DAYS = (END_DATE - START_DATE).days       # 一共多少天

# 行为类型 & 各自出现概率（权重越大出现越多）
# 真实电商场景里：浏览 >> 加购 > 下单 > 支付
behaviors = ["浏览", "加购", "下单", "支付"]
weights   = [0.70,   0.18,   0.08,    0.04]   # 加起来 = 1.0

# 一天中每个小时的活跃权重（共 24 个数字，对应 0 点 ~ 23 点）
# 数值越大，该小时出现数据的概率越高；晚上 20-22 点是购物高峰
hour_weights = [
    1,  1,  1,  1,  1,  2,      # 0-5 点   凌晨，几乎没人
    4,  8,  12, 14, 14, 12,     # 6-11 点  早上到中午
    10, 10, 12, 12, 12, 14,     # 12-17 点 下午
    18, 22, 25, 24, 16, 6       # 18-23 点 晚上高峰
]

# ============ 第 3 步：准备用户 ID 列表 ============
user_ids = [10001 + i for i in range(USER_NUM)]   # 10001 ~ 10800

# ============ 第 4 步：循环生成 5000 条数据 ============
rows = []   # 用一个列表暂存所有数据，最后统一写入文件

for i in range(TOTAL_ROWS):
    # 1) 随机选一个用户
    user_id = random.choice(user_ids)

    # 2) 按权重随机选一种行为
    #    random.choices 会按 weights 的概率返回，k=1 表示取 1 个
    behavior = random.choices(behaviors, weights=weights, k=1)[0]

    # 3) 随机生成时间戳
    day    = random.randint(0, TOTAL_DAYS - 1)                        # 随机某一天
    hour   = random.choices(range(24), weights=hour_weights, k=1)[0]  # 按小时权重选小时
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    ts = START_DATE + timedelta(days=day, hours=hour,
                                minutes=minute, seconds=second)

    # 4) 把时间格式化成 "YYYY-MM-DD HH:MM:SS"
    ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")

    # 5) 存进列表
    rows.append([user_id, behavior, ts_str])

# ============ 第 5 步：按时间先后排序（看起来更像真实日志）============
rows.sort(key=lambda x: x[2])

# ============ 第 6 步：写入 CSV 文件 ============
# newline="" 是为了避免 Windows 下每行之间多出空行
# encoding="utf-8-sig" 是为了用 Excel 打开时中文不乱码
with open("user_behavior.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["user_id", "behavior_type", "timestamp"])  # 写表头
    writer.writerows(rows)                                       # 一次性写入所有数据

# ============ 第 7 步：打印统计信息，检查数据是否合理 ============
print(f"✅ 生成完成！共 {len(rows)} 条数据，已保存到 user_behavior.csv\n")

from collections import Counter
counter = Counter(r[1] for r in rows)   # 统计每种行为出现次数

print("各行为数量统计：")
for b in behaviors:
    cnt = counter[b]
    print(f"  {b:6s}: {cnt:5d} 条  ({cnt / TOTAL_ROWS * 100:.1f}%)")

print("\n前 5 行预览：")
for r in rows[:5]:
    print("  ", r)