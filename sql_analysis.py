import sqlite3
import pandas as pd

#====== 读取csv文件 ======
csv_path= 'user_behavior.csv'
df = pd.read_csv(csv_path, encoding='utf-8')

print("CSV文件读取成功,共", len(df), "条数据")
print("数据预览:")
print(df.head())

# =====链接数据库=====
# 如果 behavior.bdb 不存在，会自动创建
db_path = 'behavior.db'
conn = sqlite3.connect(db_path)

#===== 把DataFrame写入SQLite 表behavior =====
# if_exists="replace":如果behavior表存在，则删除原表，重新创建
# index=False:不把 pandas 的索引写入数据库
df.to_sql('behavior', conn, if_exists='replace', index=False)

print("\n数据已导入SQLite数据库,表名: behavior")
print("数据库文件:", db_path)

# ==== 写SQL,用 GROUP BY 统计每个用户的行为次数 =====
# 因为原始数据中 behavior_type 是“行”，这里用SUM(CASE WHEN ...) 来把行为类型转成“列”，方便统计
sql = """
SELECT
    user_id,
    SUM(CASE WHEN behavior_type = '浏览' THEN 1 ELSE 0 END) AS 浏览次数,
    SUM(CASE WHEN behavior_type = '加购' THEN 1 ELSE 0 END) AS 加购次数,
    SUM(CASE WHEN behavior_type = '下单' THEN 1 ELSE 0 END) AS 下单次数,
    SUM(CASE WHEN behavior_type = '支付' THEN 1 ELSE 0 END) AS 支付次数
FROM behavior
GROUP BY user_id
LIMIT 5;
"""

# ==== 用pandas执行SQL,并输出结果 =====
result_df = pd.read_sql_query(sql, conn)

print("\n每个用户的行为次数统计（前5条）:")
print(result_df.to_string(index=False))

# === 关闭数据库连接 =====
conn.close()
