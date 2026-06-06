@echo off
chcp 65001 >nul
echo ========================================
echo   商城后端服务启动
echo ========================================
echo.

set PYTHON=E:\360Downloads\miniconda\envs\myshop\python.exe
set PROJECT_DIR=%~dp0myshop-api2

cd /d %PROJECT_DIR%

echo [1] 执行数据库迁移...
%PYTHON% manage.py migrate

echo.
echo [2] 启动 Django 服务 (http://127.0.0.1:8000)...
%PYTHON% manage.py runserver 0.0.0.0:8000

pause
