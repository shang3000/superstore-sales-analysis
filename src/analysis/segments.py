"""
区域分析函数

按 Region / State / City 聚合销售和利润，识别核心市场和亏损市场。
"""

import pandas as pd


def region_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    按区域（Region）汇总销售和利润。

    Returns
    -------
    pd.DataFrame
        列: Region, Sales, Profit, Margin, SalesShare
    """
    r = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    r['Profit Margin'] = (r['Profit'] / r['Sales'] * 100).round(2)
    r['Sales Share'] = (r['Sales'] / r['Sales'].sum() * 100).round(2)
    return r.sort_values('Sales', ascending=False)


def state_summary(df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    按州（State）汇总销售和利润。

    Parameters
    ----------
    top_n : int, optional
        仅返回销售额前 N 的州，默认返回全部

    Returns
    -------
    pd.DataFrame
        列: State, Sales, Profit, Margin
    """
    s = df.groupby('State').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    s['Profit Margin'] = (s['Profit'] / s['Sales'] * 100).round(2)
    s = s.sort_values('Sales', ascending=False)
    if top_n:
        s = s.head(top_n)
    return s


def city_summary(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    按城市（City, State）汇总销售。

    Returns
    -------
    pd.DataFrame
        列: City, State, Sales, Profit, Margin
    """
    c = df.groupby(['City', 'State']).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    c['Profit Margin'] = (c['Profit'] / c['Sales'] * 100).round(2)
    return c.sort_values('Sales', ascending=False).head(top_n)


def region_category_cross(df: pd.DataFrame) -> tuple:
    """
    区域 × 品类交叉统计。

    Returns
    -------
    (sales_pivot, profit_pivot) : tuple[pd.DataFrame, pd.DataFrame]
    """
    cross = df.groupby(['Region', 'Category']).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    ps = cross.pivot(index='Region', columns='Category', values='Sales')
    pp = cross.pivot(index='Region', columns='Category', values='Profit')
    return ps, pp
