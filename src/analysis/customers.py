"""
客户分析函数

按 Segment / 单个客户聚合，支持 RFM 分析。
"""

import pandas as pd


def segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    按客户类型（Segment）汇总。

    Returns
    -------
    pd.DataFrame
        列: Segment, Sales, Profit, Margin, Orders, Customers, AOV
    """
    s = df.groupby('Segment').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique',
        'Customer ID': 'nunique'
    }).reset_index()
    s = s.rename(columns={'Order ID': 'Orders', 'Customer ID': 'Customers'})
    s['Profit Margin'] = (s['Profit'] / s['Sales'] * 100).round(2)
    s['Sales Share'] = (s['Sales'] / s['Sales'].sum() * 100).round(2)
    s['AOV'] = (s['Sales'] / s['Orders']).round(2)
    return s.sort_values('Sales', ascending=False)


def segment_category_cross(df: pd.DataFrame) -> tuple:
    """
    客户类型 × 品类交叉统计。

    Returns
    -------
    (sales_pivot, profit_pivot) : tuple[pd.DataFrame, pd.DataFrame]
    """
    cross = df.groupby(['Segment', 'Category']).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    ps = cross.pivot(index='Segment', columns='Category', values='Sales')
    pp = cross.pivot(index='Segment', columns='Category', values='Profit')
    return ps, pp


def top_customers(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    按客户汇总消费额。

    Returns
    -------
    pd.DataFrame
        列: Customer ID, Customer Name, Segment, Sales, Profit, Orders
    """
    c = df.groupby(['Customer ID', 'Customer Name', 'Segment']).agg(
        {'Sales': 'sum', 'Profit': 'sum', 'Order ID': 'nunique'}).reset_index()
    c = c.rename(columns={'Order ID': 'Orders'})
    c['Profit Margin'] = (c['Profit'] / c['Sales'] * 100).round(2)
    return c.sort_values('Sales', ascending=False).head(top_n)


def rfm_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    简化版 RFM 分析。

    Returns
    -------
    pd.DataFrame
        列: Customer ID, Recency, Frequency, Monetary, R_Score, F_Score, M_Score
    """
    reference_date = df['Order Date'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('Customer ID').agg({
        'Order Date': lambda x: (reference_date - x.max()).days,
        'Order ID': 'nunique',
        'Sales': 'sum'
    }).reset_index()
    rfm.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary']
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
    return rfm
