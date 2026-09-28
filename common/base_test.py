"""
测试基类：封装浏览器的启动、关闭、截图等公共操作
所有测试类都继承这个基类
"""
import os
import time
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.config import (
    BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT,
    WINDOW_SIZE, SCREENSHOT_DIR, BASE_URL
)


class BaseTest:
    """测试基类"""

    driver = None
    wait = None

    def setup_method(self, method):
        """每个测试用例执行前的准备工作：启动浏览器"""
        self._init_driver()
        self.driver.maximize_window()
        self.driver.implicitly_wait(IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        self.wait = WebDriverWait(self.driver, IMPLICIT_WAIT)

    def teardown_method(self, method):
        """每个测试用例执行后的清理工作：截图+关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def _init_driver(self):
        """初始化浏览器驱动"""
        if BROWSER.lower() == "chrome":
            options = Options()
            if HEADLESS:
                options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(f"--window-size={WINDOW_SIZE}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            self.driver = webdriver.Chrome(options=options)

            # 去掉 webdriver 标识，防止被检测
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
            )
        else:
            raise ValueError(f"不支持的浏览器类型: {BROWSER}")

    def open(self, url=""):
        """打开页面，支持相对路径，并等待页面加载完成"""
        if url.startswith("http"):
            self.driver.get(url)
        else:
            self.driver.get(BASE_URL + url)
        # 等待页面加载完成
        self._wait_page_ready()
        # 尝试关闭可能的弹窗（隐私协议等）
        self._try_close_popup()

    def _try_close_popup(self):
        """尝试关闭页面上可能出现的弹窗/遮罩"""
        popup_selectors = [
            "#isAgreeWrapper",         # 百度隐私协议
            ".popup-bottom-close",     # 底部弹窗关闭
            ".mask-close",             # 遮罩关闭
            ".close-btn",              # 通用关闭按钮
        ]
        for selector in popup_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and elements[0].is_displayed():
                    elements[0].click()
                    time.sleep(0.3)
            except Exception:
                pass

    def _wait_page_ready(self, timeout=None):
        """等待页面加载完成（document.readyState == complete）"""
        if timeout is None:
            timeout = PAGE_LOAD_TIMEOUT
        end_time = time.time() + timeout
        while time.time() < end_time:
            ready_state = self.driver.execute_script("return document.readyState")
            if ready_state == "complete":
                # 额外等一小会儿，让动态内容渲染
                time.sleep(0.5)
                return True
            time.sleep(0.2)
        return False

    def find_element(self, by, value):
        """查找单个元素（显式等待可见）

        使用 visibility_of_any_elements_located：当页面存在多个同定位器元素
        （如新版百度首页同时有隐藏的旧版 #kw 和新版 #chat-textarea）时，
        返回第一个"可见"的元素，避免隐藏元素导致的误超时。
        """
        elements = self.wait.until(
            EC.visibility_of_any_elements_located((by, value))
        )
        return elements[0]

    def find_elements(self, by, value):
        """查找多个元素"""
        self.wait.until(EC.presence_of_element_located((by, value)))
        return self.driver.find_elements(by, value)

    def click(self, by, value):
        """点击元素（显式等待任意匹配元素可见且可点击）"""
        element = self.wait.until(
            lambda d: next(
                (e for e in d.find_elements(by, value)
                 if e.is_displayed() and e.is_enabled()),
                False,
            )
        )
        element.click()

    def input_text(self, by, value, text):
        """输入文本"""
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def search(self, keyword):
        """在百度首页执行搜索（兼容新版 AI 搜索框与旧版输入框）

        新版首页的可见搜索框是 textarea#chat-textarea，旧版 input#kw 已被
        隐藏折叠（0x0），因此优先使用新版搜索框 + 回车提交，
        回车无效时回退为点击"百度一下"按钮。
        """
        from selenium.webdriver.common.keys import Keys

        try:
            box = self.find_element(By.ID, "chat-textarea")
        except Exception:
            box = self.find_element(By.ID, "kw")
        box.send_keys(keyword)
        box.send_keys(Keys.ENTER)
        # 回车未生效时（仍在首页），点击"百度一下"按钮兜底
        if "百度一下" in (self.driver.title or ""):
            try:
                self.click(By.CSS_SELECTOR, "#chat-submit-button, #su")
            except Exception:
                pass

    def get_title(self):
        """获取页面标题"""
        return self.driver.title

    def get_current_url(self):
        """获取当前页面URL（页面渲染繁忙时自动重试）"""
        import time as _time
        last_err = None
        for _ in range(3):
            try:
                return self.driver.current_url
            except Exception as e:
                last_err = e
                _time.sleep(1)
        raise last_err

    def assert_title_contains(self, expected):
        """断言标题包含预期内容（显式等待，避免页面未加载完就断言）"""
        try:
            self.wait.until(EC.title_contains(expected))
        except Exception:
            actual = self.driver.title
            raise AssertionError(
                f"页面标题 '{actual}' 不包含 '{expected}'（等待超时）"
            )

    def assert_url_contains(self, expected):
        """断言URL包含预期内容（显式等待 + 渲染超时重试）

        部分页面（如 hao123）加载重、渲染器响应慢，current_url 读取可能
        连续超时，因此等待上限使用页面加载超时时间（30秒）。
        """
        url_wait = WebDriverWait(self.driver, PAGE_LOAD_TIMEOUT)

        def _url_contains(d):
            try:
                return expected in d.current_url
            except Exception:
                return False  # 渲染器超时等瞬时错误，继续轮询

        try:
            url_wait.until(_url_contains)
        except Exception:
            actual = self.get_current_url()
            raise AssertionError(
                f"URL '{actual}' 不包含 '{expected}'（等待超时）"
            )

    def assert_element_exists(self, by, value):
        """断言元素存在"""
        elements = self.driver.find_elements(by, value)
        assert len(elements) > 0, f"元素不存在: {by}={value}"

    def assert_text_in_element(self, by, value, expected_text):
        """断言元素文本包含预期内容"""
        actual = self.find_element(by, value).text
        assert expected_text in actual, f"元素文本 '{actual}' 不包含 '{expected_text}'"

    def save_screenshot(self, name=None):
        """截图保存"""
        if not name:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(SCREENSHOT_DIR, f"{name}.png")
        self.driver.save_screenshot(filename)
        return filename

    def switch_to_window(self, index=1):
        """切换到第N个窗口（0是第一个，1是第二个，以此类推）"""
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[index])

    def open_in_new_window(self, by, value):
        """点击元素打开新窗口并自动切换过去（等待新窗口出现，避免竞态）"""
        old_handles = set(self.driver.window_handles)
        self.click(by, value)
        self.wait.until(lambda d: len(set(d.window_handles) - old_handles) > 0)
        new_handle = (set(self.driver.window_handles) - old_handles).pop()
        self.driver.switch_to.window(new_handle)

    def click_and_follow(self, by, value):
        """点击元素并跟随跳转：无论目标在新标签页还是当前页，都切换到位

        某些链接的打开方式不稳定（同一入口有时当前页跳转、有时新标签页），
        统一等待"新窗口出现或当前页URL变化"后再继续。
        """
        old_handles = set(self.driver.window_handles)
        old_url = self.driver.current_url
        self.click(by, value)

        def _navigated(d):
            if len(set(d.window_handles) - old_handles) > 0:
                return "new"
            try:
                if d.current_url != old_url:
                    return "same"
            except Exception:
                pass  # 渲染器繁忙时读取URL可能超时，继续轮询
            return False

        result = self.wait.until(_navigated)
        if result == "new":
            self.driver.switch_to.window(self.driver.window_handles[-1])

    def scroll_to_bottom(self):
        """滚动到页面底部"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_element(self, by, value):
        """滚动到指定元素"""
        element = self.find_element(by, value)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def accept_alert(self):
        """接受弹窗"""
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()

    def dismiss_alert(self):
        """取消弹窗"""
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.dismiss()
