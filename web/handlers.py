# -*- coding: utf-8 -*-
"""
===================================
Web 处理器层 - 请求处理
===================================

职责：
1. 处理各类 HTTP 请求
2. 调用服务层执行业务逻辑
3. 返回响应数据

处理器分类：
- PageHandler: 页面请求处理
- ApiHandler: API 接口处理
"""

from __future__ import annotations

import json
import re
import logging
from http import HTTPStatus
from datetime import datetime
from typing import Dict, Any, TYPE_CHECKING

from web.services import get_config_service, get_analysis_service
from web.templates import render_config_page
from src.enums import ReportType

if TYPE_CHECKING:
    from http.server import BaseHTTPRequestHandler

logger = logging.getLogger(__name__)


# ============================================================
# 响应辅助类
# ============================================================

class Response:
    """HTTP 响应封装"""
    
    def __init__(
        self,
        body: bytes,
        status: HTTPStatus = HTTPStatus.OK,
        content_type: str = "text/html; charset=utf-8"
    ):
        self.body = body
        self.status = status
        self.content_type = content_type
    
    def send(self, handler: 'BaseHTTPRequestHandler') -> None:
        """发送响应到客户端"""
        handler.send_response(self.status)
        handler.send_header("Content-Type", self.content_type)
        handler.send_header("Content-Length", str(len(self.body)))
        handler.end_headers()
        handler.wfile.write(self.body)


class JsonResponse(Response):
    """JSON 响应封装"""
    
    def __init__(
        self,
        data: Dict[str, Any],
        status: HTTPStatus = HTTPStatus.OK
    ):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        super().__init__(
            body=body,
            status=status,
            content_type="application/json; charset=utf-8"
        )


class HtmlResponse(Response):
    """HTML 响应封装"""
    
    def __init__(
        self,
        body: bytes,
        status: HTTPStatus = HTTPStatus.OK
    ):
        super().__init__(
            body=body,
            status=status,
            content_type="text/html; charset=utf-8"
        )


# ============================================================
# 页面处理器
# ============================================================

class PageHandler:
    """页面请求处理器"""
    
    def __init__(self):
        self.config_service = get_config_service()
    
    def handle_index(self) -> Response:
        """处理首页请求 GET /"""
        stock_list = self.config_service.get_stock_list()
        env_filename = self.config_service.get_env_filename()
        body = render_config_page(stock_list, env_filename)
        return HtmlResponse(body)
    
    def handle_update(self, form_data: Dict[str, list]) -> Response:
        """
        处理配置更新 POST /update
        
        Args:
            form_data: 表单数据
        """
        stock_list = form_data.get("stock_list", [""])[0]
        normalized = self.config_service.set_stock_list(stock_list)
        env_filename = self.config_service.get_env_filename()
        body = render_config_page(normalized, env_filename, message="已保存")
        return HtmlResponse(body)


# ============================================================
# API 处理器
# ============================================================

class ApiHandler:
    """API 请求处理器"""
    
    def __init__(self):
        self.analysis_service = get_analysis_service()
    
    def handle_health(self) -> Response:
        """
        健康检查 GET /health
        
        返回:
            {
                "status": "ok",
                "timestamp": "2026-01-19T10:30:00",
                "service": "stock-analysis-webui"
            }
        """
        data = {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "service": "stock-analysis-webui"
        }
        return JsonResponse(data)
    
    def handle_analysis(self, query: Dict[str, list]) -> Response:
        """
        触发股票分析 GET /analysis?code=xxx
        
        Args:
            query: URL 查询参数
            
        返回:
            {
                "success": true,
                "message": "分析任务已提交",
                "code": "600519",
                "task_id": "600519_20260119_103000"
            }
        """
        # 获取股票代码参数
        code_list = query.get("code", [])
        if not code_list or not code_list[0].strip():
            return JsonResponse(
                {"success": False, "error": "缺少必填参数: code (股票代码)"},
                status=HTTPStatus.BAD_REQUEST
            )
        
        code = code_list[0].strip()

        # 验证股票代码格式：A股(6位数字) / 港股(hk+5位数字) / 美股(1-5个大写字母)
        code = code.lower()
        is_a_stock = re.match(r'^\d{6}$', code)
        is_hk_stock = re.match(r'^hk\d{5}$', code)
        is_us_stock = re.match(r'^[A-Z]{1,5}(\.[A-Z])?$', code.upper())

        if not (is_a_stock or is_hk_stock or is_us_stock):
            return JsonResponse(
                {"success": False, "error": f"无效的股票代码格式: {code} (A股6位数字 / 港股hk+5位数字 / 美股1-5个字母)"},
                status=HTTPStatus.BAD_REQUEST
            )
        
        # 获取报告类型参数（默认精简报告）
        report_type_str = query.get("report_type", ["simple"])[0]
        report_type = ReportType.from_str(report_type_str)
        
        # 提交异步分析任务
        try:
            result = self.analysis_service.submit_analysis(code, report_type=report_type)
            return JsonResponse(result)
        except Exception as e:
            logger.error(f"[ApiHandler] 提交分析任务失败: {e}")
            return JsonResponse(
                {"success": False, "error": f"提交任务失败: {str(e)}"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
    
    def handle_tasks(self, query: Dict[str, list]) -> Response:
        """
        查询任务列表 GET /tasks
        
        Args:
            query: URL 查询参数 (可选 limit)
            
        返回:
            {
                "success": true,
                "tasks": [...]
            }
        """
        limit_list = query.get("limit", ["20"])
        try:
            limit = int(limit_list[0])
        except ValueError:
            limit = 20
        
        tasks = self.analysis_service.list_tasks(limit=limit)
        return JsonResponse({"success": True, "tasks": tasks})
    
    def handle_task_status(self, query: Dict[str, list]) -> Response:
        """
        查询单个任务状态 GET /task?id=xxx

        Args:
            query: URL 查询参数
        """
        task_id_list = query.get("id", [])
        if not task_id_list or not task_id_list[0].strip():
            return JsonResponse(
                {"success": False, "error": "缺少必填参数: id (任务ID)"},
                status=HTTPStatus.BAD_REQUEST
            )

        task_id = task_id_list[0].strip()
        task = self.analysis_service.get_task_status(task_id)

        if task is None:
            return JsonResponse(
                {"success": False, "error": f"任务不存在: {task_id}"},
                status=HTTPStatus.NOT_FOUND
            )

        return JsonResponse({"success": True, "task": task})

    def handle_report(self, query: Dict[str, list]) -> Response:
        """
        获取Markdown报告内容 GET /report?id=xxx

        Args:
            query: URL 查询参数

        返回:
            HTML格式的Markdown报告
        """
        task_id_list = query.get("id", [])
        if not task_id_list or not task_id_list[0].strip():
            return JsonResponse(
                {"success": False, "error": "缺少必填参数: id (任务ID)"},
                status=HTTPStatus.BAD_REQUEST
            )

        task_id = task_id_list[0].strip()
        task = self.analysis_service.get_task_status(task_id)

        if task is None:
            return HtmlResponse(
                b"<html><body><h1>Error 404</h1><p>Task not found</p></body></html>",
                status=HTTPStatus.NOT_FOUND
            )

        # 获取报告路径
        result = task.get('result', {})
        report_path = result.get('report_path')

        if not report_path:
            return HtmlResponse(
                b"<html><body><h1>Error 404</h1><p>Report file not found</p></body></html>",
                status=HTTPStatus.NOT_FOUND
            )

        # 读取Markdown文件
        try:
            import os
            if not os.path.isabs(report_path):
                report_path = os.path.join(os.getcwd(), report_path)

            with open(report_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            # 转换Markdown为HTML
            try:
                import markdown
                html_content = markdown.markdown(
                    markdown_content,
                    extensions=['tables', 'fenced_code', 'nl2br']
                )
            except ImportError:
                # 如果没有markdown库，简单转换
                html_content = f"<pre>{markdown_content}</pre>"

            # 生成完整HTML页面
            from web.templates import render_base
            full_html = render_base(
                title=f"分析报告 - {result.get('name', '')}({result.get('code', '')})",
                content=f"""
                <div style="max-width: 100%; width: 100%; margin: 0; padding: 10px; background: white;">
                    <div style="margin-bottom: 15px; padding: 10px 5px;">
                        <a href="/" style="color: #2563eb; text-decoration: none; font-size: 14px;">← 返回首页</a>
                    </div>
                    <div class="markdown-body">
                        {html_content}
                    </div>
                </div>
                """,
                extra_css="""
                /* 覆盖基础 body 样式 - 报告页面全宽显示 */
                body {
                    display: block !important;
                    min-height: auto !important;
                    justify-content: normal !important;
                    align-items: normal !important;
                    padding: 0 !important;
                    overflow-x: hidden;
                    background: #f8f9fa;
                }

                /* 基础样式 */
                .markdown-body {
                    line-height: 1.6;
                    color: #333;
                    font-size: 14px;
                    padding: 10px 5px;
                }
                .markdown-body h1, .markdown-body h2, .markdown-body h3 { margin-top: 1.2em; margin-bottom: 0.5em; font-weight: 600; }
                .markdown-body h1 { font-size: 1.5em; border-bottom: 2px solid #2563eb; padding-bottom: 0.3em; }
                .markdown-body h2 { font-size: 1.25em; border-bottom: 1px solid #eee; padding-bottom: 0.3em; }
                .markdown-body h3 { font-size: 1.1em; }
                .markdown-body p { margin-bottom: 0.8em; }

                /* 列表样式 */
                .markdown-body ul, .markdown-body ol { padding-left: 1.2em; margin-bottom: 0.8em; }
                .markdown-body li { margin-bottom: 0.3em; }

                /* 引用块 */
                .markdown-body blockquote { padding: 0.5em 1em; margin: 1em 0; border-left: 4px solid #2563eb; background: #f0f7ff; border-radius: 0 4px 4px 0; }

                /* 代码块 */
                .markdown-body code { padding: 0.15em 0.35em; background: #f5f5f5; border-radius: 3px; font-family: 'SF Mono', Monaco, 'Courier New', monospace; font-size: 0.9em; color: #e83e8c; }
                .markdown-body pre { padding: 0.8em; background: #f8f9fa; border-radius: 5px; overflow-x: auto; margin: 1em 0; font-size: 0.85em; }

                /* 表格样式 - 移动端优化 */
                .markdown-body table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.85em; }
                .markdown-body table th, .markdown-body table td { border: 1px solid #ddd; padding: 6px 8px; text-align: left; word-wrap: break-word; }
                .markdown-body table th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-weight: 600; }
                .markdown-body table tr:nth-child(even) { background-color: #f8f9fa; }
                .markdown-body table tr:hover { background-color: #e9ecef; }

                /* 横线 */
                .markdown-body hr { border: none; border-top: 2px solid #eee; margin: 1.5em 0; }

                /* 响应式设计 - 移动端优化 */
                @media (max-width: 768px) {
                    .markdown-body { font-size: 13px; }
                    .markdown-body h1 { font-size: 1.3em; }
                    .markdown-body h2 { font-size: 1.15em; }
                    .markdown-body h3 { font-size: 1em; }
                    .markdown-body table { font-size: 0.8em; }
                    .markdown-body table th, .markdown-body table td { padding: 5px 6px; }
                    .markdown-body pre { padding: 0.6em; font-size: 0.8em; }
                    .markdown-body blockquote { padding: 0.4em 0.8em; margin: 0.8em 0; }
                    .markdown-body ul, .markdown-body ol { padding-left: 1em; }
                }

                /* 超小屏幕优化 */
                @media (max-width: 480px) {
                    .markdown-body { font-size: 12px; }
                    .markdown-body h1 { font-size: 1.2em; }
                    .markdown-body h2 { font-size: 1.1em; }
                    .markdown-body h3 { font-size: 1em; }
                    .markdown-body table { font-size: 0.75em; display: block; overflow-x: auto; }
                    .markdown-body table th, .markdown-body table td { padding: 4px 5px; }
                    .markdown-body p { margin-bottom: 0.6em; }
                }
                """
            )

            return HtmlResponse(full_html.encode('utf-8'))

        except FileNotFoundError:
            return HtmlResponse(
                b"<html><body><h1>Error 404</h1><p>Report file not found on disk</p></body></html>",
                status=HTTPStatus.NOT_FOUND
            )
        except Exception as e:
            logger.error(f"[ApiHandler] 读取报告文件失败: {e}")
            return HtmlResponse(
                f"<html><body><h1>Error 500</h1><p>Failed to read report: {str(e)}</p></body></html>".encode('utf-8'),
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )


# ============================================================
# Bot Webhook 处理器
# ============================================================

class BotHandler:
    """
    机器人 Webhook 处理器
    
    处理各平台的机器人回调请求。
    """
    
    def handle_webhook(self, platform: str, form_data: Dict[str, list], headers: Dict[str, str], body: bytes) -> Response:
        """
        处理 Webhook 请求
        
        Args:
            platform: 平台名称 (feishu, dingtalk, wecom, telegram)
            form_data: POST 数据（已解析）
            headers: HTTP 请求头
            body: 原始请求体
            
        Returns:
            Response 对象
        """
        try:
            from bot.handler import handle_webhook
            from bot.models import WebhookResponse
            
            # 调用 bot 模块处理
            webhook_response = handle_webhook(platform, headers, body)
            
            # 转换为 web 响应
            return JsonResponse(
                webhook_response.body,
                status=HTTPStatus(webhook_response.status_code)
            )
            
        except ImportError as e:
            logger.error(f"[BotHandler] Bot 模块未正确安装: {e}")
            return JsonResponse(
                {"error": "Bot module not available"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"[BotHandler] 处理 {platform} Webhook 失败: {e}")
            return JsonResponse(
                {"error": str(e)},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )


# ============================================================
# 处理器工厂
# ============================================================

_page_handler: PageHandler | None = None
_api_handler: ApiHandler | None = None
_bot_handler: BotHandler | None = None


def get_page_handler() -> PageHandler:
    """获取页面处理器实例"""
    global _page_handler
    if _page_handler is None:
        _page_handler = PageHandler()
    return _page_handler


def get_api_handler() -> ApiHandler:
    """获取 API 处理器实例"""
    global _api_handler
    if _api_handler is None:
        _api_handler = ApiHandler()
    return _api_handler


def get_bot_handler() -> BotHandler:
    """获取 Bot 处理器实例"""
    global _bot_handler
    if _bot_handler is None:
        _bot_handler = BotHandler()
    return _bot_handler
