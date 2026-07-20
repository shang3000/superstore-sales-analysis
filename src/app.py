"""
销售雷达 - Superstore Sales Dashboard
主入口文件
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="销售雷达",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS样式 ====================
st.markdown("""
<style>
    /* 全局样式 */
    .stApp {
        background: linear-gradient(135deg, #E3DAD6 0%, #EDE8E4 100%);
    }

    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #013054;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #EDE8E4;
    }

    [data-testid="stSidebar"] label {
        color: #EDE8E4 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="multi-select"] {
        background-color: #001E38;
        border-radius: 8px;
    }

    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
        background-color: #4A7A9C;
    }

    /* 标题样式 */
    h1 {
        color: #FFFFFF !important;
        font-family: 'Arial', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
        font-size: 2.5rem !important;
    }

    h2 {
        color: #013054 !important;
        font-family: 'Arial', sans-serif;
        font-weight: 600;
        font-size: 1.8rem !important;
    }

    h3 {
        color: #001E38 !important;
        font-family: 'Arial', sans-serif;
        font-weight: 600;
        font-size: 1.4rem !important;
    }

    h4 {
        color: #013054 !important;
        font-family: 'Arial', sans-serif;
        font-weight: 600;
        font-size: 1.2rem !important;
    }

    /* 指标卡片样式 */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #013054 0%, #001E38 100%);
        padding: 20px 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: none;
        transition: transform 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 2rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: #4A7A9C !important;
        font-weight: 500;
        font-size: 0.95rem !important;
    }

    [data-testid="stMetricDelta"] {
        color: #EDE8E4 !important;
    }

    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #013054 0%, #4A7A9C 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #4A7A9C 0%, #013054 100%);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-1px);
    }

    /* 下载按钮样式 */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4A7A9C 0%, #013054 100%);
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        width: 100%;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #013054 0%, #4A7A9C 100%);
    }

    /* 选择框样式 */
    .stSelectbox, .stMultiSelect {
        background-color: #EDE8E4;
        border-radius: 8px;
    }

    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #EDE8E4;
        border-radius: 8px;
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #013054;
        border-radius: 6px;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: #013054 !important;
        color: white !important;
    }

    /* 分割线 */
    hr {
        border-color: #4A7A9C;
        border-width: 1px;
        margin: 24px 0;
    }

    /* 容器样式 */
    .stPlotlyChart {
        background-color: transparent;
        border-radius: 12px;
        padding: 10px;
    }

    /* 自定义卡片容器 */
    .custom-card {
        background: #EDE8E4;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* 洞察卡片 */
    .insight-card {
        background: linear-gradient(135deg, #013054 0%, #001E38 100%);
        border-radius: 12px;
        padding: 20px;
        color: #EDE8E4;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .insight-card h4 {
        color: #4A7A9C !important;
        margin-bottom: 12px;
        font-size: 1.1rem !important;
    }

    .insight-card p {
        color: #EDE8E4;
        margin: 8px 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .insight-card strong {
        color: #FFFFFF;
    }

    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 侧边栏标题 */
    [data-testid="stSidebar"] .stMarkdown h1 {
        color: #FFFFFF !important;
        font-size: 1.8rem !important;
        margin-bottom: 10px;
    }

    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #4A7A9C !important;
        font-size: 1.2rem !important;
        margin-top: 20px;
    }

    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #EDE8E4 !important;
        font-size: 1rem !important;
    }

    /* 日期输入框样式 */
    [data-testid="stSidebar"] .stDateInput {
        background-color: #001E38;
        border-radius: 8px;
    }

    /* 侧边栏分割线 */
    [data-testid="stSidebar"] hr {
        border-color: #4A7A9C;
        margin: 15px 0;
    }

    /* 图表标题样式 */
    .stPlotlyChart h4 {
        color: #013054 !important;
        font-size: 1.1rem !important;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 数据加载 ====================
import os

@st.cache_data
def load_data():
    """加载并缓存数据"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_path = os.path.join(project_root, 'data', 'processed', 'superstore_cleaned.csv')

    df = pd.read_csv(data_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

# ==================== 侧边栏筛选器 ====================
with st.sidebar:
    st.markdown("# 🎯 销售雷达")
    st.markdown("---")
    st.markdown("## 🔍 数据筛选")

    # 日期范围筛选
    min_date = df['Order Date'].min().date()
    max_date = df['Order Date'].max().date()
    date_range = st.date_input(
        "📅 日期范围",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # 区域筛选
    regions = st.multiselect(
        "🗺️ 区域",
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )

    # 品类筛选
    categories = st.multiselect(
        "📦 品类",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )

    # 客户类型筛选
    segments = st.multiselect(
        "👥 客户类型",
        options=df['Segment'].unique(),
        default=df['Segment'].unique()
    )

    st.markdown("---")

    # 下载按钮
    filtered_df_temp = df.copy()
    if len(date_range) == 2:
        filtered_df_temp = filtered_df_temp[
            (filtered_df_temp['Order Date'].dt.date >= date_range[0]) &
            (filtered_df_temp['Order Date'].dt.date <= date_range[1])
        ]
    if regions:
        filtered_df_temp = filtered_df_temp[filtered_df_temp['Region'].isin(regions)]
    if categories:
        filtered_df_temp = filtered_df_temp[filtered_df_temp['Category'].isin(categories)]
    if segments:
        filtered_df_temp = filtered_df_temp[filtered_df_temp['Segment'].isin(segments)]

    csv = filtered_df_temp.to_csv(index=False)
    st.download_button(
        label="📥 下载数据",
        data=csv,
        file_name=f"superstore_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==================== 数据筛选 ====================
filtered_df = df.copy()

# 日期筛选
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['Order Date'].dt.date >= date_range[0]) &
        (filtered_df['Order Date'].dt.date <= date_range[1])
    ]

# 区域筛选
if regions:
    filtered_df = filtered_df[filtered_df['Region'].isin(regions)]

# 品类筛选
if categories:
    filtered_df = filtered_df[filtered_df['Category'].isin(categories)]

# 客户类型筛选
if segments:
    filtered_df = filtered_df[filtered_df['Segment'].isin(segments)]

# ==================== 主页面 ====================
st.markdown("""
<div style='display: flex; align-items: center; gap: 15px; margin-bottom: 10px;'>
    <span style='font-size: 3rem;'>🎯</span>
    <div>
        <h1 style='margin: 0; padding: 0; font-size: 3rem; color: #013054 !important;'>
            <span style='color: #013054;'>销售</span><span style='color: #4A7A9C;'>雷达</span>
        </h1>
        <p style='margin: 5px 0 0 0; color: #001E38; font-size: 1.2rem; font-weight: 500;'>
            Superstore Sales Analysis Dashboard
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== 核心指标卡片 ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_df['Sales'].sum()
    st.metric(
        label="💰 总销售额",
        value=f"${total_sales:,.0f}"
    )

with col2:
    total_profit = filtered_df['Profit'].sum()
    st.metric(
        label="📈 总利润",
        value=f"${total_profit:,.0f}"
    )

with col3:
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    st.metric(
        label="📊 利润率",
        value=f"{profit_margin:.1f}%"
    )

with col4:
    total_orders = filtered_df['Order ID'].nunique()
    st.metric(
        label="📋 订单数",
        value=f"{total_orders:,}"
    )

st.markdown("---")

# ==================== 图表区域 ====================
# 第一行：趋势 + 地图
col_left, col_right = st.columns([3, 2])

# ---------- 图表1：月度销售趋势 ----------
with col_left:
    st.markdown("#### 📈 月度销售趋势")

    # 图表切换
    chart_type = st.selectbox(
        "选择指标",
        options=["销售额", "利润", "订单量"],
        key="trend_chart",
        label_visibility="collapsed"
    )

    # 按月聚合
    monthly_data = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    monthly_data['Order Date'] = monthly_data['Order Date'].dt.to_timestamp()
    monthly_data['Month'] = monthly_data['Order Date'].dt.strftime('%Y-%m')

    # 创建图表
    if chart_type == "销售额":
        fig_trend = px.area(
            monthly_data,
            x='Month',
            y='Sales',
            color_discrete_sequence=['#013054']
        )
        fig_trend.update_traces(line=dict(width=3), fillcolor='rgba(1, 48, 84, 0.2)')
    elif chart_type == "利润":
        fig_trend = px.bar(
            monthly_data,
            x='Month',
            y='Profit',
            color_discrete_sequence=['#4A7A9C']
        )
    else:
        fig_trend = px.bar(
            monthly_data,
            x='Month',
            y='Order ID',
            color_discrete_sequence=['#001E38']
        )

    fig_trend.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#013054'),
        xaxis=dict(gridcolor='#E3DAD6', showgrid=True),
        yaxis=dict(gridcolor='#E3DAD6', showgrid=True),
        height=350,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# ---------- 图表2：区域销售地图 ----------
with col_right:
    st.markdown("#### 🗺️ 区域销售地图")

    # 地图指标切换
    map_metric = st.selectbox(
        "选择指标",
        options=["销售额", "利润率"],
        key="map_metric",
        label_visibility="collapsed"
    )

    # 按区域聚合
    region_data = filtered_df.groupby('State').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    region_data['Profit Margin'] = (region_data['Profit'] / region_data['Sales'] * 100).round(2)

    # 创建地图
    if map_metric == "销售额":
        fig_map = px.choropleth(
            region_data,
            locations='State',
            locationmode='USA-states',
            color='Sales',
            scope='usa',
            hover_data=['Sales', 'Profit', 'Profit Margin'],
            color_continuous_scale=['#EDE8E4', '#4A7A9C', '#013054']
        )
    else:
        fig_map = px.choropleth(
            region_data,
            locations='State',
            locationmode='USA-states',
            color='Profit Margin',
            scope='usa',
            hover_data=['Sales', 'Profit', 'Profit Margin'],
            color_continuous_scale=['#C73E1D', '#EDE8E4', '#013054']
        )

    fig_map.update_layout(
        geo=dict(
            lakecolor='rgb(255, 255, 255)',
            bgcolor='rgba(0,0,0,0)',
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_colorbar=dict(
            title=dict(font=dict(color='#013054')),
            tickfont=dict(color='#013054')
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)

# 第二行：品类 + 客户
col_left2, col_right2 = st.columns(2)

# ---------- 图表3：品类销售占比 ----------
with col_left2:
    st.markdown("#### 📦 品类销售占比")

    # 品类图表切换
    cat_chart_type = st.selectbox(
        "图表类型",
        options=["旭日图", "饼图", "柱状图"],
        key="cat_chart",
        label_visibility="collapsed"
    )

    # 按品类聚合
    category_data = filtered_df.groupby(['Category', 'Sub-Category']).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()

    category_colors = {
        'Technology': '#013054',
        'Furniture': '#4A7A9C',
        'Office Supplies': '#001E38'
    }

    if cat_chart_type == "旭日图":
        fig_cat = px.sunburst(
            category_data,
            path=['Category', 'Sub-Category'],
            values='Sales',
            color='Category',
            color_discrete_map=category_colors
        )
    elif cat_chart_type == "饼图":
        category_total = filtered_df.groupby('Category').agg({
            'Sales': 'sum'
        }).reset_index()

        fig_cat = px.pie(
            category_total,
            values='Sales',
            names='Category',
            color='Category',
            color_discrete_map=category_colors,
            hole=0.4
        )
    else:
        subcat_data = filtered_df.groupby(['Category', 'Sub-Category']).agg({
            'Sales': 'sum'
        }).reset_index().sort_values('Sales', ascending=True)

        fig_cat = px.bar(
            subcat_data,
            x='Sales',
            y='Sub-Category',
            color='Category',
            color_discrete_map=category_colors,
            orientation='h'
        )

    fig_cat.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#013054'),
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ---------- 图表4：客户类型分析 ----------
with col_right2:
    st.markdown("#### 👥 客户类型分析")

    # 客户图表切换
    cust_chart_type = st.selectbox(
        "选择指标",
        options=["销售额", "利润率", "客单价"],
        key="cust_chart",
        label_visibility="collapsed"
    )

    # 按客户类型聚合
    segment_data = filtered_df.groupby('Segment').agg({
        'Sales': ['sum', 'mean'],
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    segment_data.columns = ['Segment', 'Total Sales', 'Avg Sales', 'Total Profit', 'Orders']
    segment_data['Profit Margin'] = (segment_data['Total Profit'] / segment_data['Total Sales'] * 100).round(2)
    segment_data['Avg Order Value'] = (segment_data['Total Sales'] / segment_data['Orders']).round(2)

    segment_colors = ['#013054', '#4A7A9C', '#001E38']

    if cust_chart_type == "销售额":
        fig_cust = px.bar(
            segment_data,
            x='Segment',
            y='Total Sales',
            color='Segment',
            color_discrete_sequence=segment_colors,
            text_auto='.2s'
        )
    elif cust_chart_type == "利润率":
        fig_cust = px.bar(
            segment_data,
            x='Segment',
            y='Profit Margin',
            color='Segment',
            color_discrete_sequence=segment_colors,
            text_auto='.1f'
        )
        fig_cust.add_hline(
            y=segment_data['Profit Margin'].mean(),
            line_dash="dash",
            line_color="#C73E1D",
            annotation_text="平均利润率",
            annotation_position="top right"
        )
    else:
        fig_cust = px.bar(
            segment_data,
            x='Segment',
            y='Avg Order Value',
            color='Segment',
            color_discrete_sequence=segment_colors,
            text_auto='$.0f'
        )

    fig_cust.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#013054'),
        showlegend=False,
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor='#E3DAD6'),
        yaxis=dict(gridcolor='#E3DAD6')
    )
    st.plotly_chart(fig_cust, use_container_width=True)

# ==================== 深度洞察 ====================
st.markdown("---")
st.markdown("## 🔍 深度洞察")

col_insight, col_scatter = st.columns([1, 2])

with col_insight:
    # 计算关键指标
    total_sales_ins = filtered_df['Sales'].sum()
    total_profit_ins = filtered_df['Profit'].sum()
    profit_margin_ins = (total_profit_ins / total_sales_ins * 100) if total_sales_ins > 0 else 0

    # 亏损分析
    loss_orders = filtered_df[filtered_df['Profit'] < 0]
    loss_amount = loss_orders['Profit'].sum()

    # 高折扣分析
    high_discount = filtered_df[filtered_df['Discount'] > 0.3]
    high_discount_loss = high_discount[high_discount['Profit'] < 0]['Profit'].sum()

    # 最佳/最差
    best_region = filtered_df.groupby('Region')['Profit'].sum().idxmax()
    worst_region = filtered_df.groupby('Region')['Profit'].sum().idxmin()
    best_category = filtered_df.groupby('Category')['Profit'].sum().idxmax()

    # 展示洞察
    st.markdown(f"""
    <div class="insight-card">
        <h4>🎯 核心发现</h4>
        <p>• 整体利润率: <strong>{profit_margin_ins:.1f}%</strong></p>
        <p>• 亏损订单占比: <strong>{len(loss_orders)/len(filtered_df)*100:.1f}%</strong></p>
        <p>• 高折扣导致亏损: <strong>${abs(high_discount_loss):,.0f}</strong></p>
        <p>• 最佳区域: <strong>{best_region}</strong></p>
        <p>• 最差区域: <strong>{worst_region}</strong></p>
        <p>• 最佳品类: <strong>{best_category}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">
        <h4>💡 业务建议</h4>
        <p>1. 折扣策略: 控制折扣在20%以内</p>
        <p>2. 品类优化: 提升低利润品类盈利能力</p>
        <p>3. 区域策略: 优化{worst_region}区域定价</p>
        <p>4. 产品推广: 加大高利润产品推广</p>
    </div>
    """, unsafe_allow_html=True)

with col_scatter:
    st.markdown("#### 📉 折扣 vs 利润关系")

    fig_scatter = px.scatter(
        filtered_df,
        x='Discount',
        y='Profit',
        color='Category',
        size='Sales',
        color_discrete_map={
            'Technology': '#013054',
            'Furniture': '#4A7A9C',
            'Office Supplies': '#001E38'
        },
        hover_data=['Product Name', 'Sales', 'Profit'],
        opacity=0.7
    )
    fig_scatter.add_hline(y=0, line_dash="dash", line_color="#C73E1D", opacity=0.5)
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#013054'),
        height=400,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor='#E3DAD6', title='折扣率'),
        yaxis=dict(gridcolor='#E3DAD6', title='利润 ($)'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ==================== 页脚 ====================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #4A7A9C; padding: 20px; font-size: 0.9rem;'>
        <p style='margin: 0;'>🎯 销售雷达 - Superstore Sales Analysis Dashboard</p>
        <p style='margin: 5px 0 0 0;'>Built with Streamlit & Plotly | Data: Sample Superstore</p>
    </div>
    """,
    unsafe_allow_html=True
)
