"""
通用图表绘制工具

封装 matplotlib / seaborn 的常用图表，减少 analysis 模块和 notebook 中的重复代码。
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from pathlib import Path
import numpy as np


YAHEI_PATH = Path('C:/Windows/Fonts/msyh.ttc')
SIMHEI_PATH = Path('C:/Windows/Fonts/simhei.ttf')


def setup_font():
    """配置字体和图表风格。"""
    if YAHEI_PATH.exists():
        fm.fontManager.addfont(str(YAHEI_PATH))
    if SIMHEI_PATH.exists():
        fm.fontManager.addfont(str(SIMHEI_PATH))
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    sns.set_style('whitegrid')


def setup_axes(ax, title: str, xlabel: str = None, ylabel: str = None):
    """统一设置标题和轴标签。"""
    ax.set_title(title, fontsize=14, fontweight='bold')
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)


def horizontal_bar_with_labels(ax, labels, values, color, title, xlabel, fmt='{:.0f}'):
    """
    绘制水平条形图，并在右侧标注数值。

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    labels : array-like
    values : array-like
    color : str or list
    title : str
    xlabel : str
    fmt : str
        数值格式字符串
    """
    bars = ax.barh(labels, values, color=color, edgecolor='white', linewidth=0.5)
    setup_axes(ax, title, xlabel)
    ax.bar_label(bars, fmt=fmt, fontsize=9)


def pie_chart(ax, values, labels, colors, title):
    """绘制饼图。"""
    ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors,
           startangle=90, textprops={'fontsize': 11})
    ax.set_title(title, fontsize=14, fontweight='bold')


def heatmap_pair(axes, df1, df2, title1, title2, cmap1='YlOrRd', cmap2='RdYlGn'):
    """
    并排放置两个热力图。

    Parameters
    ----------
    axes : list[Axes]
    df1, df2 : pd.DataFrame
    """
    sns.heatmap(df1, annot=True, fmt='.0f', cmap=cmap1, ax=axes[0])
    setup_axes(axes[0], title1)

    sns.heatmap(df2, annot=True, fmt='.0f', cmap=cmap2, ax=axes[1])
    setup_axes(axes[1], title2)


def value_in_millions(x):
    """将数值转换为 $x.xM 格式。"""
    return f'${x/1e6:.1f}M'


def value_in_thousands(x):
    """将数值转换为 $xK 格式。"""
    return f'${x/1e3:.0f}K'
