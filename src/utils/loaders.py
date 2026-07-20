"""
通用数据加载工具

提供标准化的数据加载函数，供 analysis 和 visualization 模块复用。
"""

import pandas as pd
from pathlib import Path


def get_project_root() -> Path:
    """从当前文件所在位置向上推导出项目根目录。"""
    # 当前文件在 src/utils/loaders.py，向上两级为项目根目录
    return Path(__file__).parent.parent.parent


def load_cleaned_data() -> pd.DataFrame:
    """
    加载清洗后的数据。

    Returns
    -------
    pd.DataFrame
        包含 'Order Date' 等标准列的 DataFrame
    """
    root = get_project_root()
    path = root / 'data' / 'processed' / 'superstore_cleaned.csv'
    df = pd.read_csv(path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df


def load_raw_data() -> pd.DataFrame:
    """
    加载原始数据（未清洗）。

    Returns
    -------
    pd.DataFrame
        原始 CSV 数据
    """
    root = get_project_root()
    path = root / 'data' / 'raw' / 'Sample-Superstore.csv'
    return pd.read_csv(path)
