# Railway 部署步骤 - 当前进度

## ✅ 已完成
1. Fork 项目到您的 GitHub
2. 登录 Railway

## 🔄 当前步骤: 连接 GitHub 仓库

### 操作指引:

1. **点击 "GitHub Repository"**

2. **选择仓库**
   - 在弹出的列表中找到并选择: `guozx086-star/daily_stock_analysis`
   - 如果没看到,点击 "Configure GitHub App" 授权访问

3. **等待 Railway 自动检测**
   - Railway 会自动识别 `railway.json` 和 `Dockerfile`
   - 自动开始构建

4. **添加环境变量**
   - 构建开始后,点击左侧项目名
   - 点击 "Variables" 标签
   - 添加所需的环境变量 (详见下方列表)

---

## 📝 需要添加的环境变量

在 Railway Variables 页面,逐个添加:

```
GEMINI_API_KEY=AIzaSyCV-2SavzqoGyphV_OEOE7y5OK12NAl2Hg
GEMINI_MODEL=gemini-2.5-flash
GEMINI_MODEL_FALLBACK=gemini-2.0-flash
STOCK_LIST=688499
WEBUI_ENABLED=true
WEBUI_HOST=0.0.0.0
WEBUI_PORT=8000
SCHEDULE_ENABLED=true
SCHEDULE_TIME=18:00
MARKET_REVIEW_ENABLED=true
```

添加方法:
- 点击 "New Variable"
- Name: 输入变量名 (如 GEMINI_API_KEY)
- Value: 输入对应的值
- 点击 "Add"
- 重复以上步骤添加所有变量

---

## ⏭️ 下一步

添加完所有环境变量后:
1. 点击 "Deployments" 查看部署进度
2. 等待构建完成 (约 3-5 分钟)
3. 点击 "Settings" -> "Networking" -> "Generate Domain"
4. 获取访问链接并在浏览器打开

---

## 🎯 提示

- 每次添加/修改环境变量,Railway 会自动重新部署
- 可以在 "Deployments" 页面查看日志排查问题
- 如果构建失败,查看 "Build Logs" 了解原因
