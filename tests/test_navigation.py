"""
测试模块2：页面导航测试
测试百度首页的导航链接、页面跳转等功能
适配说明：导航链接在新标签页打开，统一通过 open_in_new_window() 等待新窗口
出现后再切换，避免竞态；标题/URL 断言改为显式等待。
"""
import time
import pytest
from selenium.webdriver.common.by import By

from common.base_test import BaseTest


class TestNavigation(BaseTest):
    """页面导航测试类"""

    def setup_method(self, method):
        """每个测试用例前打开百度首页"""
        super().setup_method(method)
        self.open("https://www.baidu.com")

    def test_homepage_title(self):
        """TC-NAV-001：首页标题验证"""
        self.assert_title_contains("百度一下")

    def test_homepage_logo(self):
        """TC-NAV-002：首页Logo存在性验证"""
        self.assert_element_exists(By.CSS_SELECTOR, "#s_lg_img, .s_lg_img_gold_show, img[title='到百度首页']")

    def test_homepage_search_box(self):
        """TC-NAV-003：首页搜索框存在性验证（新版为 textarea#chat-textarea）"""
        self.assert_element_exists(By.CSS_SELECTOR, "#chat-textarea, #kw")

    def test_homepage_search_button(self):
        """TC-NAV-004：首页搜索按钮存在性验证（新版为 button#chat-submit-button）"""
        self.assert_element_exists(By.CSS_SELECTOR, "#chat-submit-button, #su")

    def test_nav_news_link(self):
        """TC-NAV-005：导航栏-新闻链接跳转"""
        self.open_in_new_window(By.LINK_TEXT, "新闻")
        self.assert_title_contains("百度新闻")

    def test_nav_map_link(self):
        """TC-NAV-006：导航栏-地图链接跳转"""
        self.open_in_new_window(By.LINK_TEXT, "地图")
        self.assert_title_contains("百度地图")

    def test_nav_haokan_link(self):
        """TC-NAV-007：导航栏-hao123链接跳转"""
        self.open_in_new_window(By.LINK_TEXT, "hao123")
        self.assert_url_contains("hao123.com")

    def test_nav_tieba_link(self):
        """TC-NAV-008：导航栏-贴吧链接跳转"""
        self.open_in_new_window(By.LINK_TEXT, "贴吧")
        self.assert_title_contains("贴吧")

    def test_nav_video_link(self):
        """TC-NAV-009：导航栏-视频链接跳转（新版跳转好看视频）"""
        self.open_in_new_window(By.LINK_TEXT, "视频")
        self.assert_title_contains("视频")

    def test_back_to_home(self):
        """TC-NAV-010：返回首页功能"""
        self.search("测试")
        # 点击结果页 Logo 返回首页
        self.click(By.CSS_SELECTOR, "#result_logo a, #result_logo")
        # 回到首页后新版搜索框可见
        self.find_element(By.ID, "chat-textarea")

    def test_page_refresh(self):
        """TC-NAV-011：页面刷新功能"""
        original_title = self.get_title()
        self.driver.refresh()
        assert self.get_title() == original_title

    def test_window_maximize(self):
        """TC-NAV-012：窗口最大化验证"""
        self.driver.maximize_window()
        size = self.driver.get_window_size()
        assert size["width"] > 1000
        assert size["height"] > 600
