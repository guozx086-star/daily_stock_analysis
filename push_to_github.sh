#!/bin/bash
# GitHub 推送脚本

echo "========================================="
echo "📤 推送代码到 GitHub"
echo "========================================="
echo ""
echo "请按照以下步骤操作:"
echo ""
echo "1️⃣ 生成 GitHub Personal Access Token"
echo "   访问: https://github.com/settings/tokens/new"
echo "   - Note: Railway Deployment"
echo "   - Expiration: 90 days (或选择其他)"
echo "   - 勾选权限: repo (所有子项目)"
echo "   - 点击 'Generate token'"
echo "   - ⚠️ 复制生成的 Token (只显示一次!)"
echo ""
echo "2️⃣ 推送代码"
read -p "   准备好后按回车继续..."
echo ""

# 推送代码
echo "正在推送..."
git push origin main

echo ""
echo "========================================="
echo "✅ 推送完成!"
echo "========================================="
echo ""
echo "下一步: 在 Railway 部署"
echo "访问: https://railway.app/"
