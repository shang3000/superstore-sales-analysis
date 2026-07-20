"""
品类分析函数

按 Category / Sub-Category 聚合销售和利润，分析折扣影响。
"""

import pandas as pd


def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    按大品类汇总。

    Returns
    -------
    pd.DataFrame
        列: Category, Sales, Profit, Margin, SalesShare
    """
    c = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    c['Profit Margin'] = (c['Profit'] / c['Sales'] * 100).round(2)
    c['Sales Share'] = (c['Sales'] / c['Sales'].sum() * 100).round(2)
    return c.sort_values('Sales', ascending=False)


def subcategory_summary(df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    按子品类汇总。

    Parameters
    ----------
    top_n : int, optional
        返回销售额前 N 的子品类

    Returns
    -------
    pd.DataFrame
        列: Category, Sub-Category, Sales, Profit, Margin
    """
    s = df.groupby(['Category', 'Sub-Category']).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    s['Profit Margin'] = (s['Profit'] / s['Sales'] * 100).round(2)
    s = s.sort_values('Sales', ascending=False)
    if top_n:
        s = s.head(top_n)
    return s


def category_discount_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    品类 × 折扣区间分析。

    Returns
    -------
    pd.DataFrame
        列: Category, Discount Range, Sales, Profit, Margin
    """
    df = df.copy()
    df['Discount Range'] = pd.cut(df['Discount'],
                                  bins=[0, 0.1, 0.2, 0.3, 0.5, 1.0],
                                  labels=['0-10%', '10-20%', '20-30%', '30-50%', '50%+'])
    d = df.groupby(['Category', 'Discount Range'], observed=True).agg(
        {'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    d['Profit Margin'] = (d['Profit'] / d['Sales'] * 100).round(2)
    return d


def loss_subcategories(df: pd.DataFrame) -> pd.DataFrame:
    """
    返回亏损子品类列表。

    Returns
    -------
    pd.DataFrame
        按亏损金额升序排列
    """
    s = df.groupby(['Category', 'Sub-Category']).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    s['Profit Margin'] = (s['Profit'] / s['Sales'] * 100).round(2)
    return s[s['Profit'] < 0].sort_values('Profit')
