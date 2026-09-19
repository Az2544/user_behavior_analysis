import pandas as pd

# ============ 第 1 步：读取 CSV 文件 ============
# 注意：因为之前生成数据时使用了 utf-8-sig 编码，读取时也要加 encoding 参数，防止中文乱码
print("正在读取数据...")
df = pd.read_csv("user_behavior.csv", encoding="utf-8-sig")
print(f"读取成功，共 {len(df)} 条数据。\n")

# ============ 第 2 步：检查缺失值 ============
print("--- 检查缺失值 ---")
# df.isnull() 会返回一个全是 True/False 的表格，.sum() 会把 True 当成 1 加起来
missing_data = df.isnull().sum()
print("各列缺失值数量：")
print(missing_data)

# 如果有缺失值，我们就进行清洗（删除包含缺失值的行）
if missing_data.sum() > 0:
    print("\n发现有缺失值，正在清洗...")
    # inplace=True 表示直接在原表格上修改，不用重新赋值
    df.dropna(inplace=True)
    print(f"清洗完成，剩余 {len(df)} 条数据。\n")
else:
    print("\n数据非常干净，没有缺失值！\n")

# ============ 第 3 步：计算漏斗转化率 ============
print("--- 计算漏斗转化率 ---")

# 1) 统计每种行为分别发生了多少次
# value_counts() 会自动统计某一列中每个值出现了多少次
behavior_counts = df["behavior_type"].value_counts()

# 2) 把每种行为的次数提取出来，方便后面计算
# 注意：用 .get() 可以防止因为某个行为没出现而报错
view_count = behavior_counts.get("浏览", 0)
cart_count = behavior_counts.get("加购", 0)
order_count = behavior_counts.get("下单", 0)
pay_count = behavior_counts.get("支付", 0)

print(f"行为总次数统计：")
print(f"  浏览 (view) : {view_count} 次")
print(f"  加购 (cart) : {cart_count} 次")
print(f"  下单 (order): {order_count} 次")
print(f"  支付 (pay)  : {pay_count} 次\n")

# 3) 依次计算每一步的转化率
# 转化率公式 = 下一步的次数 / 上一步的次数
rate_view_to_cart = cart_count / view_count if view_count > 0 else 0
rate_cart_to_order = order_count / cart_count if cart_count > 0 else 0
rate_order_to_pay = pay_count / order_count if order_count > 0 else 0
rate_view_to_pay = pay_count / view_count if view_count > 0 else 0  # 整体转化率

# 4) 打印每一步的转化率（格式化为百分比，保留两位小数）
print("漏斗转化率如下：")
print(f"  浏览 -> 加购 : {rate_view_to_cart * 100:.2f}%")
print(f"  加购 -> 下单 : {rate_cart_to_order * 100:.2f}%")
print(f"  下单 -> 支付 : {rate_order_to_pay * 100:.2f}%")
print(f"  整体转化率 (浏览 -> 支付) : {rate_view_to_pay * 100:.2f}%\n")

# ============ 第 4 步：找出流失最严重的环节 ============
print("--- 流失环节分析 ---")

# 流失率 = 1 - 转化率
loss_view_to_cart = 1 - rate_view_to_cart
loss_cart_to_order = 1 - rate_cart_to_order
loss_order_to_pay = 1 - rate_order_to_pay

# 把三个流失率放进一个字典里
loss_dict = {
    "浏览 -> 加购": loss_view_to_cart,
    "加购 -> 下单": loss_cart_to_order,
    "下单 -> 支付": loss_order_to_pay
}

# 找到流失率最高的环节（字典中值最大的键）
worst_step = max(loss_dict, key=loss_dict.get)
worst_loss_rate = loss_dict[worst_step]

print(f"⚠️ 流失最严重的环节是：【{worst_step}】")
print(f"该环节流失率高达：{worst_loss_rate * 100:.2f}%")
print(f"也就是说，有大约 {worst_loss_rate * 100:.1f}% 的用户在这个环节放弃了。")