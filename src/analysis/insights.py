"""
深度洞察函数

分析折扣、利润、亏损之间的关系，输出业务建议相关的指标。
"""

import pandas as pd


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    关键数值字段的相关性矩阵。

    Returns
    -------
    pd.DataFrame
        Sales, Quantity, Discount, Profit 的相关性
    """
    return df[['Sales', 'Quantity', 'Discount', 'Profit']].corr().round(3)


def discount_profit_by_range(df: pd.DataFrame) -> pd.DataFrame:
    """
    按折扣区间统计平均利润。

    Returns
    -------
    pd.DataFrame
        列: Discount Range, Sales, Profit, Avg Profit
    """
    df = df.copy()
    df['Discount Range'] = pd.cut(df['Discount'],
                                  bins=[0, 0.1, 0.2, 0.3, 0.5, 1.0],
                                  labels=['0-10%', '10-20%', '20-30%', '30-50%', '50%+'])
    d = df.groupby('Discount Range', observed=True).agg(
        {'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    d['Avg Profit'] = (d['Profit'] / df.groupby('Discount Range', observed=True).size().values).round(2)
    return d


def loss_orders_summary(df: pd.DataFrame) -> dict:
    """
    亏损订单统计。

    Returns
    -------
    dict
        盈利/亏损订单数、金额、平均利润等
    """
    profit = df[df['Profit'] >= 0]
    loss = df[df['Profit'] < 0]
    return {
        'profit_count': len(profit),
        'loss_count': len(loss),
        'profit_pct': len(profit) / len(df) * 100,
        'loss_pct': len(loss) / len(df) * 100,
        'total_profit': profit['Profit'].sum(),
        'total_loss': loss['Profit'].sum(),
        'avg_profit': profit['Profit'].mean(),
        'avg_loss': loss['Profit'].mean(),
    }


def loss_by_dimension(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """
    按指定维度统计亏损。

    Parameters
    ----------
    dimension : str
        如 'Category', 'Region', 'Segment', 'Sub-Category'

    Returns
    -------
    pd.DataFrame
        按亏损金额升序排列
    """
    loss = df[df['Profit'] < 0]
    g = loss.groupby(dimension).agg({'Profit': 'sum'}).reset_index()
    return g.sort_values('Profit')


def high_discount_impact(df: pd.DataFrame, threshold: float = 0.3) -> dict:
    """
    高折扣（> threshold）订单的影响。

    Returns
    -------
    dict
        订单数、销售额、利润、利润率等
    """
    hd = df[df['Discount'] > threshold]
    hd_loss = hd[hd['Profit'] < 0]
    return {
        'count': len(hd),
        'pct': len(hd) / len(df) * 100,
        'sales': hd['Sales'].sum(),
        'profit': hd['Profit'].sum(),
        'profit_margin': hd['Profit'].sum() / hd['Sales'].sum() * 100 if hd['Sales'].sum() else 0,
        'loss_amount': hd_loss['Profit'].sum(),
    }
