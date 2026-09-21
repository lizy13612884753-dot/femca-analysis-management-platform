import subprocess
import sys
import os

os.chdir(r"c:\FEMCA platform test\backend")

cmd = [sys.executable, "manage.py", "runserver", "0.0.0.0:8000"]

print("启动后端服务...")
print(f"命令: {' '.join(cmd)}")
print("=" * 50)

try:
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        print(line, end="")

except KeyboardInterrupt:
    print("\n正在停止服务...")
    process.terminate()
    process.wait()
    print("服务已停止")
except Exception as e:
    print(f"错误: {e}")
