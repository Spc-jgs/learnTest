# Python 学习路径与阶段规划

这份规划基于当前仓库里的学习文件整理：

- `tuple_list_01.py`：正在学习 tuple、list、可变/不可变对象。
- `remote_log_filter.py`：已经开始用 Python 解决实际问题，涉及 SSH、命令行参数、字符串拼接、异常后的资源关闭。
- `remote_log_filter_02.py`：加入了 JSON 配置、文件写入、路径拼接和结果保存。
- `remote_log_filter_03.py`：开始尝试多个关键字、匹配模式和命令构建函数。

你的路线不需要从纯语法题一直刷到很后面。更适合的方式是：基础语法打牢，同时围绕“远程日志分析工具”这个真实小项目持续升级。

## 总目标

用 8 周时间完成三个目标：

1. Python 基础能独立写出来：变量、条件、循环、函数、常见容器、文件、异常、模块。
2. 能把一个脚本逐步重构成结构清晰的小工具：参数解析、配置管理、日志输出、错误处理、测试。
3. 能做出一个实用版远程日志分析 CLI：支持多环境、多服务、多关键字、保存结果、基本安全处理。

## 第 1 阶段：基础语法与数据结构（第 1-2 周）

目标：写代码时不再频繁卡在语法本身。

重点内容：

- 变量、数字、字符串、布尔值、`None`
- `if / elif / else`
- `for`、`while`、`break`、`continue`
- `list`、`tuple`、`dict`、`set`
- 切片、遍历、成员判断、常见内置函数
- 可变对象与不可变对象

建议练习：

- 扩展 `tuple_list_01.py`，增加 `dict` 和 `set` 的对比示例。
- 写一个 `basic_collections_practice.py`：
  - 统计一组日志级别里 `INFO`、`WARN`、`ERROR` 的数量。
  - 从一批用户名里去重。
  - 用字典保存服务名和日志路径。

阶段验收：

- 能解释 `list` 和 `tuple` 的区别。
- 能用 `dict` 表达配置类数据。
- 能写出一个 50 行以内的小练习脚本。

## 第 2 阶段：函数、模块与代码组织（第 3 周）

目标：从“顺着写脚本”过渡到“拆函数、分职责”。

重点内容：

- 函数参数、默认值、返回值
- 什么时候用 `print`，什么时候用 `return`
- `if __name__ == "__main__"` 的作用
- 标准库导入与第三方库导入
- 简单模块拆分

建议练习：

- 把日志脚本里的职责拆清楚：
  - `load_server_config()`：只负责读配置。
  - `build_grep_command()`：只负责生成远程命令。
  - `filter_remote_log()`：只负责连接服务器并执行命令。
  - `save_result()`：只负责保存结果。
- 单独创建 `command_builder_practice.py`，只练习命令字符串构建。

阶段验收：

- 每个函数只做一件明确的事。
- 函数名能看出意图。
- 业务代码和命令行入口能分开。

## 第 3 阶段：文件、JSON、异常处理（第 4 周）

目标：能稳定读写文件，并知道常见错误怎么处理。

重点内容：

- `open()` 和 `with`
- 文本文件读写
- JSON 读取与写入
- `try / except / finally`
- 常见异常：`FileNotFoundError`、`KeyError`、`ValueError`
- 路径处理：`pathlib`、`posixpath`

建议练习：

- 给 `load_server_config()` 增加更友好的错误提示：
  - 配置文件不存在。
  - JSON 格式错误。
  - 指定环境不存在。
- 把结果文件统一保存到 `results/` 目录。
- 保存结果时处理关键字里的特殊字符，避免文件名不合法。

阶段验收：

- 脚本遇到配置错误时不会直接炸出一大堆堆栈。
- 结果文件有统一目录和清晰命名。
- 能解释 `with open(...) as f` 为什么推荐使用。

## 第 4 阶段：命令行工具能力（第 5 周）

目标：把脚本做得像一个真正可用的小工具。

重点内容：

- `argparse`
- 必填参数、默认参数、可选值
- `nargs="+"` 接收多个值
- `choices` 限制参数范围
- 帮助文本设计

建议练习：

- 修正并完善 `remote_log_filter_03.py`：
  - 当前 `filter_remote_log()` 接收的是 `keywords`，但内部还在使用 `keyword`。
  - 命令行入口调用时传了 `keyword=args.keyword`，但参数实际叫 `--keywords`。
  - `--lines` 在 `remote_log_filter_03.py` 里需要补回来。
  - `build_grep_command()` 已经写出来了，应该在 `filter_remote_log()` 里实际使用它。
- 增加命令示例：

```bash
python remote_log_filter_03.py --env test --log-filename sms-customer-boot --keywords ERROR timeout --mode any --lines 1000
python remote_log_filter_03.py --env test --log-filename sms-customer-boot --keywords userId Exception --mode all --lines 500
```

阶段验收：

- `python remote_log_filter_03.py --help` 输出清楚。
- 参数传错时，提示能让自己看懂。
- 支持一个关键字和多个关键字。

## 第 5 阶段：第三方库与远程操作（第 6 周）

目标：理解 `paramiko` 这类库怎么查文档、怎么稳妥使用。

重点内容：

- `pip` 安装依赖
- 虚拟环境：`python -m venv .venv`
- `requirements.txt`
- `paramiko.SSHClient`
- 连接超时、认证失败、远程命令失败
- stdout / stderr / exit status

建议练习：

- 新增 `requirements.txt`，记录 `paramiko`。
- 执行远程命令后读取退出码：
  - grep 找不到内容时可能返回非 0，这不一定是程序错误。
  - SSH 连接失败、日志文件不存在、权限不足，需要区分提示。
- 把 SSH 密码从代码和 `config.json` 中移走，改用环境变量或本机私有配置文件。

阶段验收：

- 新电脑 clone 仓库后，能根据文档装依赖并运行。
- 远程连接失败时能看懂错误。
- 不再把服务器密码提交到 Git 仓库。

## 第 6 阶段：重构成小项目（第 7 周）

目标：把多个练习脚本沉淀成一个清晰的小项目结构。

建议结构：

```text
learnTest/
  README.md
  PYTHON_LEARNING_PLAN.md
  requirements.txt
  config.example.json
  src/
    log_filter/
      __init__.py
      cli.py
      config.py
      command.py
      ssh_client.py
      output.py
  tests/
    test_command.py
```

重点内容：

- `src` 目录结构
- 包和模块
- 示例配置 `config.example.json`
- 真实配置加入 `.gitignore`
- 业务逻辑和命令行入口分离

阶段验收：

- 运行入口清楚。
- 配置示例安全。
- 代码不再全部挤在一个文件里。

## 第 7 阶段：测试与质量习惯（第 8 周）

目标：让自己能放心改代码。

重点内容：

- `pytest`
- 测试纯函数
- 测试 `build_grep_command()`
- 格式化：`ruff format` 或 `black`
- 静态检查：`ruff`

建议练习：

- 给 `build_grep_command()` 写测试：
  - `mode="any"` 时生成 `grep -e`。
  - `mode="all"` 时生成多个串联 `grep`。
  - 关键字包含空格或特殊字符时，确认用了 `shlex.quote()`。
- 每次改脚本前先跑测试，改完再跑一次。

阶段验收：

- 至少有 5 个测试用例。
- 修改命令构建逻辑时，能通过测试确认没有改坏。
- 形成“先验证，再提交”的习惯。

## 当前项目的优先改进清单

建议按这个顺序做，不要一口气全改：

1. 修复 `remote_log_filter_03.py` 的参数名问题，让它能正常运行。
2. 把 `build_grep_command()` 接入实际执行流程。
3. 增加 `--lines` 参数。
4. 新增 `requirements.txt`。
5. 新增 `config.example.json`，真实 `config.json` 后续加入 `.gitignore`。
6. 把结果文件保存到 `results/`。
7. 给命令构建函数加 `pytest` 测试。
8. 再考虑拆成 `src/log_filter/` 项目结构。

## 每周学习节奏

建议每周 4 次，每次 45-90 分钟：

- 第 1 次：学一个新知识点，写最小示例。
- 第 2 次：把知识点用到日志脚本里。
- 第 3 次：整理注释和 README，写下自己卡住的点。
- 第 4 次：做一次小重构或补测试。

每次学习结束前，做三件小事：

1. 运行代码确认没有明显错误。
2. 写 3-5 行学习记录。
3. 提交一次 git commit。

## 推荐学习顺序备忘

短期先补：

- `dict`
- 函数返回值
- 异常处理
- `argparse`
- 文件与 JSON

中期再补：

- 虚拟环境
- 依赖管理
- 测试
- 项目结构
- Git 分支与 PR

长期再看：

- 面向对象
- 类型注解
- 日志库 `logging`
- 正则表达式
- Web API 调用
- 自动化任务与定时执行

## 一个判断标准

如果某个知识点学完后，能让 `remote_log_filter` 这个脚本更稳定、更好用、更安全，那它就是现阶段值得优先学的知识点。

先把一个真实工具打磨好，比零散学很多语法更容易形成手感。
