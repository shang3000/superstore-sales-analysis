"""
Export key charts to output/images/

Extracts the most representative charts from 5 notebooks and exports as PNG.
These charts are used in README, reports, and project showcases.

Usage:
    python src/visualization/export_charts.py

Output:
    output/images/01_monthly_sales_trend.png
    output/images/02_yearly_comparison.png
    output/images/03_region_analysis.png
    output/images/04_region_category_heatmap.png
    output/images/05_subcategory_profit.png
    output/images/06_customer_segment.png
    output/images/07_discount_profit.png
    output/images/08_loss_analysis.png
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np
from pathlib import Path

# Load Chinese font for Windows
YAHEI_PATH = Path('C:/Windows/Fonts/msyh.ttc')
SIMHEI_PATH = Path('C:/Windows/Fonts/simhei.ttf')

def _init_chinese_font():
    """Initialize Chinese font for matplotlib Agg backend."""
    if YAHEI_PATH.exists():
        fm.fontManager.addfont(str(YAHEI_PATH))
    if SIMHEI_PATH.exists():
        fm.fontManager.addfont(str(SIMHEI_PATH))
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    sns.set_style('whitegrid')


COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'danger': '#C73E1D',
    'success': '#27AE60',
    'category': {'Furniture': '#2E86AB', 'Office Supplies': '#A23B72', 'Technology': '#F18F01'},
    'region': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'],
    'segment': ['#2E86AB', '#A23B72', '#F18F01'],
}


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def load_data() -> pd.DataFrame:
    root = get_project_root()
    df = pd.read_csv(root / 'data' / 'processed' / 'superstore_cleaned.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df


def chart_01(df, out):
    """Monthly sales trend + order volume."""
    m = df.groupby(df['Order Date'].dt.to_period('M')).agg(
        {'Sales': 'sum', 'Order ID': 'nunique'}).reset_index()
    m['Date'] = m['Order Date'].dt.to_timestamp()
    m['Label'] = m['Date'].dt.strftime('%Y-%m')

    fig, ax1 = plt.subplots(figsize=(14, 5))
    ax1.fill_between(range(len(m)), m['Sales'], alpha=0.3, color=COLORS['primary'])
    ax1.plot(range(len(m)), m['Sales'], color=COLORS['primary'], lw=2, label='Sales')
    ax1.set_ylabel('Sales ($)', fontsize=12)
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_xticks(range(0, len(m), 6))
    ax1.set_xticklabels(m['Label'].iloc[::6], fontsize=9)
    ax1.set_title('Monthly Sales Trend (2014-2017)', fontsize=14, fontweight='bold')

    ax2 = ax1.twinx()
    ax2.bar(range(len(m)), m['Order ID'], alpha=0.3, color=COLORS['secondary'], width=0.8, label='Orders')
    ax2.set_ylabel('Orders', fontsize=12)

    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.95))
    plt.tight_layout()
    plt.savefig(out / '01_monthly_sales_trend.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ 01_monthly_sales_trend.png")


def chart_02(df, out):
    """Yearly sales & profit comparison."""
    y = df.groupby('Order Year').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    def _m(x):
        return f'${x/1e6:.1f}M'

    b1 = axes[0].bar(y['Order Year'].astype(int), y['Sales'], color=COLORS['primary'], edgecolor='white', lw=1.5)
    axes[0].set_title('Annual Sales', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Sales ($)')
    axes[0].set_xticks(y['Order Year'].astype(int))
    axes[0].bar_label(b1, labels=[_m(v) for v in y['Sales']], fontsize=10)

    b2 = axes[1].bar(y['Order Year'].astype(int), y['Profit'], color=COLORS['secondary'], edgecolor='white', lw=1.5)
    axes[1].set_title('Annual Profit', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Profit ($)')
    axes[1].set_xticks(y['Order Year'].astype(int))
    axes[1].bar_label(b2, labels=[_m(v) for v in y['Profit']], fontsize=10)

    plt.tight_layout()
    plt.savefig(out / '02_yearly_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ 02_yearly_comparison.png")


def chart_03(df, out):
    """Region sales share, profit margin, top 10 states."""
    r = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    r['Margin'] = (r['Profit'] / r['Sales'] * 100).round(2)
    r = r.sort_values('Sales', ascending=False)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    axes[0].pie(r['Sales'], labels=r['Region'], autopct='%1.1f%%',
                colors=COLORS['region'], startangle=90, textprops={'fontsize': 11})
    axes[0].set_title('Sales by Region', fontsize=14, fontweight='bold')

    b = axes[1].barh(r['Region'], r['Margin'], color=COLORS['region'], edgecolor='white', lw=1.5)
    axes[1].set_xlabel('Profit Margin (%)')
    axes[1].set_title('Profit Margin by Region', fontsize=14, fontweight='bold')
    axes[1].bar_label(b, fmt='%.1f%%', fontsize=10)

    s = df.groupby('State').agg({'Sales': 'sum'}).reset_index().sort_values('Sales', ascending=False).head(10)
    cmap = plt.cm.viridis(np.linspace(0.3, 0.9, 10))
    b = axes[2].barh(s['State'].iloc[::-1], s['Sales'].iloc[::-1], color=cmap, edgecolor='white', lw=0.5)
    axes[2].set_xlabel('Sales ($)')
    axes[2].set_title('Top 10 States', fontsize=14, fontweight='bold')
    axes[2].bar_label(b, labels=[f'${v/1e3:.0f}K' for v in s['Sales'].iloc[::-1]], fontsize=9)

    plt.tight_layout()
    plt.savefig(out / '03_region_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ 03_region_analysis.png")


def chart_04(df, out):
    """Region x Category heatmap (sales & profit)."""
    cross = df.groupby(['Region', 'Category']).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    ps = cross.pivot(index='Region', columns='Category', values='Sales')
    pp = cross.pivot(index='Region', columns='Category', values='Profit')

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.heatmap(ps, annot=True, fmt='.0f', cmap='YlOrRd', ax=axes[0])
    axes[0].set_title('Region x Category: Sales', fontsize=14, fontweight='bold')

    sns.heatmap(pp, annot=True, fmt='.0f', cmap='RdYlGn', ax=axes[1])
    axes[1].set_title('Region x Category: Profit', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(out / '04_region_category_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ 04_region_category_heatmap.png")


def chart_05(df, out):
    """Sub-category sales and profit margin."""
    sc = df.groupby(['Category', 'Sub-Category']).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    sc['Margin'] = (sc['Profit'] / sc['Sales'] * 100).round(2)
    sc = sc.sort_values('Sales', ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    top15 = sc.head(15)
    bc = [COLORS['category'].get(c, '#888') for c in top15['Category']]
    b = axes[0].barh(top15['Sub-Category'].iloc[::-1], top15['Sales'].iloc[::-1],
                     color=bc[::-1], edgecolor='white', lw=0.5)
    axes[0].set_xlabel('Sales ($)')
    axes[0].set_title('Top 15 Sub-Categories: Sales', fontsize=14, fontweight='bold')
    axes[0].bar_label(b, labels=[f'${v/1e3:.0f}K' for v in top15['Sales'].iloc[::-1]], fontsize=9)

    mc = [COLORS['primary'] if x > 0 else COLORS['danger'] for x in sc['Margin'].iloc[::-1]]
    b = axes[1].barh(sc['Sub-Category'].iloc[::-1], sc['Margin'].iloc[::-1],
                     color=mc, edgecolor='white', lw=0.5)
    axes[1].set_xlabel('Profit Margin (%)')
    axes[1].set_title('Sub-Category Profit Margin', fontsize=14, fontweight='bold')
    axes[1].axvline(x=0, color='red', ls='--', lw=1, alpha=0.5)
    axes[1].bar_label(b, fmt='%.1f%%', fontsize=8)

    from matplotlib.patches import Patch
    legend = [Patch(facecolor=COLORS['category'][c], label=c) for c in COLORS['category']]
    axes[0].legend(handles=legend, loc='lower right')

    plt.tight_layout()
    plt.savefig(out / '05_subcategory_profit.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ 05_subcategory_profit.png")


def chart_06(df, out):
    """Customer segment analysis."""
    seg = df.groupby('Segment').agg({
        'Sales': ['sum', 'mean'], 'Profit': ['sum', 'mean'],
        'Order ID': 'nunique', 'Customer ID': 'nunique'}).reset_index()
    seg.columns = ['Segment', 'TotalSales', 'AvgSales', 'TotalProfit', 'AvgProfit', 'Orders', 'Customers']
    seg['Margin'] = (seg['TotalProfit'] / seg['TotalSales'] * 100).round(2)
    seg['AOV'] = (seg['TotalSales'] / seg['Orders']).round(2)
    seg = seg.sort_values('TotalSales', ascending=False)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    axes[0].pie(seg['TotalSales'], labels=seg['Segment'], autopct='%1.1f%%',
                colors=COLORS['segment'], startangle=90, textprops={'fontsize': 11})
    axes[0].set_title('Sales by Segment', fontsize=14, fontweight='bold')

    b = axes[1].barh(seg['Segment'], seg['Margin'], color=COLORS['segment'], edgecolor='white', lw=1.5)
    axes[1].set_xlabel('Profit Margin (%)')
    axes[1].set_title('Profit Margin by Segment', fontsize=14, fontweight='bold')
    axes[1].bar_label(b, fmt='%.1f%%', fontsize=10)

    b = axes[2].barh(seg['Segment'], seg['AOV'], color=COLORS['segment'], edgecolor='white', lw=1.5)
    axes[2].set_xlabel('Avg Order Value ($)')
    axes[2].set_title('Avg Order Value by Segment', fontsize=14, fontweight='bold')
    axes[2].bar_label(b, fmt='$%.0f', fontsize=10)

    plt.tight_layout()
    plt.savefig(out / '06_customer_segment.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ 06_customer_segment.png")


def chart_07(df, out):
    """Discount vs profit relationship."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sc = axes[0].scatter(df['Discount'], df['Profit'], c=df['Sales'], cmap='YlOrRd', alpha=0.5, s=20)
    axes[0].axhline(y=0, color='red', ls='--', lw=1, alpha=0.5)
    axes[0].set_xlabel('Discount Rate', fontsize=12)
    axes[0].set_ylabel('Profit ($)', fontsize=12)
    axes[0].set_title('Profit vs Discount', fontsize=14, fontweight='bold')
    plt.colorbar(sc, ax=axes[0], label='Sales ($)')

    df2 = df.copy()
    df2['DiscRange'] = pd.cut(df2['Discount'], bins=[0, 0.1, 0.2, 0.3, 0.5, 1.0],
                               labels=['0-10%', '10-20%', '20-30%', '30-50%', '50%+'])
    dp = df2.groupby('DiscRange', observed=True).agg({'Profit': 'mean'}).reset_index()
    bc = [COLORS['primary'] if x > 0 else COLORS['danger'] for x in dp['Profit']]
    b = axes[1].bar(dp['DiscRange'], dp['Profit'], color=bc, edgecolor='white', lw=1.5)
    axes[1].axhline(y=0, color='red', ls='--', lw=1, alpha=0.5)
    axes[1].set_xlabel('Discount Range', fontsize=12)
    axes[1].set_ylabel('Avg Profit ($)', fontsize=12)
    axes[1].set_title('Avg Profit by Discount Range', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(out / '07_discount_profit.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ 07_discount_profit.png")


def chart_08(df, out):
    """Loss analysis across dimensions."""
    loss = df[df['Profit'] < 0]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    lc = loss.groupby('Category').agg({'Profit': 'sum'}).reset_index().sort_values('Profit')
    b = axes[0, 0].barh(lc['Category'], lc['Profit'], color=COLORS['danger'], edgecolor='white')
    axes[0, 0].set_title('Loss by Category', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Loss ($)')
    axes[0, 0].bar_label(b, fmt='$%.0fK', fontsize=9)

    lr = loss.groupby('Region').agg({'Profit': 'sum'}).reset_index().sort_values('Profit')
    b = axes[0, 1].barh(lr['Region'], lr['Profit'], color=COLORS['danger'], edgecolor='white')
    axes[0, 1].set_title('Loss by Region', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Loss ($)')
    axes[0, 1].bar_label(b, fmt='$%.0fK', fontsize=9)

    ls = loss.groupby('Segment').agg({'Profit': 'sum'}).reset_index().sort_values('Profit')
    b = axes[1, 0].barh(ls['Segment'], ls['Profit'], color=COLORS['danger'], edgecolor='white')
    axes[1, 0].set_title('Loss by Segment', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Loss ($)')
    axes[1, 0].bar_label(b, fmt='$%.0fK', fontsize=9)

    lsc = loss.groupby('Sub-Category').agg({'Profit': 'sum'}).reset_index().sort_values('Profit')
    bc = [COLORS['danger'] if x < -1000 else COLORS['accent'] for x in lsc['Profit']]
    b = axes[1, 1].barh(lsc['Sub-Category'], lsc['Profit'], color=bc, edgecolor='white')
    axes[1, 1].set_title('Loss by Sub-Category', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Loss ($)')
    axes[1, 1].axvline(x=0, color='black', ls='-', lw=1)

    plt.tight_layout()
    plt.savefig(out / '08_loss_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ 08_loss_analysis.png")


def main():
    """Export all charts."""
    _init_chinese_font()

    root = get_project_root()
    out = root / 'output' / 'images'
    out.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("📊 Superstore Key Charts Export")
    print("=" * 60)

    print("\n📥 Loading data...")
    df = load_data()
    print(f"   Records: {len(df)}")

    print("\n🎨 Exporting charts...")
    chart_01(df, out)
    chart_02(df, out)
    chart_03(df, out)
    chart_04(df, out)
    chart_05(df, out)
    chart_06(df, out)
    chart_07(df, out)
    chart_08(df, out)

    print(f"\n✅ All charts exported to: {out}")
    print("=" * 60)


if __name__ == "__main__":
    main()
