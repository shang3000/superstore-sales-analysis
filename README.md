# 🎯 销售雷达 - Superstore 数据分析项目

一个完整的零售销售数据分析项目，包含数据清洗、探索性分析和交互式仪表盘。

## 📊 项目概览

| 指标 | 数值 |
|------|------|
| 数据量 | 9,994 行 × 21 列 |
| 时间范围 | 2014-01-03 ~ 2017-12-30 |
| 总销售额 | $2,297,201 |
| 总利润 | $286,397 |
| 利润率 | 12.47% |

## 📁 项目结构

```
superstore-sales-analysis/
├── data/
│   ├── raw/                    # 原始数据
│   │   └── Sample-Superstore.csv
│   └── processed/              # 清洗后数据
├── notebooks/                  # Jupyter 分析笔记
│   ├── 01_销售趋势分析.ipynb
│   ├── 02_区域分析.ipynb
│   ├── 03_品类分析.ipynb
│   ├── 04_客户分析.ipynb
│   └── 05_深度洞察.ipynb
├── src/
│   └── app.py                  # Streamlit 仪表盘
├── reports/                    # 生成的报告
├── start.bat                   # 启动脚本（Windows）
├── requirements.txt            # Python 依赖
└── README.md
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd superstore-sales-analysis
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv .venv
   ```

3. **激活虚拟环境**
   ```bash
   # Windows
   .venv\Scripts\activate

   # Mac/Linux
   source .venv/bin/activate
   ```

4. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

5. **启动仪表盘**
   ```bash
   # Windows - 双击 start.bat
   # 或命令行
   streamlit run src/app.py
   ```

6. **访问**
   打开浏览器访问 http://localhost:8501

## 📈 分析模块

### 01 销售趋势分析
- 月度/季度/年度销售趋势
- 季节性分析
- 同比环比增长

### 02 区域分析
- 全国销售地图
- Top 10 州/城市排名
- 区域利润率对比

### 03 品类分析
- 产品类别占比
- 子类别利润贡献
- 盈利/亏损产品识别

### 04 客户分析
- 客户分层（Consumer/Corporate/Home Office）
- RFM 模型分析
- 客户价值评估

### 05 深度洞察
- 折扣与利润相关性
- 异常值检测
- 关键业务发现

## 🎨 仪表盘特性

- **交互式筛选器**：日期范围、区域、品类、客户类型
- **实时更新**：选择筛选条件后图表自动刷新
- **数据下载**：支持下载筛选后的数据
- **响应式设计**：适配不同屏幕尺寸

## 🔍 关键发现

1. **区域表现**：西部区域最佳（31.6% 份额，14.9% 利润率）
2. **品类差异**：Technology 利润率最高（17.4%），Furniture 最低（2.5%）
3. **折扣陷阱**：折扣超过 30% 会导致亏损
4. **客户结构**：Consumer 占比 50.6%，但利润率最低

## 🛠️ 技术栈

- **数据处理**：Pandas, NumPy
- **可视化**：Plotly, Matplotlib, Seaborn
- **仪表盘**：Streamlit
- **开发环境**：Jupyter Notebook

## 📝 License

MIT License

## 👤 作者

**不如吃茶去** (Izumi)
- 大连海事大学 | 大数据管理与应用
- Python 爱好者 | 数据可视化

---

⭐ 如果这个项目对你有帮助，请给个 Star！
