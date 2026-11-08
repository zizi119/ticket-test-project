# 工单接口测试练习

## 项目内容

- `ticket.py`：本机练习用的工单接口，监听 `127.0.0.1:8001`。
- `test_ticket_api.py`：工单接口的自动化测试。
- `test_basics.py`：Python 断言、静态文件和模拟响应的基础练习。

工单接口内置测试数据：工单 `T1001` 属于用户 `U001`，标题为“无法登录”。

## 运行环境

电脑需要安装 Python 和 pytest。首次安装 pytest 时运行：

```powershell
python -m pip install pytest
```

## 运行工单接口测试

在项目目录打开第一个命令窗口，启动工单服务：

```powershell
python ticket.py
```

保持该窗口运行。在同一目录打开第二个命令窗口，执行：

```powershell
python -m pytest test_ticket_api.py -v
```

预期收集到 **5 个测试**，结果为 **`5 passed`**。测试覆盖：工单所有者查询、其他用户越权查询、不存在的工单、管理员查询、未带用户标识查询。

## 运行全部练习测试

`test_basics.py` 中的部分测试还需要本机 8000 端口的静态文件服务。在包含 `hello.txt` 和 `ticket.json` 的目录中，另开命令窗口运行：

```powershell
python -m http.server 8000
```

保持 8000 和 8001 两个服务运行，再在项目目录执行：

```powershell
python -m pytest -v
```

当前预期收集到 **10 个测试**，结果为 **`10 passed`**。

## 常见问题

- **连接被拒绝**：检查对应端口的服务是否仍在运行。
- **找不到文件**：检查命令窗口是否位于项目目录，以及 `hello.txt`、`ticket.json` 是否存在。
- **收集到的测试数量不对**：检查测试文件名和以 `test_` 开头的函数名。
- **端口被占用**：先确认是否已有同一个服务在运行。

`X-User-Id` 仅用于本机练习，可由请求方自行填写，不代表真实系统的安全登录机制。
本项目已接入 GitHub Actions，提交后自动运行 pytest。