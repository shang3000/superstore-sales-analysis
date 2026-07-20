"""
销售雷达 - Superstore Sales Analysis
项目入口脚本

使用方法：
    python main.py              # 显示帮助
    python main.py clean        # 运行数据清洗
    python main.py dashboard    # 启动仪表盘
    python main.py export       # 导出关键图表
    python main.py analysis     # 运行分析模块
    python main.py all          # 运行完整流程
"""

import sys
import subprocess
from pathlib import Path


def show_help():
    """显示帮助信息"""
    print("""
╔════════════════════════════════════════════════════════════╗
║           🎯 销售雷达 - Superstore Sales Analysis          ║
╚════════════════════════════════════════════════════════════╝

📋 可用命令：

    python main.py clean        数据清洗（原始 → 清洗后）
    python main.py dashboard    启动 Streamlit 仪表盘
    python main.py export       导出关键图表到 output/images/
    python main.py analysis     运行 src/ 分析模块并输出指标
    python main.py all          运行完整流程（清洗 + 导出 + 仪表盘）

📁 项目结构：

    data/
    ├── raw/                 原始数据
    └── processed/           清洗后数据
    notebooks/               Jupyter 分析笔记
    src/
    ├── data/                数据处理脚本
    ├── analysis/            可复用分析函数
    ├── visualization/       图表导出与绘图工具
    ├── app.py               Streamlit 仪表盘
    └── run_analysis.py      分析模块入口
    output/
    └── images/              导出的关键图表
    reports/
    └── report.md            分析报告

🚀 快速开始：

    1. 激活虚拟环境：.venv\\Scripts\\activate
    2. 安装依赖：pip install -r requirements.txt
    3. 运行清洗：python main.py clean
    4. 导出图表：python main.py export
    5. 启动仪表盘：python main.py dashboard

💡 更多信息请查看 README.md
""")


def run_clean():
    """运行数据清洗"""
    print("\n🧹 开始数据清洗...\n")
    try:
        from src.data.clean_data import main as clean_main
        clean_main()
    except Exception as e:
        print(f"\n❌ 清洗失败: {e}")
        return False
    return True


def run_dashboard():
    """启动 Streamlit 仪表盘"""
    print("\n🚀 启动仪表盘...\n")
    try:
        # 检查 streamlit 是否可用
        import streamlit
        print("✅ Streamlit 已安装")
    except ImportError:
        print("❌ Streamlit 未安装，请运行: pip install streamlit")
        return False

    # 启动 Streamlit
    app_path = Path(__file__).parent / 'src' / 'app.py'
    if not app_path.exists():
        print(f"❌ 仪表盘文件不存在: {app_path}")
        return False

    print(f"📁 仪表盘文件: {app_path}")
    print("🌐 访问地址: http://localhost:8501")
    print("🛑 按 Ctrl+C 停止服务\n")

    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', str(app_path)], check=True)
    except KeyboardInterrupt:
        print("\n👋 仪表盘已停止")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 启动失败: {e}")
        return False

    return True


def run_export():
    """导出关键图表"""
    print("\n🎨 开始导出关键图表...\n")
    script = Path(__file__).parent / 'src' / 'visualization' / 'export_charts.py'
    try:
        subprocess.run([sys.executable, str(script)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 导出失败: {e}")
        return False


def run_analysis():
    """运行分析模块"""
    print("\n📊 开始运行分析模块...\n")
    script = Path(__file__).parent / 'src' / 'run_analysis.py'
    try:
        subprocess.run([sys.executable, str(script)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 分析失败: {e}")
        return False


def run_all():
    """运行完整流程"""
    print("\n🔄 运行完整流程...\n")

    # 1. 数据清洗
    print("=" * 60)
    print("📋 步骤 1/3: 数据清洗")
    print("=" * 60)
    if not run_clean():
        return False

    # 2. 导出图表
    print("\n" + "=" * 60)
    print("📋 步骤 2/3: 导出关键图表")
    print("=" * 60)
    if not run_export():
        return False

    # 3. 启动仪表盘
    print("\n" + "=" * 60)
    print("📋 步骤 3/3: 启动仪表盘")
    print("=" * 60)
    if not run_dashboard():
        return False

    return True


def main():
    """主函数"""
    # 解析命令行参数
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command in ['clean', 'c']:
        run_clean()
    elif command in ['dashboard', 'dash', 'd', 'app']:
        run_dashboard()
    elif command in ['export', 'e', 'charts']:
        run_export()
    elif command in ['analysis', 'analyze', 'a']:
        run_analysis()
    elif command in ['all', 'full', 'f']:
        run_all()
    elif command in ['help', 'h', '--help', '-h']:
        show_help()
    else:
        print(f"\n❌ 未知命令: {command}")
        show_help()


if __name__ == "__main__":
    main()
