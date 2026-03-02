# 🤖 API-AutoTest: 问答机器人接口自动化测试框架 (V3.0)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-stable-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

> 一款专为 AI 问答机器人设计的接口自动化测试工具，专注于验证 AI 生成的 SQL 语句的准确性与业务逻辑。
> **V3.0 版本已针对鉴权稳定性、网络防风控及复杂 JSON 解析进行了深度优化。**

---

## 🌟 核心特性 (V3.0)

- 🔐 **API 直连鉴权** - 支持 "账号登录 -> Ticket -> Token" 完整链路，自动处理 Token 刷新。
- 🛡️ **深度网络伪装** - 自动禁用系统代理，模拟真实浏览器 Header (`Referer`/`UA`)，通过服务器风控。
- 🌊 **SSE 流式解析** - 完美支持 `Server-Sent Events` 协议，实时解析 AI 响应流。
- 🔍 **智能 SQL 提取** - 支持从嵌套 JSON 及 **字符串值** (`"sql: SELECT..."`) 中提取 SQL。
- 🎯 **多维模糊校验** - 支持关键字与条件片段的灵活匹配，自动容错单双引号与换行符。
- 🚀 **批量并发执行** - 基于 `ThreadPoolExecutor` 的并发控制，支持从 Excel 读取海量用例。
- 📊 **可视化报告** - 自动生成带样式的 Excel 测试报告，结果一目了然。

---

## 🏗️ 项目架构

```mermaid
graph TD
    A[run_batch_test.py 批量入口] --> B[AuthManager 鉴权中心]
    A --> C[Excel 用例加载]
    A --> D[ThreadPoolExecutor 并发执行]
    D --> E[APIRunner 业务请求]
    E --> F[SSE 流解析/SQL提取]
    D --> G[Validator 结果校验]
    G --> H[Reporter 报告生成]
    H --> I[data/output/report_result.xlsx]
```

---

## 📂 目录结构

```text
d:\apiautotest\
├── src/                    # 核心源码
│   ├── auth.py             # 登录鉴权逻辑 (含 Ticket 换 Token)
│   ├── api_runner.py       # 业务接口交互 (SSE + SQL递归提取)
│   ├── validator.py        # SQL 准确性匹配引擎
│   ├── reporter.py         # Excel 报告生成工具
│   └── config.py           # 全局环境配置
├── data/                   # 数据文件
│   ├── input/              # 测试用例 (如 test_3_cases.xlsx)
│   └── output/             # 测试报告 (Excel)
├── run_batch_test.py       # 【推荐】批量测试启动入口
├── main.py                 # 旧版入口 (保留)
├── requirements.txt        # 依赖包清单
└── 修改记录_V3.0.md        # 版本更新详细记录
```

---

## 🚀 快速开始

### 1. 环境准备
确保已安装 Python 3.8+，执行以下命令安装依赖：
```bash
pip install -r requirements.txt
```

### 2. 参数配置
编辑 `src/config.py` 确认测试数据路径：
```python
# 指定测试用例文件
INPUT_FILE = r"D:\apiautotest\data\input\test_3_cases.xlsx"

# 登录账号配置
LOGIN_ACCOUNT = "13439427048"
# ...
```

### 3. 运行批量测试
使用 V3.0 新增的批量测试脚本：
```powershell
python run_batch_test.py
```

### 4. 查看报告
测试结束后，报告将生成于：`D:\apiautotest\data\output\report_result.xlsx`

---

## 📝 V3.0 稳定性改进说明

针对之前版本出现的“无法获取数据”、“鉴权失败”等问题，V3.0 进行了以下关键修复：

1.  **网络层优化**：显式禁用了 `requests` 的系统代理设置，防止请求被本地代理 (如 Charles/Fiddler) 拦截导致超时。
2.  **Header 修正**：严格对齐了浏览器行为，特别是 `Referer` 字段补充了 `web-dashboard` 路径，防止被服务端拦截。
3.  **SQL 解析增强**：不仅支持标准的 JSON 字段提取，还增加了对 **字符串内嵌 SQL** (如 `sql: SELECT...`) 的解析支持，解决了部分场景下无法提取 SQL 的问题。

---

## 🔗 常见问题

- **Q: 为什么提示 'no such table'？**
  - A: 这是业务系统的正常返回，说明 SQL 语法正确但表不存在。**只要提取到了 SQL，测试框架即视为“成功获取”**。断言失败是因为预期关键字不匹配。
- **Q: 登录超时怎么办？**
  - A: 检查网络是否正常，或在 config.py 中增加 `LOGIN_TIMEOUT`。

---

## 🛠️ 技术栈
- **HTTP Client**: [requests](https://requests.readthedocs.io/)
- **Concurrency**: [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- **Data Engine**: [pandas](https://pandas.pydata.org/)
