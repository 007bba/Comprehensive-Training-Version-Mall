# Comprehensive-Training-Version-Mall

综合实训商城项目，包含 Django REST API 后端和 Vue 2 前端。本文档说明如何在本地开发环境和生产环境中部署、启动与使用本项目。

## 目录

- [项目结构](#项目结构)
- [环境准备](#环境准备)
- [后端部署与启动](#后端部署与启动)
- [前端部署与启动](#前端部署与启动)
- [本地开发启动流程](#本地开发启动流程)
- [生产环境部署建议](#生产环境部署建议)
- [常见问题](#常见问题)
- [协作说明](#协作说明)

## 项目结构

```text
myshop-api2/   Django REST API 后端
myshop-vue/    Vue 2 前端
docs/          项目说明与协作文档
```

## 环境准备

### 1. 安装 Conda

推荐使用 Conda 管理后端 Python 版本和虚拟环境。可以安装 Miniconda 或 Anaconda：

- Miniconda 下载地址：https://docs.conda.io/en/latest/miniconda.html
- Anaconda 下载地址：https://www.anaconda.com/download

安装完成后，打开终端并检查 Conda 是否可用：

```bash
conda --version
```

如果能看到类似下面的输出，说明安装成功：

```text
conda 24.x.x
```

### 2. 安装 Node.js

前端项目使用 Vue 2 + webpack 3，依赖相对较旧。推荐使用 Node.js 14.x 或 16.x，不建议直接使用过新的 Node.js 版本。

推荐使用 Node.js 版本管理工具安装和切换 Node.js 版本：

- macOS/Linux 推荐 nvm：https://github.com/nvm-sh/nvm
- Windows 推荐 nvm-windows：https://github.com/coreybutler/nvm-windows

安装版本管理工具后，可以安装并切换到 Node.js 14：

```bash
nvm install 14
nvm use 14
```

检查 Node.js 与 npm：

```bash
node -v
npm -v
```

## 后端部署与启动

后端目录为：

```text
myshop-api2
```

### 1. 进入后端目录

```bash
cd myshop-api2
```

### 2. 创建并激活 Conda 环境

项目后端推荐使用 Python 3.8。

```bash
conda create -n myshop python=3.8 -y
conda activate myshop
```

确认 Python 版本：

```bash
python --version
```

### 3. 安装后端依赖

```bash
pip install -r requirements.txt
```

如果下载速度较慢，可以使用清华 PyPI 镜像：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

主要依赖包括：

```text
Django==3.1.5
djangorestframework==3.12.4
djangorestframework_jwt==1.11.0
django_ckeditor==6.1.0
django-filter==2.4.0
django-cors-headers==3.6.0
pymysql==1.0.2
psycopg2-binary==2.9.9
gunicorn==20.1.0
django-prometheus==2.2.0
```

### 4. 配置后端环境变量

后端会读取 `myshop-api2/.env` 文件。项目提供了模板文件 `.env.example`。

Linux/macOS/Git Bash：

```bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

开发环境可以先使用 SQLite：

```env
DJANGO_SECRET_KEY=change-this-to-a-long-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

如果不配置 `DATABASE_URL`，项目会默认使用 SQLite 数据库：

```text
myshop-api2/db.sqlite3
```
已经有postgresql的配置了，就在env文件中配好了，可以不用管。
如果使用 PostgreSQL，例如 Supabase，可以配置：

```env
DJANGO_SECRET_KEY=change-this-to-a-long-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://用户名:密码@数据库地址:5432/数据库名?sslmode=require
```

生产环境请务必修改：

```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=你的域名,你的服务器IP
```

### 5. 初始化数据库

```bash
python manage.py makemigrations
python manage.py migrate
```

项目使用了 Django 数据库缓存，需要创建缓存表：

```bash
python manage.py createcachetable
```

如果提示缓存表已存在，可以忽略。

### 6. 创建管理员账号

```bash
python manage.py createsuperuser
```

按照提示输入用户名、邮箱和密码。

### 7. 启动后端服务

开发环境启动：

```bash
python manage.py runserver 0.0.0.0:8000
```

常用访问地址：

```text
后端首页：http://localhost:8000/
管理后台：http://localhost:8000/admin/
接口文档：http://localhost:8000/docs/
Swagger 文档：http://localhost:8000/docs2/
JWT 登录接口：http://localhost:8000/login/
Token 认证接口：http://localhost:8000/api-token-auth/
```

## 前端部署与启动

前端目录为：

```text
myshop-vue
```

### 1. 进入前端目录

```bash
cd myshop-vue
```

### 2. 安装前端依赖

```bash
npm install
```

如果下载速度较慢，可以使用 npm 镜像：

```bash
npm install --registry=https://registry.npmmirror.com
```

如果遇到旧依赖兼容问题，可以尝试：

```bash
npm install --legacy-peer-deps
```

### 3. 配置前端接口地址

前端接口地址配置在：

```text
myshop-vue/config/dev.env.js
myshop-vue/config/prod.env.js
```

当前默认接口地址为：

```text
http://localhost:8000/
```

也可以通过环境变量 `API_BASE_URL` 指定后端地址。

Linux/macOS/Git Bash：

```bash
API_BASE_URL=http://localhost:8000/ npm run dev
```

Windows PowerShell：

```powershell
$env:API_BASE_URL="http://localhost:8000/"
npm run dev
```

Windows CMD：

```cmd
set API_BASE_URL=http://localhost:8000/
npm run dev
```

### 4. 启动前端开发服务

```bash
npm run dev
```

也可以使用：

```bash
npm start
```

默认访问地址：

```text
http://localhost:8080/
```

## 本地开发启动流程

建议同时打开两个终端。

### 终端 1：启动后端

```bash
cd myshop-api2
conda activate myshop
python manage.py runserver 0.0.0.0:8000
```

### 终端 2：启动前端

```bash
cd myshop-vue
npm run dev
```

然后在浏览器访问：

```text
http://localhost:8080/
```

## 生产环境部署建议

### 1. 后端生产环境配置

生产环境 `.env` 示例：

```env
DJANGO_SECRET_KEY=替换成强随机密钥
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=你的域名,你的服务器IP
DATABASE_URL=postgresql://用户名:密码@数据库地址:5432/数据库名?sslmode=require
```

### 2. 收集 Django 静态文件

在 `myshop-api2` 目录下执行：

```bash
python manage.py collectstatic
```

静态文件会收集到：

```text
myshop-api2/static
```

### 3. 使用 Gunicorn 启动后端

Linux 服务器上可以使用 Gunicorn：

```bash
cd myshop-api2
conda activate myshop
gunicorn myshop.wsgi:application --bind 0.0.0.0:8000
```

生产环境建议配合 systemd、supervisor 或 Docker 管理进程。

### 4. 构建前端生产文件

进入前端目录：

```bash
cd myshop-vue
```

构建前指定生产后端地址：

```bash
API_BASE_URL=https://你的后端域名/ npm run build
```

Windows PowerShell：

```powershell
$env:API_BASE_URL="https://你的后端域名/"
npm run build
```

构建：

```bash
npm run build
```

构建产物目录：

```text
myshop-vue/dist
```

生产环境部署时，将 `dist` 目录交给 Nginx 或其他静态文件服务器即可。

### 5. Nginx 简单示例

下面示例中：

- 前端静态文件位于 `/path/to/myshop-vue/dist`
- 后端 Gunicorn 监听 `127.0.0.1:8000`

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/myshop-vue/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8000/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /docs/ {
        proxy_pass http://127.0.0.1:8000/docs/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /docs2/ {
        proxy_pass http://127.0.0.1:8000/docs2/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /media/ {
        proxy_pass http://127.0.0.1:8000/media/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        proxy_pass http://127.0.0.1:8000/static/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /login/ {
        proxy_pass http://127.0.0.1:8000/login/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api-token-auth/ {
        proxy_pass http://127.0.0.1:8000/api-token-auth/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

如果后端接口较多且没有统一 `/api/` 前缀，也可以单独部署前端和后端到不同域名，前端构建时将 `API_BASE_URL` 指向后端域名即可。

## 常见问题

### 1. 后端提示找不到 Django

通常是 Conda 环境未激活或依赖未安装。

```bash
conda activate myshop
pip install -r requirements.txt
```

### 2. 数据库连接失败

检查 `.env` 中的 `DATABASE_URL` 是否正确。如果只是本地开发，可以先使用 SQLite：

```env
DATABASE_URL=sqlite:///db.sqlite3
```

或者删除 `DATABASE_URL`，项目会自动使用默认 SQLite。

### 3. 前端请求接口失败

先确认后端是否启动：

```text
http://localhost:8000/
```

再确认前端接口地址是否正确。默认配置为：

```text
http://localhost:8000/
```

如果后端部署在其他机器，需要通过 `API_BASE_URL` 指定后端地址。

### 4. 前端 npm install 报错

该项目依赖较旧，推荐使用 Node.js 14.x 或 16.x。

可以尝试：

```bash
npm install --legacy-peer-deps
```

### 5. 跨域问题

后端当前允许跨域请求，开发环境一般不会有跨域问题。生产环境建议只允许实际前端域名访问，而不是开放全部来源。

## 协作说明

团队成员请先阅读 [GitHub团队协作指南](docs/GitHub团队协作指南.md)。
