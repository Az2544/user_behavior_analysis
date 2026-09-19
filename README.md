# 电商用户行为漏斗分析与自动化报表 📊

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557c.svg)](https://matplotlib.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## 📖 项目简介

本项目是一个基于 **Python** 的电商用户行为漏斗分析与自动化报表工具。  
通过模拟真实电商场景下的用户行为数据（浏览、加购、下单、支付），结合 **SQL 聚合分析**与 **Pandas 数据清洗**，自动计算多级漏斗转化率，找出流失最严重的环节，并生成高质量的**可视化图表**。适合作为数据分析入门到进阶的练手项目。

## 🛠️ 技术栈

*   **编程语言**: Python 3.8+
*   **数据处理**: [Pandas](https://pandas.pydata.org/) (数据清洗、分组聚合)
*   **数据存储**: [SQLite](https://www.sqlite.org/) (本地数据库，结构化查询)
*   **数据可视化**: [Matplotlib](https://matplotlib.org/) (漏斗柱状图绘制)
*   **版本控制**: Git & GitHub
*   **SQL**: 使用 `GROUP BY` 和 `CASE WHEN` 进行行为次数统计

## ✨ 核心功能

1. **模拟数据生成** (`generate_data.py`)：按权重比例自动生成 5000 条符合真实电商业务逻辑的用户行为日志（浏览最多，支付最少）。
2. **数据清洗与存储** (`sql_analysis.py`)：读取 CSV，清洗缺失值，并导入 SQLite 数据库，使用 SQL 语句对用户行为进行聚合统计。
3. **漏斗转化率分析** (`funnel_analysis.py`)：计算“浏览 -> 加购 -> 下单 -> 支付”各环节转化率，自动诊断流失最严重的环节。
4. **一键执行与可视化** (`main.py`)：整合全流程，终端打印完整分析结果，并生成直观的漏斗柱状图 `funnel_chart.png`。

## 📂 项目结构

```text
user_behavior_analysis/
├── generate_data.py       # 数据生成脚本 (5000条数据)
├── sql_analysis.py        # SQLite 入库与 SQL 统计脚本
├── funnel_analysis.py     # 纯 Pandas 漏斗计算脚本
├── main.py                # 一键整合脚本 (推荐运行)
├── user_behavior.csv      # 生成的原始数据文件
├── behavior.db            # SQLite 数据库文件
├── funnel_chart.png       # 自动生成的漏斗图表
└── README.md              # 项目说明文档 (本文件)