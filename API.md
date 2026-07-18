# SlayHot API Reference (v2.2)

## CLI Interface

```bash
python main.py [options] [message...]
```

| 鍙傛暟 | 璇存槑 |
|------|------|
| `message` | 鐩存帴娑堟伅锛堥潪浜や簰妯″紡锛?|
| `--interactive` | 浜や簰妯″紡 |
| `-m, --model` | 妯″瀷鍚嶇О |
| `-p, --provider` | LLM 鎻愪緵鍟?(anthropic/openai/deepseek) |
| `-w, --workflow` | 宸ヤ綔娴佹ā寮?(chat/research/coding/debug/agent) |
| `--web` | Web GUI 妯″紡锛堥殢鏈虹鍙ｏ紝鑷姩寮€娴忚鍣級 |
| `--web --port 8080` | 鎸囧畾绔彛 |
| `--harness-mode` | Harness IPC 妯″紡 |

## Web GUI API

### SSE 浜嬩欢娴?

```
GET /api/stream
```

SSE 浜嬩欢绫诲瀷锛?

| 浜嬩欢 | 杞借嵎 | 璇存槑 |
|------|------|------|
| `text_delta` | `{"delta": "..."}` | 瀹炴椂鏂囨湰鍧?|
| `thinking_delta` | `{"delta": "..."}` | 鎬濊€冨潡 |
| `tool_use_start` | `{"tool_name": ..., "args_preview": ..., "file_path": ...}` | 宸ュ叿寮€濮?|
| `tool_result` | `{"tool_name": ..., "status": ..., "result": ..., "duration_ms": ...}` | 宸ュ叿缁撴灉 |
| `tool_output` | `{"tool_name": ..., "line": ...}` | 宸ュ叿瀹炴椂杈撳嚭 |
| `session_start` | `{"agent": "SlayHot"}` | 浼氳瘽寮€濮?|
| `session_end` | `{"agent": "SlayHot"}` | 浼氳瘽缁撴潫 |
| `error` | `{"message": ...}` | 閿欒 |
| `ping` | `{"type": "keepalive"}` | 蹇冭烦 |

### REST API

| 鏂规硶 | 璺緞 | 璇存槑 |
|------|------|------|
| `POST` | `/api/send` | 鍙戦€佹秷鎭?`{"text": "..."}` |
| `POST` | `/api/stop` | 缁堟褰撳墠鎵ц |
| `POST` | `/api/clear` | 娓呯┖瀵硅瘽 |
| `GET` | `/api/config` | 鑾峰彇閰嶇疆 |
| `POST` | `/api/config` | 璁剧疆閰嶇疆 |
| `GET` | `/api/context` | 鑾峰彇鐘舵€侊紙busy/provider/model锛?|
| `GET` | `/api/health` | 鍋ュ悍妫€鏌?|
| `GET` | `/api/debug` | 瀵煎嚭璋冭瘯鏃ュ織 JSON |
| `GET` | `/api/debug/markdown` | 瀵煎嚭璋冭瘯鎶ュ憡 Markdown |
| `GET` | `/api/debug/summary` | 鑾峰彇璋冭瘯鎽樿 |
| `GET` | `/{path}` | 闈欐€佹枃浠?|

## Agent API

### `Agent(config, session)`

```python
from agent.core import Agent
from agent.tools.builtin import *

agent = Agent({"provider": "deepseek", "model": "deepseek-chat"})
result = agent.run("浣犵殑闂")
```

#### 鍥炶皟

```python
agent.on_stream = lambda chunk: print(chunk, end="")
agent.on_tool_start = lambda name, args: print(f"馃洜 {name}")
agent.on_tool_call = lambda name, args, result: print(f"  鈫?{result[:50]}")
agent.on_tool_output = lambda name, line: print(f"  [{name}] {line}")
agent.on_thinking = lambda msg: print(f"馃挱 {msg}")
agent.on_content_block = lambda block_type, data: ...
agent.on_error = lambda ctx, err: print(f"鉂?{ctx}: {err}")
```

## IPC 鍗忚

鍩轰簬 stdin/stdout JSON-RPC锛?

```json
// 璇锋眰
{"id": 1, "method": "tool.call", "params": {"name": "read", "args": {...}}}
// 鍝嶅簲
{"id": 1, "result": "..."}
// 浜嬩欢
{"method": "event", "params": {"type": "text_delta", "data": "..."}}
// 娴佸紡鍧?
{"method": "stream", "params": "瀛楃鍧?}
// 蹇冭烦
{"method": "ping"} 鈫?{"id": ..., "result": "pong"}
```
