# Railway 部署说明

本文件包含 Railway 部署所需的配置。

## 环境变量设置

在 Railway 项目设置中添加以下环境变量:

```
GEMINI_API_KEY=AIzaSyCV-2SavzqoGyphV_OEOE7y5OK12NAl2Hg
GEMINI_MODEL=gemini-2.5-flash
STOCK_LIST=688499
WEBUI_ENABLED=true
WEBUI_HOST=0.0.0.0
WEBUI_PORT=8000
SCHEDULE_ENABLED=true
SCHEDULE_TIME=18:00
```

## 可选配置

如需飞书推送,添加:
```
FEISHU_WEBHOOK_URL=你的飞书Webhook地址
```
