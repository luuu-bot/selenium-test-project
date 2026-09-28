"""
pytest 配置文件
- 失败自动截图
- 测试报告配置
- 自定义命令行参数
"""
import os
import pytest
from datetime import datetime

from common.config import REPORT_DIR, SCREENSHOT_DIR


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    每个测试用例执行后的钩子函数
    用例失败时自动截图并嵌入 HTML 报告
    """
    outcome = yield
    rep = outcome.get_result()

    # setup 或 call 阶段失败都截图（setup 失败时 driver 可能尚未初始化，需容错）
    if rep.when in ("setup", "call") and rep.failed:
        driver = None
        try:
            if hasattr(item, "instance") and hasattr(item.instance, "driver"):
                driver = item.instance.driver
        except Exception:
            driver = None

        if driver:
            try:
                # 截图
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"fail_{item.name}_{timestamp}.png"
                screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
                driver.save_screenshot(screenshot_path)
                print(f"\n[失败截图] {screenshot_path}")

                # 将截图嵌入 pytest-html 报告（通过 extras 机制）
                try:
                    import pytest_html.extras
                    extra = getattr(rep, "extra", [])
                    extra.append(pytest_html.extras.image(screenshot_path))
                    rep.extra = extra
                except ImportError:
                    # 未安装 pytest-html 时只保存截图，不嵌入报告
                    pass
            except Exception as e:
                print(f"\n[警告] 截图失败: {e}")


def pytest_configure(config):
    """pytest 启动时的配置"""
    # 确保报告和截图目录存在
    os.makedirs(REPORT_DIR, exist_ok=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    # 给用例打标记
    config.addinivalue_line("markers", "smoke: 冒烟测试用例")
    config.addinivalue_line("markers", "regression: 回归测试用例")
    config.addinivalue_line("markers", "search: 搜索功能测试")
    config.addinivalue_line("markers", "navigation: 导航功能测试")


def pytest_html_report_title(report):
    """自定义 HTML 报告标题"""
    report.title = "Selenium 自动化测试报告"
