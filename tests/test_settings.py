"""
测试模块3：设置功能测试
测试百度的设置下拉菜单、搜索设置等功能
适配说明：新版设置下拉菜单为 #s-user-setting-menu（旧版 .bdpfmenu 已隐藏），
搜索设置/高级搜索以页面内弹窗（.pfpanel-bd）形式呈现，不再跳转新页面。
"""
import re
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from common.base_test import BaseTest


class TestSettings(BaseTest):
    """设置功能测试类"""

    def setup_method(self, method):
        """每个测试用例前打开百度首页"""
        super().setup_method(method)
        self.open("https://www.baidu.com")

    def _open_settings_menu(self):
        """悬停"设置"并等待下拉菜单出现，返回菜单元素"""
        settings_link = self.find_element(By.ID, "s-usersetting-top")
        ActionChains(self.driver).move_to_element(settings_link).perform()
        return self.find_element(By.ID, "s-user-setting-menu")

    def _click_menu_item(self, text):
        """打开设置菜单并点击指定菜单项"""
        menu = self._open_settings_menu()
        for item in menu.find_elements(By.TAG_NAME, "a"):
            if item.text.strip() == text:
                item.click()
                return
        raise AssertionError(f"设置菜单中未找到菜单项: {text}")

    def test_settings_menu_appear(self):
        """TC-SET-001：设置下拉菜单显示"""
        menu = self._open_settings_menu()
        assert menu.is_displayed(), "设置下拉菜单未显示"

    def test_settings_options_count(self):
        """TC-SET-002：设置菜单项数量"""
        menu = self._open_settings_menu()
        menu_items = menu.find_elements(By.TAG_NAME, "a")
        assert len(menu_items) >= 3, f"设置菜单项数量不足，实际为 {len(menu_items)}"

    def test_search_settings_page(self):
        """TC-SET-003：搜索设置弹窗打开"""
        self._click_menu_item("搜索设置")
        # 新版以页面内弹窗呈现
        self.assert_element_exists(By.CSS_SELECTOR, ".pfpanel-bd, .prefs-setting, .setting-panel")

    def test_advanced_search_page(self):
        """TC-SET-004：高级搜索弹窗打开"""
        self._click_menu_item("高级搜索")
        # 新版高级搜索为页面内弹窗，标题不再变化
        panel = self.find_element(By.CSS_SELECTOR, ".pfpanel-bd, .prefs-setting, .setting-panel")
        assert "高级搜索" in panel.text, f"弹窗内容不包含'高级搜索'，实际为: {panel.text[:50]}"

    def test_about_baidu_link(self):
        """TC-SET-005：关于百度链接"""
        self.scroll_to_bottom()
        time.sleep(1)
        self.open_in_new_window(By.LINK_TEXT, "关于百度")
        self.assert_title_contains("关于百度")

    def test_footer_links_exist(self):
        """TC-SET-006：底部链接存在性验证"""
        self.scroll_to_bottom()
        time.sleep(1)
        footer_links = self.find_elements(By.CSS_SELECTOR, "#bottom_layer a, #ftCon a")
        assert len(footer_links) > 5, f"底部链接数量不足，实际为 {len(footer_links)}"

    def test_hot_search_list(self):
        """TC-SET-007：热搜榜存在性验证"""
        self.assert_element_exists(By.CSS_SELECTOR, "#s-hotsearch-wrapper, .hotsearch")

    def test_hot_search_click(self):
        """TC-SET-008：点击热搜榜条目"""
        hot_items = self.find_elements(By.CSS_SELECTOR, "#s-hotsearch-wrapper a, .hotsearch-item")
        # 过滤出可见且有真实文本的条目（排除图标、换一换等零尺寸/私有字体图标链接）
        clickable = []
        for item in hot_items:
            try:
                text = item.text.strip()
                if item.is_displayed() and item.size["width"] > 50 and len(text) > 4:
                    clickable.append(item)
            except Exception:
                continue
        if not clickable:
            pytest.skip("未找到可点击的热搜榜条目")

        first_hot = clickable[0]
        # 清除私有字体图标字符（\ue000-\uf8ff），如热搜条目前的火焰图标
        hot_text = re.sub(r"[\ue000-\uf8ff]", "", first_hot.text).strip()
        keyword = hot_text.split("\n")[0][:4]
        first_hot.click()
        # 热搜条目在新标签页打开搜索结果
        if len(self.driver.window_handles) > 1:
            self.switch_to_window(len(self.driver.window_handles) - 1)
        self.assert_title_contains(keyword)

    def test_more_products(self):
        """TC-SET-009：更多产品入口"""
        # "更多"的打开方式不稳定（当前页跳转或新标签页），统一跟随跳转
        self.click_and_follow(By.NAME, "tj_briicon")
        # 跳转百度产品大全页
        self.assert_title_contains("百度产品大全")

    def test_page_scroll(self):
        """TC-SET-010：页面滚动功能"""
        # 先搜索关键词，进入结果页（内容多，有滚动条）
        self.search("软件测试面试题100道")
        time.sleep(1)
        # 滚动到底部
        self.scroll_to_bottom()
        time.sleep(1)
        scroll_position = self.driver.execute_script("return window.pageYOffset")
        assert scroll_position > 0, f"页面没有滚动，滚动位置: {scroll_position}"
