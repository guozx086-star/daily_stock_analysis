# 🚀 启动指南

## ✅ 已完成的配置

1. ✅ 股票代码：688499（利元亨）
2. ✅ AI模型：DeepSeek
3. ✅ WebUI：已启用，端口 8000

## 📝 接下来需要做的事情

### 第1步：获取 DeepSeek API Key

1. 打开浏览器，访问：https://platform.deepseek.com/
2. 注册/登录账号
3. 进入「API Keys」页面
4. 点击「创建新密钥」
5. 复制生成的 API Key（格式：sk-xxxxx）

### 第2步：填入 API Key

打开文件：`/Users/guozhengxiao/daily_stock_analysis/.env`

找到这一行：
```
OPENAI_API_KEY=YOUR_DEEPSEEK_API_KEY
```

替换成：
```
OPENAI_API_KEY=sk-你的真实key
```

### 第3步：启动服务

在终端运行：
```bash
cd /Users/guozhengxiao/daily_stock_analysis
docker-compose -f ./docker/docker-compose.yml up -d webui
```

### 第4步：访问 WebUI

打开浏览器，访问：
```
http://localhost:8000
```

## 🔧 其他可选配置

### 添加飞书推送（可选）

如果你想同时接收飞书通知：

1. 打开飞书，创建一个群聊
2. 群设置 → 群机器人 → 添加机器人 → 自定义机器人
3. 复制 Webhook 地址

然后在 `.env` 文件中找到：
```
# FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your_key_here
```

去掉 `#` 注释，并替换为你的真实 URL。

## 📊 使用方式

### 立即分析

在 WebUI 页面点击「立即分析」按钮

### 查看历史

在 WebUI 查看历史分析报告

### 停止服务

```bash
docker-compose -f ./docker/docker-compose.yml down
```

### 查看日志

```bash
docker-compose -f ./docker/docker-compose.yml logs -f webui
```

## ❓ 常见问题

### 1. Docker 未安装？

macOS 安装：
```bash
brew install --cask docker
```

### 2. 端口 8000 被占用？

修改 `.env` 文件中的 `WEBUI_PORT=8000` 改为其他端口，如 `8001`

### 3. 看不到分析结果？

检查 DeepSeek API Key 是否正确填写，余额是否充足

---

💡 **提示**：首次运行会下载 Docker 镜像，可能需要几分钟时间。
