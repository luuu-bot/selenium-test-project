"""
项目验证脚本 - 直接运行，验证代码是否有bug
不依赖 pytest，直接调用 BaseTest
"""
import sys
import os
import traceback

# 把项目根目录加入路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from selenium.webdriver.common.by import By

from common.base_test import BaseTest


class TestVerifier(BaseTest):
    """验证器：逐条跑用例"""

    def __init__(self):
        self.results = []  # (用例名, 是否通过, 错误信息)

    def run_case(self, name, func):
        """运行一条用例"""
        print(f"\n{'='*50}")
        print(f"  测试: {name}")
        print(f"{'='*50}")
        try:
            self.setup_method(None)
            func()
            self.teardown_method(None)
            print(f"  ✅ 通过")
            self.results.append((name, True, ""))
        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ 失败: {error_msg}")
            traceback.print_exc()
            try:
                self.save_screenshot(f"bug_{name}")
            except:
                pass
            try:
                self.teardown_method(None)
            except:
                pass
            self.results.append((name, False, error_msg))

    # ---------- 验证用例 ----------

    def case_open_baidu(self):
        """验证：打开百度首页"""
        self.open("https://www.baidu.com")
        self.assert_title_contains("百度一下")

    def case_search_box_exists(self):
        """验证：搜索框存在"""
        self.open("https://www.baidu.com")
        self.assert_element_exists(By.ID, "kw")

    def case_search_button_exists(self):
        """验证：搜索按钮存在"""
        self.open("https://www.baidu.com")
        self.assert_element_exists(By.ID, "su")

    def case_search_function(self):
        """验证：搜索功能正常"""
        self.open("https://www.baidu.com")
        self.input_text(By.ID, "kw", "selenium自动化测试")
        self.click(By.ID, "su")
        import time
        time.sleep(2)
        self.assert_title_contains("selenium自动化测试")

    def case_logo_exists(self):
        """验证：Logo存在"""
        self.open("https://www.baidu.com")
        self.assert_element_exists(By.CSS_SELECTOR, "#s_lg_img, img[title='到百度首页']")

    def case_hot_search_exists(self):
        """验证：热搜榜存在"""
        self.open("https://www.baidu.com")
        self.assert_element_exists(By.CSS_SELECTOR, "#s-hotsearch-wrapper, .hotsearch")

    def case_nav_news(self):
        """验证：新闻链接跳转"""
        self.open("https://www.baidu.com")
        self.click(By.LINK_TEXT, "新闻")
        import time
        time.sleep(2)
        self.switch_to_window(1)
        self.assert_title_contains("百度新闻")

    def case_scroll_page(self):
        """验证：页面滚动"""
        # 先打开百度首页，再搜索进入结果页（内容多才能滚动）
        self.open("https://www.baidu.com")
        self.input_text(By.ID, "kw", "软件测试面试题100道")
        self.click(By.ID, "su")
        import time
        time.sleep(2)
        self.scroll_to_bottom()
        time.sleep(1)
        scroll_pos = self.driver.execute_script("return window.pageYOffset")
        assert scroll_pos > 0, f"页面没有滚动，位置: {scroll_pos}"

    def case_input_text(self):
        """验证：输入文本功能"""
        self.open("https://www.baidu.com")
        self.input_text(By.ID, "kw", "测试输入")
        value = self.find_element(By.ID, "kw").get_attribute("value")
        assert value == "测试输入", f"输入的文本不对，实际是: {value}"

    def case_get_current_url(self):
        """验证：获取当前URL"""
        self.open("https://www.baidu.com")
        url = self.get_current_url()
        assert "baidu.com" in url, f"URL不对: {url}"

    # ---------- 汇总 ----------

    def summary(self):
        """打印汇总并写入文件"""
        total = len(self.results)
        passed = sum(1 for _, ok, _ in self.results if ok)
        failed = total - passed

        lines = []
        lines.append("="*60)
        lines.append("  验证结果汇总")
        lines.append("="*60)
        lines.append(f"  总用例数: {total}")
        lines.append(f"  通过: {passed}")
        lines.append(f"  失败: {failed}")
        lines.append(f"  通过率: {passed/total*100:.1f}%")
        lines.append("="*60)

        if failed > 0:
            lines.append("\n  失败的用例:")
            for name, ok, err in self.results:
                if not ok:
                    lines.append(f"    [FAIL] {name}")
                    lines.append(f"           原因: {err[:200]}")
        else:
            lines.append("\n  全部通过！代码没有bug！")

        lines.append("="*60)

        # 详细结果
        lines.append("\n  详细结果:")
        for i, (name, ok, err) in enumerate(self.results, 1):
            status = "PASS" if ok else "FAIL"
            lines.append(f"  {i:2d}. [{status}] {name}")
            if not ok:
                lines.append(f"       {err[:150]}")

        result_text = "\n".join(lines)
        print(result_text)

        return failed == 0


def write_result_file(result_text):
    """把验证结果写入文件，写入失败（如文件被占用）时改用带时间戳的备用文件名"""
    from datetime import datetime

    candidates = [
        os.path.join(BASE_DIR, "verify_result.txt"),
        os.path.join(
            BASE_DIR,
            f"verify_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        ),
    ]

    for result_file in candidates:
        try:
            with open(result_file, "w", encoding="utf-8") as f:
                f.write(result_text)
            print(f"\n[结果文件] {result_file}")
            return result_file
        except OSError as e:
            print(f"\n[警告] 无法写入 {result_file}: {e}，尝试备用文件名...")

    print("\n[警告] 所有结果文件均无法写入，结果仅打印到控制台")
    return None


def main():
    import io
    # 捕获所有输出到字符串
    output_buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output_buffer

    print("="*60)
    print("  Selenium 测试项目 - 代码验证")
    print("="*60)
    print("  正在逐条验证核心功能...")
    print("="*60)

    verifier = TestVerifier()

    try:
        # 运行所有验证用例
        verifier.run_case("打开百度首页", verifier.case_open_baidu)
        verifier.run_case("搜索框存在", verifier.case_search_box_exists)
        verifier.run_case("搜索按钮存在", verifier.case_search_button_exists)
        verifier.run_case("Logo存在", verifier.case_logo_exists)
        verifier.run_case("输入文本功能", verifier.case_input_text)
        verifier.run_case("获取当前URL", verifier.case_get_current_url)
        verifier.run_case("热搜榜存在", verifier.case_hot_search_exists)
        verifier.run_case("页面滚动", verifier.case_scroll_page)
        verifier.run_case("搜索功能", verifier.case_search_function)
        verifier.run_case("新闻链接跳转", verifier.case_nav_news)

        all_pass = verifier.summary()
    except Exception as e:
        print(f"\n[FATAL] 验证过程出错: {e}")
        import traceback
        traceback.print_exc()
        all_pass = False

    # 恢复输出并写入文件（只写一次，写入失败不影响退出）
    sys.stdout = old_stdout
    result_text = output_buffer.getvalue()
    write_result_file(result_text)

    # 也打印出来
    print(result_text)

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
