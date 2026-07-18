# SlayHot Technical Whitepaper

> Version 2.2 | 2026-07-19
> 
> An open-source autonomous AI agent framework, purpose-built for DeepSeek
> 
> **Model + Harness = Agent** 鈥?Every LLM call gets a fresh, dynamic system prompt.

---

## 鎽樿

SlayHot 鏄竴涓粠闆舵瀯寤虹殑銆佺敓浜х骇 AI Agent 妗嗘灦銆傚畠鎻愬嚭浜?**"鍔ㄦ€佹彁绀鸿瘝寮曟搸"** 鐨勬柊鑼冨紡锛氱郴缁熸彁绀鸿瘝涓嶆槸涓€娆℃€ч厤缃紝鑰屾槸姣忔 LLM 鍐崇瓥鍓嶇殑"鐘舵€佸揩鐓?銆傞厤鍚堝畬鍠勭殑宸ュ叿绯荤粺銆佷細璇濈鐞嗐€佹祦寮忚緭鍑烘灦鏋勫拰 Web GUI锛孋laudeZ 鎻愪緵浜嗕竴涓畬鏁寸殑 AI Agent 鍩虹璁炬柦銆?

---

## 1. 鏍稿績鍒涙柊

### 1.1 鍔ㄦ€佹彁绀鸿瘝寮曟搸 (`agent/prompt.py`)

```python
# 姣忔 LLM 璋冪敤鍓嶅姩鎬佹瀯寤?
system_prompt = prompt_builder.build(PromptContext(
    tools=get_all_tools(),          # 瀹炴椂宸ュ叿鍒楄〃
    workflow_mode="agent",          # 宸ヤ綔娴佹ā寮?
    constraints={...},              # 鍔ㄦ€佺害鏉?
    memories=[...],                 # 璇箟璁板繂
    session_state={...},            # 鑷€傚簲鐘舵€?
))
```

浼犵粺 Agent 浣跨敤闈欐€佺郴缁熸彁绀鸿瘝銆侰laudeZ 姣忔璋冪敤 LLM 鍓嶉噸寤虹郴缁熸彁绀鸿瘝锛屾敞鍏ワ細
- **宸ュ叿鍒楄〃**锛氬綋鍓嶅疄闄呮敞鍐岀殑宸ュ叿
- **宸ヤ綔娴佹ā寮?*锛歝hat / research / coding / debug / agent
- **鑷€傚簲璋冩暣**锛氭牴鎹敊璇巼銆佽疆娆°€侀噸澶嶈皟鐢ㄥ姩鎬佽皟鏁磋涓虹害鏉?
- **璁板繂娉ㄥ叆**锛氳涔夎蹇?+ 鐭湡璁板繂 + 椤圭洰涓婁笅鏂?
- **绾︽潫鏉′欢**锛氭潈闄愩€佽秴鏃躲€佽瑷€銆佺姝㈡搷浣?

### 1.2 ContentBlock 绫诲瀷绯荤粺 (`agent/types.py`)

鍙傝€?Claude Code 鐨勬秷鎭被鍨嬭璁★細

| 绫诲瀷 | 璇存槑 |
|------|------|
| `TextBlock` | 鏅€氭枃鏈?|
| `ThinkingBlock` | 鎬濊€冨潡 |
| `ToolUseBlock` | 宸ュ叿璋冪敤璇锋眰 |
| `ToolResultBlock` | 宸ュ叿鎵ц缁撴灉 |

姣忔潯 `Message` 鍖呭惈澶氫釜 `ContentBlock`锛屽厑璁?text 鍜?tool_use 浜ら敊銆?

### 1.3 缁撴瀯鍖栬皟璇曟棩蹇?(`agent/debug_stream.py`)

鍐呯疆瀹屾暣鐨勮皟璇曟暟鎹敹闆嗗櫒锛?

| 浜嬩欢绫诲瀷 | 鍐呭 |
|---------|------|
| `message_flow` | 姣忚疆 LLM 璋冪敤鐨勬秷鎭揩鐓?|
| `tool_chain` | 宸ュ叿璋冪敤閾捐矾锛堥『搴?鑰楁椂/缁撴灉锛?|
| `agent_decision` | Agent 鍐崇瓥杩囩▼ |
| `api_call` | LLM API 璇锋眰/鍝嶅簲鏃ュ織 |
| `context` | 涓婁笅鏂囩獥鍙ｇ姸鎬?|
| `error` | 閿欒璁板綍 |

鏀寔涓€閿鍑?JSON / Markdown 鏍煎紡銆?

---

## 2. 娑堟伅鍗忚

### 2.1 SSE 浜嬩欢浣撶郴

```
浜嬩欢: text_delta        鈫?瀹炴椂鏂囨湰鍧?
浜嬩欢: thinking_delta    鈫?鎬濊€冨潡
浜嬩欢: tool_use_start    鈫?宸ュ叿璋冪敤寮€濮?
浜嬩欢: tool_result       鈫?宸ュ叿鎵ц缁撴灉
浜嬩欢: tool_output       鈫?宸ュ叿瀹炴椂杈撳嚭锛坆ash 閫愯锛?
浜嬩欢: session_start     鈫?浼氳瘽寮€濮?
浜嬩欢: session_end       鈫?浼氳瘽缁撴潫
浜嬩欢: error             鈫?閿欒
```

### 2.2 娑堟伅鏍煎紡锛圖eepSeek/OpenAI 鍏煎锛?

```
assistant(content="鏂囨湰", tool_calls=[
    {id, type="function", function={name, arguments}}
])
  鈫?
tool(tool_call_id=id, content="缁撴灉")
tool(tool_call_id=id, content="缁撴灉")
  鈫?
assistant(content="瀹屾垚")
```

### 2.3 娑堟伅搴忓垪鑷姩淇

鍦?API 璋冪敤鍓嶆墽琛屼笁灞傞槻鎶わ細

1. **`_clean_session()`** 鈥?姣忔 `run()` 寮€濮嬪墠娓呯悊瀛ょ珛娑堟伅
2. **`_auto_fix_messages()`** 鈥?鑷姩淇锛氱Щ闄ゅ绔?tool_calls銆佺Щ鍔ㄦ彃闃?user 娑堟伅
3. **`_validate_and_strip()`** 鈥?鏈€缁堥槻绾匡細妫€娴嬪埌浠讳綍瀛ょ珛娑堟伅鍥為€€鍒板畨鍏ㄧ姸鎬?

---

## 3. 宸ュ叿绯荤粺

### 3.1 娉ㄥ唽妯″紡

```python
@tool(category="file", timeout=30, is_readonly=True, is_concurrency_safe=True)
def read(file_path: str, head: int = 0, tail: int = 0) -> str:
    """璇诲彇鏂囦欢鍐呭銆?""
    ...
```

### 3.2 宸ュ叿灞炴€?

| 灞炴€?| 璇存槑 |
|------|------|
| `is_readonly` | 鍙鏍囪锛堢敤浜庢潈闄愭帶鍒讹級 |
| `is_concurrency_safe` | 鍙苟鍙戞墽琛?|
| `require_confirmation` | 闇€瑕佺敤鎴风‘璁?|
| `timeout` | 瓒呮椂绉掓暟 |
| `result_truncate` | 缁撴灉鎴柇闀垮害锛堥粯璁?000锛?|

### 3.3 鍐呯疆宸ュ叿锛?4涓級

| 宸ュ叿 | 鍒嗙被 | 鍙 | 骞跺彂瀹夊叏 |
|------|------|------|---------|
| `read` | file | 鉁?| 鉁?|
| `write` | file | 鉂?| 鉂?|
| `edit` | file | 鉂?| 鉂?|
| `glob` | file | 鉁?| 鉁?|
| `grep` | file | 鉁?| 鉁?|
| `bash` | shell | 鉂?| 鉂?|
| `web` | web | 鉁?| 鉁?|
| `web_search` | web | 鉁?| 鉁?|
| `process` | system | 鉁?| 鉁?|
| `monitor` | system | 鉁?| 鉁?|
| `subagent` | agent | 鉂?| 鉂?|
| `artifact` | artifact | 鉂?| 鉂?|
| `workflow` | workflow | 鉂?| 鉂?|
| `webhook` | webhook | 鉂?| 鉂?|

### 3.4 娴佸紡杈撳嚭

Bash 宸ュ叿浣跨敤 `subprocess.Popen` + 閫愯璇诲彇锛岄€氳繃 `threading.local` 鍥炶皟瀹炴椂鎺ㄩ€佽緭鍑鸿鍒?UI銆?

Edit 宸ュ叿鍦ㄦ浛鎹㈠墠鎺ㄩ€?diff 棰勮锛堟枃浠惰矾寰勩€佽鍙枫€佹棫/鏂拌锛夈€?

---

## 4. Provider 閫傞厤灞?

### 4.1 缁熶竴鎺ュ彛

```python
class LLMProvider(ABC):
    def chat(system_prompt, messages, tools) -> LLMResponse
    def chat_with_retry(system_prompt, messages, tools) -> LLMResponse
```

### 4.2 閿欒鍒嗙被涓庨噸璇?

```
                    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
                    鈹? API 閿欒     鈹?
                    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?
                           鈹?
              鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
              鈻?           鈻?           鈻?
        鍙噸璇?          涓婁笅鏂囪秴闀?     涓嶅彲閲嶈瘯
     (429/500/502/503)  (鍘嬬缉鍚庨噸璇?   (401/400)
        鎸囨暟閫€閬?            鈹?           鈹?
        甯︽姈鍔?             鈻?           鈻?
                       鍘嬬缉鎴愬姛?      杩斿洖閿欒
                         鈹?
                         鈻?
                       閲嶈瘯
```

### 4.3 DeepSeek 鐗规畩閫傞厤

- **thinking 妯″紡鍏抽棴**锛氶€氳繃 `extra_body={"thinking": {"type": "disabled"}}` 鑺傜渷 token
- **tool_choice**: 榛樿 `"auto"` 鎺ㄥ姩妯″瀷璋冪敤宸ュ叿
- **娴佸紡宸ュ叿璋冪敤**锛歚delta.tool_calls` 閫愬潡绱Н JSON 鍙傛暟

---

## 5. Web GUI

### 5.1 鏋舵瀯

```
FastAPI 鍚庡彴
  鈹溾攢 SSE /api/stream 鈫?瀹炴椂浜嬩欢鎺ㄩ€?
  鈹溾攢 POST /api/send  鈫?娑堟伅鍙戦€?
  鈹溾攢 POST /api/stop  鈫?缁堟
  鈹溾攢 GET /api/debug  鈫?璋冭瘯鏃ュ織瀵煎嚭
  鈹斺攢 GET /{path}     鈫?闈欐€佹枃浠?

鍓嶇 (Vanilla JS)
  鈹溾攢 Canvas 绮掑瓙鑳屾櫙
  鈹溾攢 SSE EventSource 鎺ユ敹
  鈹溾攢 Markdown 娓叉煋
  鈹溾攢 鍐呰仈 Diff 鏄剧ず
  鈹溾攢 宸ュ叿鐘舵€侀潰鏉?
  鈹溾攢 浜嬩欢鏃ュ織闈㈡澘
  鈹斺攢 璋冭瘯鎶ュ憡闈㈡澘
```

### 5.2 浜嬩欢娴?

```
WebStreamHandler (server.py)
  鈹溾攢 on_text()        鈫?SSE "text_delta"
  鈹溾攢 on_thinking()    鈫?SSE "thinking_delta"
  鈹溾攢 on_tool_start()  鈫?SSE "tool_use_start"
  鈹溾攢 on_tool_result() 鈫?SSE "tool_result"
  鈹溾攢 on_tool_output() 鈫?SSE "tool_output"
  鈹斺攢 on_error()       鈫?SSE "error"
```

---

## 6. 宸ヤ綔娴佸紩鎿?(`agent/workflow.py`)

- **搴忓垪鍖?鍙嶅簭鍒楀寲**: JSON 鏍煎紡瀛樺偍鍒扮鐩?
- **妫€鏌ョ偣**: 鑷姩淇濆瓨姣?N 姝?
- **鎭㈠鎵ц**: `WorkflowResumer` 浠庢鏌ョ偣鎭㈠
- **杩涘害杩借釜**: 姣忔 pending/running/completed/failed/skipped

---

## 7. 璁板繂绯荤粺

### 7.1 鐭湡璁板繂 (`agent/memory/short_term.py`)
浼氳瘽鍐呬簨瀹炲瓨鍌紝鍩轰簬瀛楀吀鐨勯敭鍊煎锛屾敮鎸佹爣绛炬绱€?

### 7.2 璇箟璁板繂 (`agent/memory/semantic.py`)
鍩轰簬 ChromaDB 鐨勫悜閲忓瓨鍌紝閫氳繃璇箟鐩镐技搴︽悳绱㈢浉鍏宠蹇嗭紝鑷姩娉ㄥ叆鎻愮ず璇嶃€?

---

## 8. 鏉冮檺涓庡畨鍏?(`agent/permissions.py`)

| 妯″紡 | 琛屼负 |
|------|------|
| `auto` | 鑷姩鎵瑰噯鎵€鏈夋搷浣?|
| `ask` | 璇㈤棶鐢ㄦ埛纭淇敼鎿嶄綔 |
| `deny` | 鎷掔粷鎵€鏈夋搷浣?|
| `readonly` | 鍙厑璁稿彧璇绘搷浣?|

鎵€鏈夊叧閿搷浣滆褰曚笉鍙彉瀹¤鏃ュ織锛圝SONL 鏂囦欢锛夈€?

---

## 9. 娴嬭瘯瑕嗙洊

杩愯 `python tests/run_all.py` 鎵ц 9 椤规祴璇曪細

| 妯″潡 | 娴嬭瘯椤?|
|------|--------|
| 妯″潡瀵煎叆 | 鎵€鏈夋ā鍧?import 鎴愬姛 |
| 閰嶇疆鍔犺浇 | config.json 璇诲彇 |
| 宸ュ叿娉ㄥ唽琛?| 14 涓伐鍏?+ OpenAI/Anthropic 鏍煎紡 |
| 鍔ㄦ€佹彁绀鸿瘝 | 5 绉嶅伐浣滄祦妯″紡 |
| 浼氳瘽绠＄悊 | 搴忓垪鍖?鍙嶅簭鍒楀寲/鎸佷箙鍖?|
| Provider 灞?| 宸ュ巶/閲嶈瘯/閫€閬?|
| IPC 鍗忚 | 娑堟伅搴忓垪鍖?|
| 宸ヤ綔娴佸紩鎿?| 鍒涘缓/鎵ц/搴忓垪鍖?鎭㈠ |
| 璁板繂绯荤粺 | 鐭湡璁板繂璇诲啓 |

---

## 10. 鎬ц兘鎸囨爣

| 鎸囨爣 | 鍊?|
|------|-----|
| 宸ュ叿鏁伴噺 | 14 涓唴缃伐鍏?|
| API 璋冪敤鑰楁椂 | ~1.5-5s/娆★紙DeepSeek锛?|
| 宸ュ叿鎵ц鑰楁椂 | ~50ms-10s锛堝彇鍐充簬宸ュ叿锛?|
| 涓婁笅鏂囩獥鍙?| 鍙厤缃紙榛樿 50 鏉★級 |
| 鏈€澶у伐鍏疯皟鐢ㄦ鏁?| 鍙厤缃紙榛樿 50锛?|

---

## 鍙傝€冩枃鐚?

- [Claude Code 鏋舵瀯璁捐](https://github.com/6551Team/claude-code-design-guide/blob/main/part3/08-message-loop.md)
- [Agent SDK 娴佸紡杈撳嚭鏂囨。](https://code.claude.com/docs/zh-CN/agent-sdk/streaming-output)
- [deepseek-harness](https://github.com/HenryZ838978/deepseek-harness) 鈥?DeepSeek V4 鍗忚鐗规€?
