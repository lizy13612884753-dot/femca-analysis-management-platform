# FMECA设施设备分析管理平台 - 一键启动指南

## 环境要求

在使用一键启动脚本前，请确保您的计算机已安装以下软件：

1. **Python 3.8+**
   - 用于运行后端Django服务
   - 下载地址：https://www.python.org/downloads/

2. **Node.js 16+**
   - 用于运行前端开发服务器
   - 下载地址：https://nodejs.org/en/download/

## 一键启动方法

### 方法1：Windows批处理文件（推荐）

1. 直接双击运行 `start_platform.bat` 文件
2. 脚本将自动检查环境并启动前后端服务
3. 等待服务启动完成后，在浏览器中访问前端地址

### 方法2：PowerShell脚本

1. 右键点击 `start_platform.ps1` 文件
2. 选择 "使用PowerShell运行"
3. 如果出现执行策略提示，请选择 "是(Y)" 或 "全是(A)"

## 手动启动方法

如果一键启动脚本无法正常工作，您可以手动启动前后端服务：

### 步骤1：启动后端服务

1. 打开命令行窗口，进入 `backend` 目录
2. 执行以下命令：
   ```bash
   cd backend
   python manage.py runserver 0.0.0.0:8000
   ```

### 步骤2：启动前端服务

1. 打开另一个命令行窗口，进入 `frontend` 目录
2. 执行以下命令：
   ```bash
   cd frontend
   npm run dev
   ```

## 访问平台

服务启动后，您可以通过以下地址访问平台：

- **前端地址**：http://localhost:3000
- **后端API地址**：http://localhost:8000/api/

## 服务管理

### 停止服务

- **后端服务**：在后端命令行窗口按 `Ctrl+C`
- **前端服务**：在前端命令行窗口按 `Ctrl+C`

### 重启服务

如果需要重启服务，只需关闭当前的服务窗口，重新运行启动脚本即可。

## 常见问题

### 1. 端口被占用

**症状**：服务启动失败，提示端口已被使用

**解决方法**：
- 关闭占用端口的其他程序
- 或修改服务端口配置：
  - 后端端口：修改 `backend\start.bat` 文件中的端口号
  - 前端端口：修改 `frontend\vite.config.js` 文件中的端口配置

### 2. 依赖安装问题

**症状**：前端服务启动失败，提示缺少依赖

**解决方法**：
```bash
cd frontend
npm install
```

### 3. Python模块缺失

**症状**：后端服务启动失败，提示缺少Python模块

**解决方法**：
```bash
cd backend
pip install -r requirements.txt
```

## 技术支持

如果您在使用过程中遇到其他问题，请联系技术支持团队。

---

**版本**：1.0
**更新日期**：2026-01-11
