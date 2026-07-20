"""
销售趋势分析函数

按月、季度、年聚合销售额、利润、订单量，支持时间序列分析复用。
"""

import pandas as pd


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    按月聚合销售趋势。

    Returns
    -------
    pd.DataFrame
        列: Month(YYYY-MM), Sales, Profit, Orders
    """
    monthly = df.groupby(df['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    monthly['Order Date'] = monthly['Order Date'].dt.to_timestamp()
    monthly['Month'] = monthly['Order Date'].dt.strftime('%Y-%m')
    monthly = monthly.rename(columns={'Order ID': 'Orders'})
    return monthly


def yearly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    按年聚合销售趋势。

    Returns
    -------
    pd.DataFrame
        列: Order Year, Sales, Profit, Orders
    """
    yearly = df.groupby('Order Year').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index().rename(columns={'Order ID': 'Orders'})
    return yearly


def seasonal_pattern(df: pd.DataFrame) -> pd.DataFrame:
    """
    按月份分析季节性（多年平均）。

    Returns
    -------
    pd.DataFrame
        列: Order Month, Sales, Profit, Orders
    """
    pattern = df.groupby('Order Month').agg({
        'Sales': 'mean',
        'Profit': 'mean',
        'Order ID': 'nunique'
    }).reset_index().rename(columns={'Order ID': 'Orders'})
    return pattern


def day_of_week_pattern(df: pd.DataFrame) -> pd.DataFrame:
    """
    按星期分析销售分布。

    Returns
    -------
    pd.DataFrame
        列: Day, Total Sales, Avg Sales, Orders
    """
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow = df.groupby('Order Day of Week').agg({
        'Sales': ['sum', 'mean'],
        'Order ID': 'nunique'
    }).reset_index()
    dow.columns = ['Day', 'Total Sales', 'Avg Sales', 'Orders']
    dow['Day'] = pd.Categorical(dow['Day'], categories=day_order, ordered=True)
    dow = dow.sort_values('Day')
    return dow


def kpi_summary(df: pd.DataFrame) -> dict:
    """
    计算核心 KPI。

    Returns
    -------
    dict
        总销售额、总利润、利润率、订单数、客户数、平均客单价
    """
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique()
    total_customers = df['Customer ID'].nunique()
    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'profit_margin': total_profit / total_sales * 100,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'avg_order_value': total_sales / total_orders,
    }
