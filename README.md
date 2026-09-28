# Selenium 自动化测试项目

基于 Selenium + Pytest 的 Web UI 自动化测试框架，以百度首页为测试对象，覆盖搜索、导航、设置三大功能模块，共 30+ 条测试用例，支持自动生成 HTML 测试报告和失败截图。

## 📋 项目简介

这是一个面向软件测试学习和简历展示的自动化测试项目，采用企业级测试框架的设计思路，代码结构清晰，可扩展性强。

### 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.x | 开发语言 |
| Selenium | 4.x | Web UI 自动化框架 |
| Pytest | 7.x+ | 测试执行框架 |
| pytest-html | 3.x+ | HTML 测试报告生成 |
| Chrome | 最新版 | 测试浏览器 |

### 项目特点

- ✅ **结构清晰**：测试用例、公共模块、配置分离
- ✅ **断言丰富**：标题断言、元素断言、文本断言、URL断言
- ✅ **失败截图**：用例失败自动截图保存
- ✅ **HTML 报告**：自动生成可视化测试报告
- ✅ **显式等待**：封装 WebDriverWait，稳定可靠
- ✅ **易于扩展**：BaseTest 基类，新增用例只需继承

## 📁 项目结构

```
selenium-test-project/
├── tests/                      # 测试用例目录
│   ├── __init__.py
│   ├── test_search.py          # 搜索功能测试（10条）
│   ├── test_navigation.py      # 导航功能测试（12条）
│   └── test_settings.py        # 设置功能测试（10条）
├── common/                     # 公共模块
│   ├── __init__.py
│   ├── base_test.py            # 测试基类（封装Selenium操作）
│   └── config.py               # 全局配置
├── reports/                    # 测试报告输出目录
├── screenshots/                # 失败截图目录
├── conftest.py                 # pytest 配置（钩子函数）
├── run_tests.py                # 一键运行脚本
├── requirements.txt            # 依赖清单
├── testcases.md                # 测试用例设计文档
└── README.md                   # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Chrome 浏览器（最新版）
- Windows / macOS / Linux

### 安装步骤

1. **克隆项目**
```bash
git clone <项目地址>
cd selenium-test-project
```

2. **安装依赖**（推荐使用项目自带 venv，bat 脚本已默认调用 venv）
```bash
venv\Scripts\pip install -r requirements.txt
```

> Selenium 4.6+ 内置了 Selenium Manager，会自动下载匹配的 ChromeDriver，无需手动配置。

3. **运行测试**

方式一：一键运行脚本
```bash
python run_tests.py
```

方式二：直接用 pytest
```bash
pytest tests/ -v --html=reports/report.html --self-contained-html
```

方式三：运行指定模块
```bash
pytest tests/test_search.py -v           # 只跑搜索测试
pytest tests/test_navigation.py -v       # 只跑导航测试
```

4. **查看报告**

测试完成后，在 `reports/` 目录下找到最新的 HTML 报告，用浏览器打开即可查看。

## 🧪 测试模块说明

### 1. 搜索功能测试 (test_search.py)
- 正常关键词搜索
- 英文/中文关键词搜索
- 回车键搜索
- 搜索结果数量验证
- 搜索建议下拉框
- 空关键词搜索（反向）
- 特殊字符搜索（边界）
- 超长关键词搜索（边界）

### 2. 导航功能测试 (test_navigation.py)
- 首页标题验证
- Logo / 搜索框 / 按钮存在性
- 新闻、地图、hao123、贴吧、视频链接跳转
- 返回首页
- 页面刷新
- 窗口大小

### 3. 设置功能测试 (test_settings.py)
- 设置下拉菜单
- 搜索设置页面
- 高级搜索页面
- 关于百度链接
- 底部链接验证
- 热搜榜功能
- 更多产品菜单
- 页面滚动

## 📊 测试报告

运行测试后会生成 HTML 格式的测试报告，包含以下内容：

- 📈 测试概览（总数、通过、失败、跳过、通过率）
- ⏱️ 每个用例的执行时间
- ❌ 失败用例的错误详情和堆栈信息
- 🖼️ 失败用例自动截图
- 📂 按模块分类展示

## 🔧 框架设计

### BaseTest 基类

封装了所有常用的 Selenium 操作，测试类继承后直接使用：

| 方法 | 说明 |
|------|------|
| `open(url)` | 打开页面 |
| `find_element(by, value)` | 查找元素（显式等待） |
| `click(by, value)` | 点击元素 |
| `input_text(by, value, text)` | 输入文本 |
| `get_title()` | 获取标题 |
| `assert_title_contains(expected)` | 断言标题 |
| `save_screenshot(name)` | 截图 |
| `switch_to_window(index)` | 切换窗口 |
| `scroll_to_bottom()` | 滚动到底部 |

### 等待策略

- **隐式等待**：全局 10 秒，元素查找时自动等待
- **显式等待**：关键操作使用 WebDriverWait 等待条件满足
- 避免使用 `time.sleep()`，提高执行效率和稳定性

## 📝 测试用例设计

详细的测试用例设计文档请参考 [testcases.md](testcases.md)。

用例设计方法：
- 等价类划分法
- 边界值分析法
- 场景法
- 错误推测法

## ⚠️ 被测页面适配说明

百度首页改版后部分元素与旧版不同，框架已做兼容：

| 功能 | 旧版元素（已隐藏） | 新版元素（当前使用） |
|------|-------------------|---------------------|
| 搜索输入框 | `input#kw`（0×0 隐藏） | `textarea#chat-textarea` |
| 搜索按钮 | `input#su`（0×0 隐藏） | `button#chat-submit-button` |
| 设置下拉菜单 | `.bdpfmenu` | `#s-user-setting-menu` |
| 搜索设置/高级搜索 | 独立页面 | 页面内弹窗 `.pfpanel-bd` |
| 视频导航链接 | 百度视频 | 好看视频（haokan.baidu.com） |

BaseTest 中的等待策略使用 `visibility_of_any_elements_located`，可在新旧元素并存时自动选中可见元素。

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

## 📄 License

MIT License

---

> 💡 **说明**：本项目仅用于学习和测试目的，测试对象为百度首页，请勿用于商业用途或高频访问。
