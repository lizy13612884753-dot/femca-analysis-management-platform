import subprocess
import sys
import os
import time

os.chdir(r"c:\FMECA platform test\backend")

print("=" * 60)
print("  FMECA平台后端服务")
print("=" * 60)
print(f"  启动时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  访问地址: http://localhost:8000")
print("=" * 60)
print()

cmd = [sys.executable, "manage.py", "runserver", "0.0.0.0:8000"]

restart_count = 0
max_restarts = 10

while restart_count < max_restarts:
    print(f"[{time.strftime('%H:%M:%S')}] 启动后端服务 (第{restart_count + 1}次尝试)...")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # 等待几秒看是否启动成功
        time.sleep(3)
        
        if process.poll() is None:
            print(f"[{time.strftime('%H:%M:%S')}] ✅ 后端服务已启动!")
            print(f"[{time.strftime('%H:%M:%S')}] 访问地址: http://localhost:8000")
            print(f"[{time.strftime('%H:%M:%S')}] 按 Ctrl+C 停止服务")
            print("-" * 60)
            
            # 持续读取输出
            for line in process.stdout:
                print(line, end="")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] ❌ 服务启动失败")
            restart_count += 1
            time.sleep(2)
            continue
            
    except KeyboardInterrupt:
        print(f"\n[{time.strftime('%H:%M:%S')}] 正在停止服务...")
        if 'process' in dir():
            process.terminate()
        print(f"[{time.strftime('%H:%M:%S')}] 服务已停止")
        break
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] 错误: {e}")
        restart_count += 1
        time.sleep(2)
