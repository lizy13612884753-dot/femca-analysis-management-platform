# 如何双击运行 start_platform.bat 文件

以下是详细的操作步骤，帮助您成功运行一键启动脚本：

## 步骤1：打开文件资源管理器

1. 点击 Windows 任务栏上的 **文件资源管理器** 图标（通常是黄色的文件夹图标）
2. 或者使用快捷键 **Win + E** 直接打开文件资源管理器

## 步骤2：导航到平台目录

1. 在文件资源管理器的地址栏中输入：
   ```
   c:\FMECA platform test
   ```
2. 按下 **Enter** 键

## 步骤3：找到并双击启动脚本

1. 在打开的目录中，您应该能看到名为 `start_platform.bat` 的文件
2. 将鼠标指针移动到该文件上
3. 快速点击鼠标左键两次（双击）

## 步骤4：观察启动过程

双击后，您会看到一个黑色的命令行窗口打开，显示以下信息：

```
==========================================
       FMECA Platform Startup          
==========================================

✅ Success: Environment check passed

正在启动后端服务...
正在启动前端服务...

==========================================
       Services started successfully!        
==========================================
Backend URL: http://localhost:8000
Frontend URL: http://localhost:3000

Note: Please access the frontend URL in your browser

Press any key to exit...
```

## 步骤5：访问平台

服务启动完成后，打开您的浏览器并访问：
- **前端地址**：http://localhost:3000

## 可能遇到的问题和解决方法

### 问题1：看不到文件扩展名（如 .bat）

如果您看到的文件名是 `start_platform` 而不是 `start_platform.bat`：

1. 在文件资源管理器中，点击 **查看** 选项卡
2. 勾选 **文件扩展名** 复选框
3. 现在您应该能看到完整的文件名 `start_platform.bat`

### 问题2：双击后命令行窗口很快消失

这通常是因为环境检查失败。您可以：

1. 右键点击 `start_platform.bat` 文件
2. 选择 **编辑**
3. 在文件末尾添加一行：`pause`
4. 保存文件并再次双击运行
5. 现在窗口会显示错误信息，您可以根据提示解决问题

### 问题3：提示 "Python not found" 或 "Node.js not found"

这表示您的电脑上没有安装所需的软件：

1. 安装 Python 3.8+：访问 https://www.python.org/downloads/
2. 安装 Node.js 16+：访问 https://nodejs.org/en/download/
3. 重新运行启动脚本

## 手动启动备选方案

如果双击脚本仍然遇到问题，您可以尝试手动启动：

1. 打开命令行窗口
2. 启动后端服务：
   ```
   cd c:\FMECA platform test\backend
   python manage.py runserver 0.0.0.0:8000
   ```
3. 打开另一个命令行窗口
4. 启动前端服务：
   ```
   cd c:\FMECA platform test\frontend
   npm run dev
   ```

如果您需要进一步的帮助，请参考 `STARTUP.md` 文件或联系技术支持。