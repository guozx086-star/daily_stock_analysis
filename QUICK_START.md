# 🎯 快速开始 - 无需Docker版本

## ✅ 当前状态

- ✅ Python 依赖正在安装中...
- ✅ 股票代码：688499（利元亨）
- ✅ AI模型：DeepSeek（待配置API Key）
- ✅ WebUI：已启用

## 📝 下一步操作

### 1. 获取 DeepSeek API Key（必须）

打开浏览器访问：**https://platform.deepseek.com/**

步骤：
1. 注册/登录账号
2. 进入「API Keys」页面
3. 点击「创建新密钥」
4. 复制生成的 Key（格式：`sk-xxxxx`）

💰 **费用**：DeepSeek 非常便宜，新用户有免费额度，基本够用！

### 2. 配置 API Key

用文本编辑器打开文件：
```
/Users/guozhengxiao/daily_stock_analysis/.env
```

找到第44行：
```bash
OPENAI_API_KEY=YOUR_DEEPSEEK_API_KEY
```

改成：
```bash
OPENAI_API_KEY=sk-你刚才复制的key
```

保存文件。

### 3. 等待安装完成

当前 Python 依赖包正在安装，需要几分钟时间。

你可以等安装完成后告诉我，我会帮你启动服务！

### 4. 启动服务（等安装完成后）

```bash
cd /Users/guozhengxiao/daily_stock_analysis
python3 main.py --webui-only
```

### 5. 访问 WebUI

打开浏览器：**http://localhost:8000**

## 🎨 使用方式

1. **立即分析**：点击页面上的「立即分析」按钮
2. **查看历史**：可以查看之前的分析记录
3. **添加股票**：修改 `.env` 文件中的 `STOCK_LIST`，可以添加多只股票

例如：
```bash
# 单只股票
STOCK_LIST=688499

# 多只股票（逗号分隔）
STOCK_LIST=688499,600519,300750

# 混合市场
STOCK_LIST=688499,hk00700,AAPL
```

## 💡 提示

- A股代码：直接用数字，如 `688499`
- 港股代码：加 `hk` 前缀，如 `hk00700`（腾讯）
- 美股代码：直接用字母，如 `AAPL`（苹果）、`TSLA`（特斯拉）

---

## ❓ 常见问题

### Q: 如何停止服务？

按 `Ctrl + C` 即可

### Q: 想要飞书推送怎么办？

1. 飞书创建群聊 → 群机器人 → 自定义机器人
2. 复制 Webhook 地址
3. 在 `.env` 文件中找到 `#  FEISHU_WEBHOOK_URL=...`
4. 去掉 `#` 并填入你的 Webhook 地址

### Q: 分析失败怎么办？

检查：
1. DeepSeek API Key 是否正确
2. DeepSeek 账户余额是否充足
3. 网络连接是否正常

---

📱 需要帮助？把错误信息发给我！
