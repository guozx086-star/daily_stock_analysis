# 🚀 快速配置指南

## 1️⃣ 获取 DeepSeek API Key

1. 访问：https://platform.deepseek.com/
2. 注册/登录账号
3. 进入「API Keys」页面
4. 点击「创建新密钥」
5. 复制生成的 API Key（格式：sk-xxxxx）

💰 **费用说明**：DeepSeek 非常便宜，新用户有免费额度

---

## 2️⃣ 获取飞书 Webhook（可选）

1. 打开飞书，创建一个群聊
2. 群设置 → 群机器人 → 添加机器人 → 自定义机器人
3. 设置机器人名称和描述
4. 复制 Webhook 地址（格式：https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx）

---

## 3️⃣ 配置完成后

运行命令：
```bash
cd /Users/guozhengxiao/daily_stock_analysis
docker-compose -f ./docker/docker-compose.yml up -d webui
```

然后访问：http://localhost:8000

---

📝 配置完成后，告诉我你的 DeepSeek API Key，我会帮你配置好！
