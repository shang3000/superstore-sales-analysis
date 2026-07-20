"""
模块入口：演示如何调用 src/analysis/ 和 src/utils/ 中的函数。

用法：
    python src/run_analysis.py
"""

import sys
from pathlib import Path

# 将项目根目录加入 Python 路径，使得 import src.xxx 可以工作
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.utils.loaders import load_cleaned_data
from src.analysis.trends import kpi_summary, yearly_trend
from src.analysis.segments import region_summary, state_summary
from src.analysis.category import category_summary, loss_subcategories
from src.analysis.customers import segment_summary, top_customers, rfm_analysis
from src.analysis.insights import loss_orders_summary, high_discount_impact, correlation_matrix


def main():
    print("=" * 60)
    print("📊 Superstore 分析模块运行入口")
    print("=" * 60)

    df = load_cleaned_data()
    print(f"\n数据量: {len(df)} 条记录")
    print(f"时间范围: {df['Order Date'].min().date()} ~ {df['Order Date'].max().date()}")

    print("\n📈 核心 KPI")
    kpi = kpi_summary(df)
    for k, v in kpi.items():
        print(f"   {k}: {v:,.2f}")

    print("\n🗺️  区域表现")
    print(region_summary(df).to_string(index=False))

    print("\n📦 品类表现")
    print(category_summary(df).to_string(index=False))

    print("\n👥 客户类型表现")
    print(segment_summary(df).to_string(index=False))

    print("\n⚠️ 亏损子品类 TOP 5")
    print(loss_subcategories(df).head().to_string(index=False))

    print("\n🔍 高折扣影响")
    impact = high_discount_impact(df)
    for k, v in impact.items():
        print(f"   {k}: {v:,.2f}")

    print("\n✅ 分析完成")


if __name__ == "__main__":
    main()
