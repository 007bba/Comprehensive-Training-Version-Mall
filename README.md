# Comprehensive-Training-Version-Mall

综合实训商城项目，包含 Django 后端和 Vue 2 前端。

## 项目结构

```text
myshop-api2/   Django REST API 后端
myshop-vue/    Vue 2 前端
docs/          项目说明与协作文档
```

## 本地启动

### 后端

```powershell
cd myshop-api2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

编辑 `.env`，填写本机 MySQL 连接信息，然后执行：

```powershell
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

### 前端

```powershell
cd myshop-vue
npm install
$env:API_BASE_URL="http://localhost:8000/"
npm run dev
```

默认前端开发地址为 `http://localhost:8080/`。

## 协作说明

团队成员请先阅读 [GitHub团队协作指南](docs/GitHub团队协作指南.md)。
