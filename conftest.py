import socket
import subprocess
import sys
import time
from pathlib import Path
import pytest
@pytest.fixture(scope="session")
def base_url():
    server_file = Path(__file__).parent / "ticket.py"
    process = subprocess.Popen(
        [sys.executable, str(server_file)],
        cwd=server_file.parent,
    )

    try:
        # 最多等待 6 秒，直到服务开始监听 8001
        for _ in range(30):
            if process.poll() is not None:
                raise RuntimeError("工单服务启动失败，请检查 ticket.py")

            try:
                with socket.create_connection(("127.0.0.1", 8001), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.2)
        else:
            raise RuntimeError("等待工单服务启动超时")

        yield "http://127.0.0.1:8001"

    finally:
        process.terminate()
        process.wait(timeout=5)
@pytest.fixture(scope="session")
def static_base_url():
    project_dir = Path(__file__).parent
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            "8000",
            "--directory",
            str(project_dir),
        ],
        cwd=project_dir,
    )

    try:
        for _ in range(30):
            if process.poll() is not None:
                raise RuntimeError("静态文件服务启动失败")

            try:
                with socket.create_connection(("127.0.0.1", 8000), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.2)
        else:
            raise RuntimeError("等待静态文件服务启动超时")

        yield "http://127.0.0.1:8000"

    finally:
        process.terminate()
        process.wait(timeout=5)