<#
.SYNOPSIS
一键启动FMECA设施设备分析管理平台的前端和后端服务

.DESCRIPTION
此脚本将同时启动后端Django服务和前端开发服务器，方便用户快速启动整个平台

.NOTES
作者: AI助手
版本: 1.0
创建日期: 2026-01-11
#>

# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "        FMECA平台一键启动脚本          " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python是否安装
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 未检测到Python，请先安装Python 3.8+" -ForegroundColor Red
    pause
    exit 1
}

# 检查Node.js是否安装
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 未检测到Node.js，请先安装Node.js 16+" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "✅ 环境检查通过" -ForegroundColor Green
Write-Host ""

# 启动后端服务
Write-Host "正在启动后端服务..." -ForegroundColor Yellow
$backendPath = "$PSScriptRoot\backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; .\start.bat" -WindowStyle Minimized

# 等待后端服务启动
Start-Sleep -Seconds 2

# 启动前端服务
Write-Host "正在启动前端服务..." -ForegroundColor Yellow
$frontendPath = "$PSScriptRoot\frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev" -WindowStyle Minimized

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "        服务启动完成！                " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "后端服务地址: http://localhost:8000" -ForegroundColor Green
Write-Host "前端服务地址: http://localhost:5173" -ForegroundColor Green
Write-Host "" -ForegroundColor Yellow
Write-Host "⚠️  注意: 请在浏览器中访问前端服务地址 (http://localhost:5173)" -ForegroundColor Yellow
Write-Host "" -ForegroundColor Green
Write-Host "按任意键退出此脚本..." -ForegroundColor Cyan

# 等待用户输入
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
