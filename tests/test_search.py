"""
测试模块1：搜索功能测试
测试百度首页的搜索功能
适配说明：新版百度首页可见搜索框为 textarea#chat-textarea（旧版 input#kw 已隐藏），
搜索统一通过 BaseTest.search() 辅助方法执行。
"""
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from common.base_test import BaseTest


class TestSearch(BaseTest):
    """搜索功能测试类"""

    def setup_method(self, method):
        """每个测试用例前打开百度首页"""
        super().setup_method(method)
        self.open("https://www.baidu.com")

    # ---------- 正向用例 ----------

    def test_search_normal_keyword(self):
        """TC-SRCH-001：正常关键词搜索"""
        self.search("selenium自动化测试")
        self.assert_title_contains("selenium自动化测试")
        self.assert_element_exists(By.ID, "content_left")

    def test_search_english_keyword(self):
        """TC-SRCH-002：英文关键词搜索"""
        self.search("python pytest")
        self.assert_title_contains("python pytest")

    def test_search_chinese_keyword(self):
        """TC-SRCH-003：中文关键词搜索"""
        self.search("软件测试工程师")
        self.assert_title_contains("软件测试工程师")

    def test_search_enter_key(self):
        """TC-SRCH-004：按回车键搜索"""
        search_box = self.find_element(By.ID, "chat-textarea")
        search_box.send_keys("自动化测试")
        search_box.send_keys(Keys.ENTER)
        self.assert_title_contains("自动化测试")

    def test_search_result_count(self):
        """TC-SRCH-005：搜索结果数量验证"""
        self.search("pytest")
        # 验证搜索结果容器存在且有结果
        results = self.find_elements(By.CSS_SELECTOR, "#content_left .result")
        assert len(results) > 0, "搜索结果数量为0"

    def test_search_suggestion(self):
        """TC-SRCH-006：搜索建议下拉框"""
        self.input_text(By.ID, "chat-textarea", "selenium")
        # 等待下拉框出现（新版为 .ai-bdsug / #normalSugSearchUl）
        suggestions = self.find_elements(
            By.CSS_SELECTOR,
            ".ai-bdsug li, .bdsug li, #normalSugSearchUl li"
        )
        assert len(suggestions) > 0, "搜索建议下拉框没有出现"

    # ---------- 反向/边界用例 ----------

    def test_search_empty_keyword(self):
        """TC-SRCH-007：空关键词搜索（应停留在首页）"""
        self.click(By.CSS_SELECTOR, "#chat-submit-button, #su")
        # 空搜索应仍在首页或显示提示
        title = self.get_title()
        assert "百度" in title

    def test_search_special_characters(self):
        """TC-SRCH-008：特殊字符搜索"""
        self.search("!@#$%^&*()")
        # 特殊字符搜索也应该返回页面
        self.assert_element_exists(By.ID, "content_left")

    def test_search_long_keyword(self):
        """TC-SRCH-009：超长关键词搜索"""
        long_keyword = "测试" * 50  # 100字
        self.search(long_keyword)
        # 超长关键词也应该返回结果页
        self.assert_element_exists(By.ID, "content_left")

    def test_search_url_in_title(self):
        """TC-SRCH-010：搜索后URL包含搜索参数"""
        self.search("软件测试")
        self.assert_url_contains("wd=")
