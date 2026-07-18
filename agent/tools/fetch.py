"""tools/fetch — 网页抓取工具。

提供 fetch_url 工具，让 SlayHot 具备网页内容抓取能力。
基于 httpx 进行 HTTP 请求，BeautifulSoup 解析 HTML。
"""

from __future__ import annotations

from .registry import tool

try:
    import httpx
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


@tool(
    name="fetch_url",
    description="抓取指定 URL 的网页内容，返回纯文本。支持公开可访问的网页、文档、新闻等。",
    category="web",
    is_readonly=True,
    is_concurrency_safe=True,
    timeout=30.0,
)
def fetch_url(url: str, max_length: int = 10000) -> str:
    """抓取网页内容并返回纯文本。

    Args:
        url: 要抓取的网页 URL（必须公开可访问）
        max_length: 最大返回字符数（默认 10000，最大 50000）

    Returns:
        网页的纯文本内容，或错误信息
    """
    if not HAS_DEPS:
        return "[错误] 需要安装依赖: pip install httpx beautifulsoup4"

    if not url.startswith(("http://", "https://")):
        return "[错误] URL 必须以 http:// 或 https:// 开头"

    max_length = min(max(max_length, 1000), 50000)

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }

        with httpx.Client(timeout=15.0, follow_redirects=True) as client:
            resp = client.get(url, headers=headers)
            resp.raise_for_status()

        # 检测编码
        content_type = resp.headers.get("content-type", "")
        encoding = resp.encoding
        html_text = resp.text

        # 用 BeautifulSoup 提取纯文本
        soup = BeautifulSoup(html_text, "html.parser")

        # 移除无用标签
        for tag in soup(["script", "style", "nav", "header", "footer",
                         "noscript", "iframe", "svg", "form", "input",
                         "button", "select", "textarea"]):
            tag.decompose()

        # 提取标题
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        text = soup.get_text(separator="\n", strip=True)

        # 清理空白行
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = "\n".join(lines)

        # 构建输出
        result = ""
        if title:
            result += f"标题: {title}\n\n"
        result += text

        # 截断
        if len(result) > max_length:
            result = result[:max_length] + f"\n\n... (内容已截断，共 {len(result)} 字符)"

        return result

    except httpx.TimeoutException:
        return f"[超时] 请求 {url} 超时，目标网站响应过慢。"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            return f"[拒绝] HTTP 403 - 目标网站拒绝了请求（反爬虫）。"
        elif e.response.status_code == 404:
            return f"[不存在] HTTP 404 - 页面不存在: {url}"
        elif e.response.status_code >= 500:
            return f"[服务端错误] HTTP {e.response.status_code} - 目标网站服务异常。"
        return f"[HTTP错误] {e.response.status_code}"
    except httpx.ConnectError:
        return f"[连接失败] 无法连接到 {url}，请检查 URL 是否正确。"
    except Exception as e:
        return f"[错误] {type(e).__name__}: {str(e)}"
