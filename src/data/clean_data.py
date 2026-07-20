"""
数据清洗脚本
原始数据 → 清洗后数据

使用方法：
    python src/data/clean_data.py

输入：data/raw/Sample-Superstore.csv
输出：data/processed/superstore_cleaned.csv
"""

import pandas as pd
import os
from pathlib import Path


def get_project_root() -> Path:
    """获取项目根目录"""
    # 当前文件在 src/data/clean_data.py，向上两级到项目根
    return Path(__file__).parent.parent.parent


def load_raw_data(file_path: str, encodings: list = None) -> pd.DataFrame:
    """
    加载原始 CSV 文件（支持多编码自动检测）

    Parameters
    ----------
    file_path : str
        CSV 文件路径
    encodings : list, optional
        尝试的编码列表，默认 ['utf-8', 'latin-1', 'gbk', 'iso-8859-1']

    Returns
    -------
    pd.DataFrame
        加载的数据框
    """
    if encodings is None:
        encodings = ['utf-8', 'latin-1', 'gbk', 'iso-8859-1']

    for enc in encodings:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            print(f"✅ 成功使用编码 {enc} 加载数据")
            return df
        except UnicodeDecodeError:
            continue

    raise ValueError(f"❌ 无法识别文件编码: {file_path}")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    数据清洗

    Steps:
    1. 删除重复行
    2. 处理缺失值
    3. 转换数据类型
    4. 特征工程

    Parameters
    ----------
    df : pd.DataFrame
        原始数据

    Returns
    -------
    pd.DataFrame
        清洗后的数据
    """
    print("\n📋 开始数据清洗...")
    print(f"   原始数据: {df.shape[0]} 行 × {df.shape[1]} 列")

    # 1. 删除重复行
    initial_rows = len(df)
    df = df.drop_duplicates()
    removed_rows = initial_rows - len(df)
    if removed_rows > 0:
        print(f"   ✅ 删除重复行: {removed_rows} 行")
    else:
        print("   ✅ 无重复行")

    # 2. 处理缺失值
    missing = df.isnull().sum()
    if missing.any():
        print(f"   ⚠️ 缺失值统计:")
        for col in missing[missing > 0].index:
            print(f"      - {col}: {missing[col]} 行 ({missing[col]/len(df)*100:.2f}%)")
        # 对于数值列用中位数填充，分类列用众数填充
        for col in df.columns:
            if df[col].isnull().any():
                if df[col].dtype in ['int64', 'float64']:
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
        print("   ✅ 缺失值已处理")
    else:
        print("   ✅ 无缺失值")

    # 3. 转换日期列
    date_columns = ['Order Date', 'Ship Date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
            print(f"   ✅ 日期转换: {col}")

    # 4. 特征工程
    print("\n🔧 特征工程...")

    # 时间特征
    if 'Order Date' in df.columns:
        df['Order Year'] = df['Order Date'].dt.year
        df['Order Month'] = df['Order Date'].dt.month
        df['Order Quarter'] = df['Order Date'].dt.quarter
        df['Order Day of Week'] = df['Order Date'].dt.day_name()
        print("   ✅ 时间特征: Year, Month, Quarter, Day of Week")

    # 计算运输天数
    if 'Order Date' in df.columns and 'Ship Date' in df.columns:
        df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
        print("   ✅ 运输天数: Shipping Days")

    # 计算利润率（如果有 Sales 和 Profit）
    if 'Sales' in df.columns and 'Profit' in df.columns:
        df['Profit Margin'] = (df['Profit'] / df['Sales'] * 100).round(2)
        print("   ✅ 利润率: Profit Margin")

    print(f"\n📋 清洗完成: {df.shape[0]} 行 × {df.shape[1]} 列")

    return df


def main():
    """主函数"""
    # 获取项目根目录
    root = get_project_root()

    # 文件路径
    input_file = root / 'data' / 'raw' / 'Sample-Superstore.csv'
    output_file = root / 'data' / 'processed' / 'superstore_cleaned.csv'

    print("=" * 60)
    print("🧹 Superstore 数据清洗脚本")
    print("=" * 60)
    print(f"\n📁 输入文件: {input_file}")
    print(f"📁 输出文件: {output_file}")

    # 检查输入文件是否存在
    if not input_file.exists():
        print(f"\n❌ 错误: 输入文件不存在 - {input_file}")
        return

    # 加载数据
    print("\n📥 加载原始数据...")
    df = load_raw_data(str(input_file))
    print(f"   数据形状: {df.shape[0]} 行 × {df.shape[1]} 列")

    # 数据清洗
    df_cleaned = clean_data(df)

    # 保存清洗后的数据
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n💾 已保存到: {output_file}")

    # 输出数据概览
    print("\n📊 数据概览:")
    print(f"   - 时间范围: {df_cleaned['Order Date'].min().date()} ~ {df_cleaned['Order Date'].max().date()}")
    print(f"   - 总销售额: ${df_cleaned['Sales'].sum():,.2f}")
    print(f"   - 总利润: ${df_cleaned['Profit'].sum():,.2f}")
    print(f"   - 利润率: {df_cleaned['Profit'].sum()/df_cleaned['Sales'].sum()*100:.2f}%")

    print("\n" + "=" * 60)
    print("✅ 清洗完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
