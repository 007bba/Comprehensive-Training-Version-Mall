@echo off
chcp 65001 >nul
echo ========================================
echo   商城前端服务启动 (商家端)
echo ========================================
echo.

set PATH=C:\Program Files\nodejs;%PATH%
set PROJECT_DIR=%~dp0myshop-merchant-vue

cd /d "%PROJECT_DIR%"

echo [1] 检查 node_modules...
if not exist node_modules (
    echo 首次运行，正在安装依赖...
    call npm install
    if errorlevel 1 (
        echo.
        echo 依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo [2] 启动前端服务 (http://localhost:8081)...
call npm run dev

pause
