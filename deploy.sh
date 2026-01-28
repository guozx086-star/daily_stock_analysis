#!/bin/bash
# ========================================
# 股票分析系统 - 云端一键部署脚本
# ========================================

set -e

echo "========================================="
echo "📦 股票分析系统 - 云端部署向导"
echo "========================================="
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 未检测到 Docker，正在安装..."
    curl -fsSL https://get.docker.com | bash
    systemctl start docker
    systemctl enable docker
    echo "✅ Docker 安装完成"
else
    echo "✅ Docker 已安装"
fi

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ 未检测到 Docker Compose，正在安装..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose 安装完成"
else
    echo "✅ Docker Compose 已安装"
fi

echo ""
echo "========================================="
echo "📝 配置检查"
echo "========================================="

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "❌ 未找到 .env 文件，从 .env.example 复制..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件，填入您的配置："
    echo "   - GEMINI_API_KEY (必填)"
    echo "   - STOCK_LIST (必填)"
    echo "   - FEISHU_WEBHOOK_URL (可选)"
    echo ""
    read -p "按回车键继续..."
fi

# 检查必要配置
if ! grep -q "GEMINI_API_KEY=AIzaSy" .env; then
    echo "⚠️  警告: GEMINI_API_KEY 可能未配置"
fi

if ! grep -q "STOCK_LIST=" .env | grep -v "your_"; then
    echo "⚠️  警告: STOCK_LIST 可能未配置"
fi

echo ""
echo "========================================="
echo "🚀 开始部署"
echo "========================================="

# 创建必要目录
mkdir -p data logs reports

# 构建 Docker 镜像
echo "📦 构建 Docker 镜像..."
docker-compose -f docker/docker-compose.yml build

# 启动服务
echo "🚀 启动服务..."
docker-compose -f docker/docker-compose.yml up -d webui

echo ""
echo "========================================="
echo "✅ 部署完成！"
echo "========================================="
echo ""

# 获取服务器 IP
SERVER_IP=$(curl -s ifconfig.me || echo "localhost")

echo "📱 访问地址:"
echo "   本地: http://localhost:8000"
echo "   远程: http://$SERVER_IP:8000"
echo ""
echo "📊 查看日志:"
echo "   docker-compose -f docker/docker-compose.yml logs -f webui"
echo ""
echo "🔄 重启服务:"
echo "   docker-compose -f docker/docker-compose.yml restart webui"
echo ""
echo "🛑 停止服务:"
echo "   docker-compose -f docker/docker-compose.yml down"
echo ""
echo "========================================="

# 显示实时日志
echo "正在显示服务日志 (Ctrl+C 退出)..."
sleep 2
docker-compose -f docker/docker-compose.yml logs -f webui
