# ☁️ 股票分析系统 - 云端部署指南

## 📋 目录
1. [方案一: 阿里云/腾讯云 (推荐)](#方案一-阿里云腾讯云)
2. [方案二: Railway (免费)](#方案二-railway)
3. [方案三: Vercel + Supabase](#方案三-vercel--supabase)

---

## 方案一: 阿里云/腾讯云 (推荐) ⭐

### 💰 费用: ¥30-100/月
### ⏱️ 部署时间: 15分钟

### 步骤 1: 购买云服务器

**推荐配置:**
- CPU: 2核
- 内存: 2GB
- 带宽: 3Mbps
- 系统: Ubuntu 22.04

**购买链接:**
- 阿里云: https://www.aliyun.com/product/ecs
- 腾讯云: https://cloud.tencent.com/product/cvm

### 步骤 2: 连接服务器

```bash
# 使用 SSH 连接 (替换为你的服务器 IP)
ssh root@你的服务器IP
```

### 步骤 3: 安装 Docker

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | bash

# 启动 Docker
systemctl start docker
systemctl enable docker

# 安装 Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 步骤 4: 上传项目到服务器

**方法一: Git 克隆 (推荐)**
```bash
# 安装 Git
apt update && apt install -y git

# 克隆项目 (需要先上传到 GitHub)
git clone https://github.com/你的用户名/daily_stock_analysis.git
cd daily_stock_analysis
```

**方法二: 直接上传**
```bash
# 在本地电脑执行 (替换为你的服务器 IP)
scp -r /Users/guozhengxiao/daily_stock_analysis root@你的服务器IP:/root/
```

### 步骤 5: 配置环境变量

```bash
# 编辑 .env 文件
nano .env

# 修改以下配置:
# 1. 确认 Gemini API Key 已填写
# 2. 确认 STOCK_LIST 股票代码
# 3. 设置 WEBUI_HOST=0.0.0.0 (已设置)
# 4. 可选: 添加飞书 Webhook URL
```

### 步骤 6: 启动服务

```bash
# 启动 WebUI 模式
docker-compose -f docker/docker-compose.yml up -d webui

# 查看日志
docker-compose -f docker/docker-compose.yml logs -f webui
```

### 步骤 7: 配置防火墙

```bash
# 开放 8000 端口
# 阿里云/腾讯云: 在控制台安全组添加规则
# 入站规则: TCP 8000 端口, 来源 0.0.0.0/0

# Linux 防火墙 (如果有)
ufw allow 8000
```

### 步骤 8: 访问

浏览器打开: `http://你的服务器IP:8000`

### 🔒 可选: 配置 HTTPS + 域名

```bash
# 安装 Nginx
apt install -y nginx

# 安装 Certbot (Let's Encrypt)
apt install -y certbot python3-certbot-nginx

# 配置 Nginx
cat > /etc/nginx/sites-available/stock << 'EOF'
server {
    listen 80;
    server_name 你的域名.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/stock /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# 申请 SSL 证书
certbot --nginx -d 你的域名.com
```

---

## 方案二: Railway (免费) 🆓

### 💰 费用: 免费 (每月 $5 额度)
### ⏱️ 部署时间: 5分钟

### 步骤 1: 准备 GitHub 仓库

```bash
# 在本地项目目录
cd /Users/guozhengxiao/daily_stock_analysis

# 初始化 Git (如果还没有)
git init
git add .
git commit -m "Initial commit"

# 上传到 GitHub
# 1. 在 GitHub 创建新仓库: https://github.com/new
# 2. 推送代码
git remote add origin https://github.com/你的用户名/daily_stock_analysis.git
git branch -M main
git push -u origin main
```

### 步骤 2: 部署到 Railway

1. 访问 https://railway.app/
2. 点击 "Start a New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择你的 `daily_stock_analysis` 仓库
5. Railway 会自动检测到 Dockerfile 并开始构建

### 步骤 3: 配置环境变量

在 Railway 项目设置中添加环境变量:
- `GEMINI_API_KEY`: 你的 Gemini API Key
- `STOCK_LIST`: 688499
- `WEBUI_ENABLED`: true
- `WEBUI_HOST`: 0.0.0.0
- `WEBUI_PORT`: 8000

### 步骤 4: 获取访问链接

Railway 会自动生成一个公开 URL,类似:
`https://your-app-name.railway.app`

---

## 方案三: Vercel + Supabase 🎯

### 💰 费用: 免费
### ⏱️ 部署时间: 10分钟
### 特点: 全球 CDN 加速,速度快

### 步骤 1: 创建 `vercel.json`

在项目根目录创建:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "web/server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "web/server.py"
    }
  ],
  "env": {
    "GEMINI_API_KEY": "@gemini_api_key",
    "STOCK_LIST": "688499"
  }
}
```

### 步骤 2: 部署到 Vercel

```bash
# 安装 Vercel CLI
npm install -g vercel

# 登录
vercel login

# 部署
cd /Users/guozhengxiao/daily_stock_analysis
vercel --prod
```

### 步骤 3: 配置数据库

Vercel 不支持 SQLite,需要使用云数据库:

1. 注册 Supabase: https://supabase.com/
2. 创建新项目
3. 获取数据库连接 URL
4. 在 Vercel 环境变量添加: `DATABASE_URL`

---

## 🎯 快速决策指南

| 需求 | 推荐方案 |
|-----|---------|
| 最稳定可靠 | 阿里云/腾讯云 |
| 零成本 | Railway |
| 全球访问快 | Vercel |
| 企业使用 | 阿里云 + HTTPS + 域名 |

---

## 🔧 常见问题

### Q1: 如何更新部署?

**Docker 方式:**
```bash
# SSH 连接到服务器
cd daily_stock_analysis
git pull
docker-compose -f docker/docker-compose.yml restart
```

**Railway 方式:**
```bash
# 本地推送代码
git push origin main
# Railway 自动重新部署
```

### Q2: 如何查看日志?

**Docker:**
```bash
docker-compose -f docker/docker-compose.yml logs -f webui
```

**Railway:**
在 Railway 控制台查看 "Deployments" -> "Logs"

### Q3: 如何设置定时任务?

在 `.env` 文件中:
```bash
SCHEDULE_ENABLED=true
SCHEDULE_TIME=18:00
```

Docker 会自动在每天 18:00 执行分析并推送。

### Q4: 如何配置飞书推送?

1. 在飞书群创建机器人,获取 Webhook URL
2. 在 `.env` 添加:
```bash
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your_key
```
3. 重启服务

---

## 📱 手机访问

部署成功后,手机浏览器打开:
- 云服务器: `http://你的服务器IP:8000`
- Railway: `https://your-app.railway.app`
- Vercel: `https://your-app.vercel.app`

建议添加到手机主屏幕,体验类似原生 App!

---

## 🆘 需要帮助?

如遇到问题,提供以下信息:
1. 选择的部署方案
2. 错误日志
3. 服务器配置 (如适用)

联系方式: [项目 GitHub Issues](https://github.com/ZhuLinsen/daily_stock_analysis/issues)
