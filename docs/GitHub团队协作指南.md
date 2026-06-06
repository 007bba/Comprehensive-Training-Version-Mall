# GitHub 团队协作指南

仓库地址：

```text
https://github.com/007bba/Comprehensive-Training-Version-Mall.git
```

## 1. 首次拉取项目

HTTPS：

```powershell
git clone https://github.com/007bba/Comprehensive-Training-Version-Mall.git
cd Comprehensive-Training-Version-Mall
```

SSH：

```powershell
git clone git@github.com:007bba/Comprehensive-Training-Version-Mall.git
cd Comprehensive-Training-Version-Mall
```

如果使用 SSH，需要先在 GitHub 个人账号中配置 SSH Key。

## 2. 配置本地运行环境

后端：

```powershell
cd myshop-api2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

打开 `.env`，填写自己的数据库账号、密码、端口等本地配置。`.env` 不提交到 Git。

前端：

```powershell
cd ..\myshop-vue
npm install
$env:API_BASE_URL="http://localhost:8000/"
npm run dev
```

## 3. 日常开发流程

每次开始写代码前，先同步主分支：

```powershell
git checkout main
git pull origin main
```

为自己的任务创建分支：

```powershell
git checkout -b feature/your-task-name
```

提交代码：

```powershell
git status
git add .
git commit -m "feat: describe your change"
git push -u origin feature/your-task-name
```

然后在 GitHub 上创建 Pull Request，请至少一名成员 review 后再合并到 `main`。

## 4. 分支命名建议

```text
feature/login-page
feature/goods-api
fix/cart-total
docs/setup-guide
```

## 5. 提交信息建议

```text
feat: add goods category page
fix: correct cart total calculation
docs: update setup guide
chore: update dependencies
```

## 6. 冲突处理

同步远程主分支：

```powershell
git checkout main
git pull origin main
git checkout feature/your-task-name
git merge main
```

如果出现冲突，打开冲突文件，保留正确代码后执行：

```powershell
git add .
git commit
git push
```

## 7. 不要提交的内容

不要提交以下内容：

```text
node_modules/
dist/
.venv/
env-py3.8.2/
.env
*.log
.idea/
.vscode/
```

数据库密码、GitHub Token、服务器密码等敏感信息必须放在本机环境变量或 `.env` 中，不要写进代码。

## 8. 加入协作

仓库管理员在 GitHub 中邀请成员：

1. 打开仓库页面。
2. 进入 `Settings`。
3. 进入 `Collaborators and teams`。
4. 点击 `Add people`。
5. 输入成员 GitHub 用户名或邮箱并发送邀请。

成员接受邀请后即可 push 自己的分支并创建 Pull Request。
