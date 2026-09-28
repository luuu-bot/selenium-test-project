"""
全局配置文件
"""
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 测试网站（使用练习专用网站，稳定可靠）
BASE_URL = "https://www.baidu.com"

# 浏览器配置
BROWSER = "chrome"           # 浏览器类型：chrome / firefox / edge
HEADLESS = False             # 是否无头模式（不显示浏览器窗口）
IMPLICIT_WAIT = 10           # 隐式等待时间（秒）
PAGE_LOAD_TIMEOUT = 30       # 页面加载超时时间（秒）

# 窗口大小
WINDOW_SIZE = "1366,768"     # 浏览器窗口大小

# 报告和截图路径
REPORT_DIR = os.path.join(BASE_DIR, "reports")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")

# 确保目录存在
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
