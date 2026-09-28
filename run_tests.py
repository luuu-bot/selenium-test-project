"""
一键运行测试脚本
用法：python run_tests.py
"""
import os
import sys
from datetime import datetime

# 把项目根目录加入 Python 路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import pytest
from common.config import REPORT_DIR


def main():
    """运行全部测试并生成 HTML 报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(REPORT_DIR, f"test_report_{timestamp}.html")

    # pytest 参数
    args = [
        os.path.join(BASE_DIR, "tests"),   # 测试用例目录
        "-v",                               # 详细输出
        "--html=" + report_file,            # HTML 报告
        "--self-contained-html",            # 报告内嵌 CSS，独立可查看
        "-s",                               # 显示 print 输出
        "--maxfail=5",                      # 最多失败5个就停止
    ]

    print("=" * 60)
    print("  Selenium 自动化测试开始运行")
    print("=" * 60)
    print(f"  测试目录: {os.path.join(BASE_DIR, 'tests')}")
    print(f"  报告路径: {report_file}")
    print("=" * 60)

    # 运行 pytest
    exit_code = pytest.main(args)

    print("\n" + "=" * 60)
    print(f"  测试完成，退出码: {exit_code}")
    print(f"  报告已生成: {report_file}")
    print("=" * 60)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
