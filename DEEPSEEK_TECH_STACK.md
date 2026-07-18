# SlayHot DeepSeek 鎶€鏈爤鏂囨。

> SlayHot v2.1 鈥?Model + Harness = Agent锛屼笓涓氫负 DeepSeek 鑰岀敓

---

## 鐩綍

1. [璁捐鍝插](#1-璁捐鍝插)
2. [DeepSeek 鍘熺敓闆嗘垚](#2-deepseek-鍘熺敓闆嗘垚)
3. [鍔ㄦ€佹彁绀鸿瘝寮曟搸](#3-鍔ㄦ€佹彁绀鸿瘝寮曟搸)
4. [Provider 閫傞厤灞俔(#4-provider-閫傞厤灞?
5. [Go Harness 鍘熺敓澹冲眰](#5-go-harness-鍘熺敓澹冲眰)
6. [IPC 閫氫俊鍗忚](#6-ipc-閫氫俊鍗忚)
7. [宸ュ叿绯荤粺](#7-宸ュ叿绯荤粺)
8. [鎻掍欢绯荤粺](#8-鎻掍欢绯荤粺)
9. [璁板繂绯荤粺](#9-璁板繂绯荤粺)
10. [宸ヤ綔娴佸紩鎿嶿(#10-宸ヤ綔娴佸紩鎿?
11. [Web GUI](#11-web-gui)
12. [浼氳瘽绠＄悊](#12-浼氳瘽绠＄悊)
13. [鏉冮檺涓庡畨鍏╙(#13-鏉冮檺涓庡畨鍏?
14. [璋冭瘯涓庡彲瑙傛祴鎬(#14-璋冭瘯涓庡彲瑙傛祴鎬?
15. [鏋勫缓涓庡垎鍙慮(#15-鏋勫缓涓庡垎鍙?
16. [璺ㄥ钩鍙版敮鎸乚(#16-璺ㄥ钩鍙版敮鎸?
17. [鎬ц兘鍩哄噯](#17-鎬ц兘鍩哄噯)
18. [涓?DeepSeek 鐨勬渶浣冲疄璺礭(#18-涓?deepseek-鐨勬渶浣冲疄璺?

---

## 1. 璁捐鍝插

### 鏍稿績鍏紡

```
Model (DeepSeek) + Harness (Go Native) = Agent (SlayHot)
```

SlayHot 鐨勬牳蹇冪悊蹇垫槸灏?*澶ц瑷€妯″瀷**涓?*鍘熺敓澹冲眰**娣卞害缁撳悎锛屽垱閫犺嚜涓?AI 鏅鸿兘浣撱€備笌浼犵粺鐨?鑱婂ぉ鏈哄櫒浜?宸ュ叿璋冪敤"涓嶅悓锛孋laudeZ 浠庢灦鏋勫簳灞傚嵆鍥寸粫浠ヤ笅鍘熷垯璁捐锛?

| 鍘熷垯 | 鎻忚堪 |
|------|------|
| **鍔ㄦ€佹彁绀鸿瘝** | 姣忔 LLM 璋冪敤鍓嶆牴鎹綋鍓嶄笂涓嬫枃瀹炴椂鏋勫缓绯荤粺鎻愮ず璇?|
| **鍘熺敓澹冲眰** | Go 缂栧啓鐨勫師鐢?Harness 鎻愪緵杩涚▼绠＄悊銆乀UI銆佽嚜鍔ㄦ洿鏂?|
| **宸ュ叿鍗虫帴鍙?* | 鎵€鏈夎兘鍔涢€氳繃宸ュ叿鏆撮湶锛孡LM 鑷富閫夋嫨璋冪敤 |
| **璁板繂鍒嗗眰** | 鐭湡璁板繂 + 璇箟璁板繂锛圕hromaDB锛変袱绾ц蹇嗘灦鏋?|
| **鎻掍欢鐢熸€?* | 鎻掍欢绯荤粺鏀寔鍔ㄦ€佸彂鐜般€佸姞杞姐€佸嵏杞藉伐鍏?|

### 涓轰粈涔堥€夋嫨 DeepSeek 浣滀负榛樿寮曟搸锛?

SlayHot 鐨勯粯璁ら厤缃€佹彁绀鸿瘝妯℃澘銆侀噸璇曢€昏緫銆佷笂涓嬫枃绐楀彛绠＄悊鍧囬拡瀵?DeepSeek 绯诲垪妯″瀷杩涜浜嗘繁搴︿紭鍖栵細

```
config.json (榛樿):
{
    "provider": "deepseek",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com/v1",
    "max_tokens": 8192,
    "temperature": 0.0
}
```

---

## 2. DeepSeek 鍘熺敓闆嗘垚

### 2.1 榛樿 Provider

SlayHot 浠?DeepSeek 浣滀负棣栭€?LLM Provider锛屼粠涓変釜灞傞潰瀹炵幇娣卞害闆嗘垚锛?

```
鐢ㄦ埛杈撳叆
    鈹?
    鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?  Agent Core (core.py)                       鈹?
鈹?  鈹斺攢 鑷姩閫夋嫨 DeepSeek Provider              鈹?
鈹?      鈹溾攢 deepseek-chat (榛樿)                鈹?
鈹?      鈹溾攢 deepseek-reasoner (鎺ㄧ悊妯″紡)        鈹?
鈹?      鈹斺攢 deepseek-coder (浠ｇ爜妯″紡)           鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

### 2.2 Thinking 妯″紡鎺у埗

DeepSeek 鐨?reasoning/thinking 鑳藉姏鍦?SlayHot 涓緱鍒颁竴绛夋敮鎸侊細

```python
# providers/base.py 鈥?DeepSeek Provider
class DeepSeekProvider(BaseProvider):
    """DeepSeek API 閫傞厤鍣紝鏀寔 thinking 妯″紡鎺у埗銆?""

    def _build_request(self, messages, tools, **kwargs):
        # 鑷姩娉ㄥ叆 thinking 鍙傛暟
        if self.config.get("disable_thinking"):
            payload["thinking"] = {"type": "disabled"}
        else:
            payload["thinking"] = {"type": "enabled", "budget_tokens": 2048}
        return payload
```

**娴佸紡 thinking 浜嬩欢**锛欴eepSeek 鐨?thinking 鍐呭閫氳繃 SSE 瀹炴椂鎺ㄩ€佸埌 Web GUI 鍜?Go TUI锛屼互 馃 鍥炬爣鍖哄垎鏄剧ず锛?

```
馃 Thinking: 璁╂垜鍒嗘瀽涓€涓嬭繖涓棶棰?..
    鈹斺攢 鐢ㄦ埛鎯冲疄鐜颁竴涓?REST API锛岄渶瑕佸厛璁捐鏁版嵁妯″瀷
馃挰 鏍规嵁鎮ㄧ殑闇€姹傦紝鎴戝缓璁娇鐢?FastAPI + SQLAlchemy...
```

### 2.3 DeepSeek API 閰嶇疆

瀹屾暣鐨?DeepSeek API 閰嶇疆椤癸細

| 閰嶇疆椤?| 榛樿鍊?| 璇存槑 |
|--------|--------|------|
| `provider` | `"deepseek"` | LLM 鎻愪緵鍟?|
| `model` | `"deepseek-chat"` | 妯″瀷鍚嶇О |
| `api_key` | `"sk-..."` | API 瀵嗛挜 |
| `base_url` | `"https://api.deepseek.com/v1"` | API 绔偣 |
| `max_tokens` | `8192` | 鏈€澶ц緭鍑?Token |
| `temperature` | `0.0` | 鐢熸垚娓╁害 |
| `timeout` | `3600` | API 瓒呮椂锛堢锛?|
| `disable_thinking` | `true` | 绂佺敤 thinking 妯″紡 |
| `enable_caching` | `false` | 鍚敤璇箟缂撳瓨 |

### 2.4 鎸囨暟閫€閬块噸璇?

閽堝 DeepSeek API 鐨勯檺娴佸拰瓒呮椂鍋氫簡涓撻棬鐨勯噸璇曠瓥鐣ワ細

```python
# providers/base.py
def _call_with_retry(self, payload):
    for attempt in range(self.config.get("max_retries", 3)):
        try:
            return self._do_request(payload)
        except (ConnectionError, TimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
            time.sleep(delay / 1000)
        except HTTPStatusError as e:
            if e.response.status_code == 429:  # Rate limited
                retry_after = int(e.response.headers.get("retry-after", 10))
                time.sleep(retry_after)
```

---

## 3. 鍔ㄦ€佹彁绀鸿瘝寮曟搸

### 3.1 鏋舵瀯

```python
# agent/prompt.py 鈥?姣忔 LLM 璋冪敤鍓嶆墽琛?
class DynamicPromptEngine:
    def build_system_prompt(self, context):
        return "\n".join([
            self._build_persona(context),       # 韬唤瑙掕壊
            self._build_capabilities(context),   # 鑳藉姏鎻忚堪
            self._build_tools(context),          # 宸ュ叿鍒楄〃锛堝疄鏃舵敞鍏ワ級
            self._build_memory(context),         # 璁板繂娉ㄥ叆
            self._build_constraints(context),    # 绾︽潫鏉′欢锛堝姩鎬佺敓鎴愶級
            self._build_adaptations(context),    # 鑷€傚簲璋冩暣
            self._build_workflow_mode(context),  # 宸ヤ綔娴佹ā寮?
        ])
```

### 3.2 鍔ㄦ€佹敞鍏ョ殑鍐呭

| 妯″潡 | 鍐呭 | 鏇存柊棰戠巼 |
|------|------|----------|
| 宸ュ叿鍒楄〃 | 鎵€鏈夊凡娉ㄥ唽宸ュ叿鐨?JSON Schema | 姣忔璋冪敤 |
| 宸ヤ綔娴佹ā寮?| chat / research / coding / debug / agent | 姣忔璋冪敤 |
| 鑷€傚簲璋冩暣 | 鍩轰簬閿欒鐜囥€侀噸澶嶈皟鐢ㄧ殑琛屼负绾︽潫 | 姣忔璋冪敤 |
| 璁板繂娉ㄥ叆 | 璇箟璁板繂 + 鐭湡璁板繂 + 椤圭洰涓婁笅鏂?| 姣忔璋冪敤 |
| 绾︽潫鏉′欢 | 鏉冮檺銆佽秴鏃躲€佽瑷€銆佺姝㈡搷浣?| 姣忔璋冪敤 |

### 3.3 DeepSeek 鐗瑰畾浼樺寲

閽堝 DeepSeek 妯″瀷瀹舵棌鐨勬彁绀鸿瘝妯℃澘浼樺寲锛?

```python
# 閽堝 deepseek-reasoner 鐨勬彁绀鸿瘝妯℃澘
DEEPSEEK_REASONER_SYSTEM = """You are SlayHot, an autonomous AI agent powered by DeepSeek.
You have access to a comprehensive tool system. Think step by step.

宸ュ叿浣跨敤瑙勫垯:
1. 姣忔鎬濊€冨悗锛岄€夋嫨鏈€鍚堥€傜殑宸ュ叿鎵ц
2. 宸ュ叿鎵ц缁撴灉浼氫互 JSON 鏍煎紡杩斿洖
3. 鏍规嵁缁撴灉鍐冲畾涓嬩竴姝ヨ鍔ㄦ垨缁欏嚭鏈€缁堢瓟妗?
"""

# 閽堝 deepseek-coder 鐨勬彁绀鸿瘝妯℃澘
DEEPSEEK_CODER_SYSTEM = """You are SlayHot-Coder, a coding agent powered by DeepSeek.
You excel at code generation, debugging, and refactoring.

浠ｇ爜宸ュ叿:
- read: 璇诲彇鏂囦欢鍐呭
- write: 鍐欏叆鏂囦欢
- edit: 缂栬緫鐜版湁鏂囦欢
- bash: 鎵ц鍛戒护
"""
```

---

## 4. Provider 閫傞厤灞?

### 4.1 缁熶竴鎺ュ彛

```python
class BaseProvider(ABC):
    """鎵€鏈?Provider 鐨勭粺涓€鎶借薄銆?""

    @abstractmethod
    def send_message(self, messages, tools=None, **kwargs) -> Message:
        """鍙戦€佹秷鎭苟鑾峰彇鍥炲銆?""

    @abstractmethod
    def stream_message(self, messages, tools=None, **kwargs) -> Iterator[Chunk]:
        """娴佸紡鍙戦€佹秷鎭€?""

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """璁＄畻 token 鏁伴噺銆?""
```

### 4.2 Provider 瀹炵幇

| Provider | 妯″瀷 | 鐗规€?|
|----------|------|------|
| `DeepSeekProvider` | deepseek-chat, deepseek-reasoner, deepseek-coder | Thinking 鎺у埗銆?192 max_tokens銆丗IM |
| `AnthropicProvider` | claude-sonnet-4, claude-opus-4 | Tool use銆丼treaming銆佺紦瀛?|
| `OpenAIProvider` | gpt-4o, gpt-4o-mini | Function calling銆佽瑙?|

### 4.3 鑷姩娑堟伅搴忓垪淇

閽堝 DeepSeek API 瀵规秷鎭簭鍒楃殑涓ユ牸瑕佹眰锛孭rovider 灞傚疄鐜拌嚜鍔ㄤ慨澶嶏細

```python
def _fix_message_sequence(self, messages):
    """淇娑堟伅搴忓垪锛岀‘淇濈鍚?DeepSeek API 瑕佹眰銆?""
    fixed = []
    for i, msg in enumerate(messages):
        # 纭繚棣栨潯娑堟伅涓?system 鎴?user 瑙掕壊
        if i == 0 and msg["role"] not in ("system", "user"):
            fixed.append({"role": "user", "content": "[Context] " + msg.get("content", "")})
            continue
        # 淇杩炵画鐨?assistant 娑堟伅
        if msg["role"] == "assistant" and i > 0 and messages[i-1]["role"] == "assistant":
            fixed.append({"role": "user", "content": "[Continue]"})
        fixed.append(msg)
    return fixed
```

---

## 5. Go Harness 鍘熺敓澹冲眰

### 5.1 鏋舵瀯鎬昏

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?             Go Harness (main.go)                  鈹?
鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?
鈹? 鈹?  TUI       鈹? 鈹? Watchdog  鈹? 鈹? Updater   鈹? 鈹?
鈹? 鈹?(bubbletea) 鈹? 鈹?(lifecycle)鈹? 鈹? (GitHub)  鈹? 鈹?
鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹? 鈹?
鈹?        鈹?              鈹?              鈹?        鈹?
鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹? 鈹?
鈹? 鈹?           IPC Protocol (stdin/stdout)        鈹? 鈹?
鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?
鈹?                        鈹?                         鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?             Python Core (runner.py)               鈹?
鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?
鈹? 鈹? Agent Loop 鈹? 鈹? Tools   鈹? 鈹? Web GUI     鈹? 鈹?
鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

### 5.2 鎶€鏈鏍?

| 缁勪欢 | 鎶€鏈?| 鐗堟湰 |
|------|------|------|
| TUI 妗嗘灦 | Charmbracelet Bubble Tea | v1.1.0 |
| 缁堢鏍峰紡 | Charmbracelet Lipgloss | v0.13.0 |
| 缁堢妫€娴?| mattn/go-isatty | v0.0.20 |
| IPC 鍗忚 | JSON-RPC 2.0 over stdin/stdout | 鑷畾涔?|
| 杩涚▼绠＄悊 | OS 淇″彿 + 鐪嬮棬鐙楀畾鏃跺櫒 | 鑷畾涔?|

### 5.3 杩涚▼鐪嬮棬鐙?

Watchdog 鎻愪緵鐢熶骇绾ц繘绋嬬敓鍛藉懆鏈熺鐞嗭細

| 鐗规€?| 鍙傛暟 | 璇存槑 |
|------|------|------|
| 鏈€澶ч噸鍚鏁?| 3 娆?| 宕╂簝鍚庤嚜鍔ㄩ噸鍚?|
| 閲嶅惎寤惰繜 | 2 绉?| 閲嶅惎鍓嶇殑绛夊緟鏃堕棿 |
| 鍏抽棴瓒呮椂 | 5 绉?| 浼橀泤鍏抽棴绛夊緟鏃堕棿 |
| 蹇冭烦闂撮殧 | 5 绉?| 瀛愯繘绋嬪仴搴锋鏌?|
| 蹇冭烦瓒呮椂 | 10 绉?| 瓒呮椂瑙﹀彂寮哄埗閲嶅惎 |

### 5.4 Bubble Tea TUI

TUI 鎻愪緵鍒嗗睆鑱婂ぉ椋庢牸鐣岄潰锛?

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? 猓?SlayHot v2.1 鈥?DeepSeek Agent                 鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                                                 鈹?
鈹? 馃挰 浣犲ソ锛佹垜鍙互甯綘瀹屾垚鍚勭浠诲姟...                鈹?
鈹?                                                 鈹?
鈹? 馃洜锔?浣跨敤宸ュ叿: bash                              鈹?
鈹? 鈹斺攢 $ python --version                          鈹?
鈹?    Python 3.12.0                                鈹?
鈹?                                                 鈹?
鈹? 馃 Thinking: 璁╂垜鍒嗘瀽涓€涓?..                     鈹?
鈹?                                                 鈹?
鈹? 鉁?浠诲姟瀹屾垚                                     鈹?
鈹?                                                 鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? Ready           Tools: 5  Errors: 0 鈹?agent 鈹?DS 鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

---

## 6. IPC 閫氫俊鍗忚

### 6.1 鍗忚瑙勮寖

鍩轰簬 JSON-RPC 2.0 鐨勫弻鍚戦€氫俊鍗忚锛?

```json
// 璇锋眰
{"id": 1, "method": "tool_call", "params": {"name": "bash", "args": ["ls"]}}
// 鍝嶅簲
{"id": 1, "result": {"stdout": "file1.txt\nfile2.txt", "exit_code": 0}}
// 浜嬩欢锛堟祦寮忥級
{"method": "event", "params": {"type": "stream", "data": "姝ｅ湪澶勭悊..."}}
// 蹇冭烦
{"id": 2, "method": "ping", "params": {}}
{"id": 2, "result": "pong"}
```

### 6.2 浜嬩欢绫诲瀷

| 浜嬩欢 | 鏂瑰悜 | 璇存槑 |
|------|------|------|
| `MESSAGE_START` | Core 鈫?Harness | 娑堟伅寮€濮?|
| `MESSAGE_DELTA` | Core 鈫?Harness | 娴佸紡鍐呭鍧?|
| `MESSAGE_STOP` | Core 鈫?Harness | 娑堟伅缁撴潫 |
| `TEXT_DELTA` | Core 鈫?Harness | 鏂囨湰澧為噺 |
| `THINKING_DELTA` | Core 鈫?Harness | DeepSeek thinking 鍐呭 |
| `TOOL_START` | Core 鈫?Harness | 宸ュ叿寮€濮嬫墽琛?|
| `TOOL_RESULT` | Core 鈫?Harness | 宸ュ叿鎵ц缁撴灉 |
| `TOOL_ERROR` | Core 鈫?Harness | 宸ュ叿鎵ц閿欒 |
| `SESSION_START` | Core 鈫?Harness | 浼氳瘽寮€濮?|
| `SESSION_END` | Core 鈫?Harness | 浼氳瘽缁撴潫 |
| `PING` | 鍙屽悜 | 蹇冭烦妫€娴?|

### 6.3 Python 渚?Transport

```python
class StdioTransport(Transport):
    """鍩轰簬 stdin/stdout 鐨勪紶杈撳眰瀹炵幇銆?""

    def send(self, data: str):
        with self._lock:
            sys.stdout.write(data + "\n")
            sys.stdout.flush()

    def recv(self, timeout: float = None) -> str | None:
        # Unix: select.select() 闈為樆濉炶鍙?
        # Windows: sys.stdin.readline() 闃诲璇诲彇
```

---

## 7. 宸ュ叿绯荤粺

### 7.1 宸ュ叿娉ㄥ唽

浣跨敤 `@tool` 瑁呴グ鍣ㄥ０鏄庡伐鍏凤細

```python
@tool(
    name="bash",
    description="鎵ц shell 鍛戒护骞惰繑鍥炶緭鍑?,
    readonly=False,
    concurrency_safe=False,
)
def bash_execute(command: str, timeout: int = 30) -> dict:
    """鎵ц bash 鍛戒护銆?""
    result = subprocess.run(command, shell=True, capture_output=True, timeout=timeout)
    return {
        "stdout": result.stdout[-6000:],  # 鎴柇鑷?6000 瀛楃
        "stderr": result.stderr[-6000:],
        "exit_code": result.returncode,
    }
```

### 7.2 鍐呯疆宸ュ叿娓呭崟

| 宸ュ叿 | 璇存槑 | Readonly | 骞跺彂瀹夊叏 |
|------|------|----------|----------|
| `read` | 璇诲彇鏂囦欢鍐呭 | 鉁?| 鉁?|
| `write` | 鍐欏叆鏂囦欢 | 鉂?| 鉂?|
| `edit` | 缂栬緫鏂囦欢锛坉iff 棰勮锛?| 鉂?| 鉂?|
| `bash` | 鎵ц shell 鍛戒护 | 鉂?| 鉂?|
| `glob` | 鏂囦欢妯″紡鍖归厤 | 鉁?| 鉁?|
| `grep` | 鍐呭鎼滅储 | 鉁?| 鉁?|
| `thinking` | 鏄惧紡鎬濊€冩楠?| 鉁?| 鉁?|
| `subagent` | 鍚姩瀛?Agent | 鉂?| 鉁?|
| `web_fetch` | 鑾峰彇缃戦〉鍐呭 | 鉁?| 鉁?|
| `web_search` | 鎼滅储缃戠粶 | 鉁?| 鉁?|

### 7.3 宸ュ叿 Schema

鍩轰簬 Pydantic 鐨?Schema 鏍￠獙锛?

```python
class ToolContext(BaseModel):
    """宸ュ叿鎵ц涓婁笅鏂囥€?""
    working_dir: str = Field(default=".", description="宸ヤ綔鐩綍")
    env: dict[str, str] = Field(default_factory=dict, description="鐜鍙橀噺")
    timeout: int = Field(default=30, description="瓒呮椂绉掓暟")
    session_id: str = Field(default="", description="浼氳瘽 ID")

class ToolResult(BaseModel):
    """宸ュ叿鎵ц缁撴灉銆?""
    success: bool = Field(default=True)
    output: str = Field(default="", max_length=6000)
    error: str | None = Field(default=None)
    metadata: dict = Field(default_factory=dict)
```

---

## 8. 鎻掍欢绯荤粺

### 8.1 鏋舵瀯

```python
PluginManager
鈹溾攢鈹€ discover()          # 鎵弿鎻掍欢鐩綍
鈹溾攢鈹€ load(plugin_id)     # 鍔犺浇鎻掍欢锛堣皟鐢?on_load + 娉ㄥ唽宸ュ叿锛?
鈹溾攢鈹€ unload(plugin_id)   # 鍗歌浇鎻掍欢锛堣皟鐢?on_unload + 娉ㄩ攢宸ュ叿锛?
鈹溾攢鈹€ reload(plugin_id)   # 閲嶆柊鍔犺浇锛坮e-probe 鍚庡埛鏂板伐鍏凤級
鈹溾攢鈹€ execute(id, tool, args)  # 鎵ц鎻掍欢宸ュ叿
鈹斺攢鈹€ get_all_tools()     # 鑾峰彇鎵€鏈夊凡鍚敤鎻掍欢鐨勫伐鍏?
```

### 8.2 鎻掍欢鐩綍缁撴瀯

```
~/.SlayHot/plugins/
鈹溾攢鈹€ builtin/          # 鍐呯疆鎻掍欢锛堥殢 Agent 鍙戝竷锛?
鈹?  鈹斺攢鈹€ host_tools/   # 涓绘満宸ュ叿閾炬帰娴嬫彃浠?
鈹?      鈹溾攢鈹€ manifest.json  # 鎻掍欢鍏冩暟鎹?
鈹?      鈹斺攢鈹€ plugin.py      # 鎻掍欢瀹炵幇
鈹溾攢鈹€ community/        # 绀惧尯鎻掍欢锛堢敤鎴峰畨瑁咃級
鈹斺攢鈹€ user/             # 鐢ㄦ埛鑷畾涔夋彃浠?
```

### 8.3 涓绘満宸ュ叿閾炬帰娴?

鑷姩鎺㈡祴鏈満寮€鍙戝伐鍏烽摼骞舵寕杞戒负 Agent 鍙皟鐢ㄥ伐鍏凤細

| 宸ュ叿 | 鎺㈡祴鍛戒护 | 鐗堟湰妫€娴?|
|------|----------|----------|
| Node.js | `node --version` | v20.11.0 |
| Python | `python --version` | Python 3.12.0 |
| Git | `git --version` | git version 2.40.0 |
| Docker | `docker --version` | Docker version 24.0.2 |
| Go | `go version` | go1.22.0 |
| Java | `java -version` | 17.0.6 |
| Rust | `rustc --version` | rustc 1.70.0 |
| .NET SDK | `dotnet --version` | 7.0.100 |
| Flutter | `flutter --version` | Flutter 3.10.0 |
| 鍏?20+ 宸ュ叿 | 鈥?| 鈥?|

### 8.4 鎻掍欢灞忚斀鏈哄埗

鐢ㄦ埛鍙€氳繃 `.tool_mask.json` 灞忚斀涓嶉渶瑕佺殑宸ュ叿锛?

```json
{
    "masked": ["adb", "aapt2", "zipalign"]
}
```

琚睆钄界殑宸ュ叿鍦?`get_tools()` 涓嚜鍔ㄨ繃婊わ紝涓嶄細娉ㄥ唽鍒?LLM 宸ュ叿鍒楄〃涓€?

---

## 9. 璁板繂绯荤粺

### 9.1 涓ゅ眰璁板繂鏋舵瀯

```
鐭湡璁板繂 (ShortTermMemory)
鈹溾攢鈹€ 浼氳瘽鍐呬簨瀹炲瓨鍌?
鈹溾攢鈹€ 鑷姩鎻愬彇鍏抽敭淇℃伅
鈹斺攢鈹€ 浼氳瘽缁撴潫鏃跺彲閫夋寔涔呭寲

璇箟璁板繂 (SemanticMemory)
鈹溾攢鈹€ ChromaDB 鍚戦噺瀛樺偍
鈹溾攢鈹€ 鐩镐技搴︽绱?(top-k)
鈹斺攢鈹€ 璺ㄤ細璇濊蹇嗘寔涔呭寲
```

### 9.2 鐭湡璁板繂

```python
class ShortTermMemory:
    def __init__(self):
        self.facts: dict[str, str] = {}  # key -> value 浜嬪疄瀛樺偍

    def add_fact(self, key: str, value: str):
        self.facts[key] = value

    def get_context(self) -> str:
        """杩斿洖褰撳墠鐭湡璁板繂鐨勬枃鏈〃绀恒€?""
        if not self.facts:
            return ""
        return "銆愮煭鏈熻蹇嗐€慭n" + "\n".join(
            f"- {k}: {v}" for k, v in self.facts.items()
        )
```

### 9.3 璇箟璁板繂

```python
class SemanticMemory:
    def __init__(self, persist_dir: str = ".SlayHot_memory"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="SlayHot_memory",
            embedding_function=embeddings  # 鍙彃鎷斿祵鍏ユā鍨?
        )

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        return self.collection.query(query_texts=[query], n_results=top_k)

    def store(self, text: str, metadata: dict = None):
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[str(uuid4())]
        )
```

---

## 10. 宸ヤ綔娴佸紩鎿?

### 10.1 鍐呯疆宸ヤ綔娴佹ā寮?

| 妯″紡 | 瑙﹀彂鏂瑰紡 | 璇存槑 |
|------|----------|------|
| `chat` | `python main.py -w chat` | 鑷敱瀵硅瘽妯″紡 |
| `research` | `python main.py -w research` | 娣卞害鐮旂┒妯″紡锛堝姝ユ悳绱?楠岃瘉锛?|
| `coding` | `python main.py -w coding` | 浠ｇ爜寮€鍙戞ā寮忥紙涓ユ牸鏂囦欢鎿嶄綔锛?|
| `debug` | `python main.py -w debug` | 璋冭瘯妯″紡锛堣缁嗘棩蹇?鍒嗘鎵ц锛?|
| `agent` | `python main.py -w agent`锛堥粯璁わ級 | 鍏ㄥ姛鑳?Agent 妯″紡 |

### 10.2 宸ヤ綔娴佸垏鎹?

```python
# workflow.py
class WorkflowEngine:
    def build_prompt(self, mode: str) -> str:
        if mode == "coding":
            return """
## 浠ｇ爜寮€鍙戝伐浣滄祦
1. 鍏堢悊瑙ｉ渶姹?
2. 璁捐浠ｇ爜缁撴瀯
3. 鍒嗘瀹炵幇
4. 娴嬭瘯楠岃瘉
5. 浼樺寲鏀硅繘
"""
        elif mode == "research":
            return """
## 娣卞害鐮旂┒宸ヤ綔娴?
1. 鏄庣‘鐮旂┒闂
2. 鎼滅储澶氫釜鏉ユ簮
3. 浜ゅ弶楠岃瘉淇℃伅
4. 缁煎悎鏁寸悊缁撴灉
5. 寮曠敤鏉ユ簮
"""
```

---

## 11. Web GUI

### 11.1 鎶€鏈爤

| 缁勪欢 | 鎶€鏈?|
|------|------|
| 鍚庣妗嗘灦 | FastAPI |
| 瀹炴椂閫氫俊 | Server-Sent Events (SSE) |
| 鍓嶇 | 鍘熺敓 HTML + CSS + JS |
| 鑷姩寮€娴忚鍣?| Python webbrowser 妯″潡 |

### 11.2 API 绔偣

| 绔偣 | 鏂规硶 | 璇存槑 |
|------|------|------|
| `/` | GET | Web GUI 涓婚〉 |
| `/api/chat` | POST | 鍙戦€佹秷鎭紙娴佸紡鍝嶅簲锛?|
| `/api/tools` | GET | 鑾峰彇宸ュ叿鍒楄〃 |
| `/api/session` | GET | 鑾峰彇浼氳瘽鐘舵€?|
| `/api/config` | GET/PUT | 鑾峰彇/鏇存柊閰嶇疆 |
| `/api/plugins` | GET | 鑾峰彇鎻掍欢鍒楄〃 |
| `/api/plugins/toggle` | POST | 鍚敤/绂佺敤鎻掍欢 |
| `/api/plugins/reload` | POST | 閲嶆柊鍔犺浇鎻掍欢 |
| `/api/logs` | GET | 鑾峰彇璋冭瘯鏃ュ織 |
| `/stream` | GET | SSE 娴佸紡绔偣 |

### 11.3 鍚姩鏂瑰紡

```bash
python main.py --web              # 闅忔満绔彛锛岃嚜鍔ㄥ紑娴忚鍣?
python main.py --web --port 8080  # 鎸囧畾绔彛
# 鎴栧弻鍑?鍚姩WebUI.bat
```

---

## 12. 浼氳瘽绠＄悊

### 12.1 Session 鐢熷懡鍛ㄦ湡

```python
class Session:
    def __init__(self):
        self.id: str = str(uuid4())
        self.messages: list[dict] = []
        self.created_at: float = time.time()
        self.metadata: dict = {}

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_context(self, max_messages: int = 50) -> list[dict]:
        return self.messages[-max_messages:]

    def save(self, path: str):
        """鎸佷箙鍖栦細璇濆埌纾佺洏銆?""
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"id": self.id, "messages": self.messages}, f)
```

### 12.2 涓婁笅鏂囧帇缂?

褰撲笂涓嬫枃鍒╃敤鐜囪秴杩囬槇鍊兼椂鑷姩鍘嬬缉锛?

| 閰嶇疆 | 榛樿鍊?| 璇存槑 |
|------|--------|------|
| `max_context_messages` | 50 | 鏈€澶ф秷鎭暟 |
| `context_compress_at` | 0.85 | 鍘嬬缉瑙﹀彂闃堝€?|
| `compression_strategy` | summary | 鍘嬬缉绛栫暐 |

---

## 13. 鏉冮檺涓庡畨鍏?

### 13.1 鏉冮檺妯″紡

| 妯″紡 | 璇存槑 |
|------|------|
| `auto` | 鑷姩鎵瑰噯宸茬煡瀹夊叏鎿嶄綔 |
| `allow_all` | 鍏佽鎵€鏈夋搷浣?|
| `strict` | 姣忔鎿嶄綔閮介渶瑕佺‘璁?|

### 13.2 瀹¤鏃ュ織

鎵€鏈夊伐鍏疯皟鐢ㄥ拰鏉冮檺鍐崇瓥閮借褰曞埌缁撴瀯鍖栨棩蹇楋細

```python
class PermissionManager:
    def log_decision(self, action: str, tool: str, allowed: bool):
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "tool": tool,
            "allowed": allowed,
            "session_id": self.session.id,
        })
```

---

## 14. 璋冭瘯涓庡彲瑙傛祴鎬?

### 14.1 DebugCollector

```python
class DebugCollector:
    """缁撴瀯鍖栬皟璇曟暟鎹敹闆嗗櫒銆?""
    data = {
        "session": {"id": "...", "model": "deepseek-chat", "version": "2.1"},
        "tool_calls": [],     # 姣忔宸ュ叿璋冪敤鐨勮鎯?
        "decisions": [],      # LLM 鍐崇瓥璁板綍
        "message_flow": [],   # 娑堟伅娴佽褰?
        "api_calls": [],      # API 璋冪敤璁板綍锛堝惈鑰楁椂锛?
    }
```

### 14.2 璋冭瘯闈㈡澘

Web GUI 涓寘鍚皟璇曢潰鏉匡紝鏀寔锛?

| 鍔熻兘 | 璇存槑 |
|------|------|
| 瀹炴椂宸ュ叿璋冪敤鏃ュ織 | 鏌ョ湅姣忔宸ュ叿璋冪敤鐨勮緭鍏ヨ緭鍑?|
| API 璋冪敤鑰楁椂 | 鏌ョ湅姣忔 LLM API 璋冪敤鐨勫欢杩?|
| 娑堟伅娴佸洖鏀?| 鍥炴函瀹屾暣鐨勬秷鎭氦浜掑簭鍒?|
| 涓€閿鍑?| JSON / Markdown 鏍煎紡瀵煎嚭 |

---

## 15. 鏋勫缓涓庡垎鍙?

### 15.1 鏋勫缓鑴氭湰

```bash
# Windows
scripts\build.bat

# Linux/macOS
./scripts/build.sh
```

### 15.2 npm 鍒嗗彂

```json
// @SlayHot/cli/package.json
{
  "name": "@SlayHot/cli",
  "version": "2.1.0",
  "bin": { "SlayHot": "./bin/SlayHot.js" },
  "optionalDependencies": {
    "@SlayHot/harness-win32-x64": "2.1.0",
    "@SlayHot/harness-darwin-arm64": "2.1.0",
    "@SlayHot/harness-linux-x64": "2.1.0"
  }
}
```

### 15.3 骞冲彴浜岃繘鍒?

| 鍖呭悕 | 骞冲彴 | CPU |
|------|------|-----|
| `@SlayHot/harness-win32-x64` | Windows | x64 |
| `@SlayHot/harness-darwin-arm64` | macOS | ARM64 (Apple Silicon) |
| `@SlayHot/harness-linux-x64` | Linux | x64 |

---

## 16. 璺ㄥ钩鍙版敮鎸?

| 鐗规€?| Windows | macOS | Linux |
|------|---------|-------|-------|
| Python Core | 鉁?| 鉁?| 鉁?|
| Go Harness | 鉁?| 鉁?| 鉁?|
| IPC (stdin/stdout) | 鉁?| 鉁?| 鉁?|
| TUI (bubbletea) | 鉁?| 鉁?| 鉁?|
| Web GUI | 鉁?| 鉁?| 鉁?|
| ChromaDB | 鉁?| 鉁?| 鉁?|
| Auto-updater | 鉁?| 鉁?| 鉁?|
| npm install | 鉁?| 鉁?| 鉁?|

---

## 17. 鎬ц兘鍩哄噯

### 17.1 DeepSeek API 鎬ц兘

| 鎸囨爣 | deepseek-chat | deepseek-reasoner |
|------|---------------|-------------------|
| 棣?Token 寤惰繜 | ~300ms | ~500ms |
| 杈撳嚭閫熷害 | ~50 tokens/s | ~30 tokens/s |
| 鏈€澶ц緭鍑?| 8192 tokens | 8192 tokens |
| 涓婁笅鏂囩獥鍙?| 64K tokens | 64K tokens |

### 17.2 宸ュ叿鎵ц寤惰繜

| 宸ュ叿 | 骞冲潎寤惰繜 | P99 寤惰繜 |
|------|----------|----------|
| `read` (100 lines) | 2ms | 5ms |
| `write` (100 lines) | 3ms | 8ms |
| `edit` (diff) | 5ms | 15ms |
| `bash` (simple) | 50ms | 200ms |
| `glob` (100 files) | 10ms | 30ms |
| `grep` (100 files) | 100ms | 500ms |
| `web_fetch` | 500ms | 2000ms |

### 17.3 鍚姩鏃堕棿

| 妯″紡 | 鍐峰惎鍔?| 鐑惎鍔?|
|------|--------|--------|
| CLI | 1.2s | 0.3s |
| Web GUI | 2.5s | 0.5s |
| Harness TUI | 1.5s | 0.4s |

---

## 18. 涓?DeepSeek 鐨勬渶浣冲疄璺?

### 18.1 閰嶇疆鎺ㄨ崘

```json
{
    "provider": "deepseek",
    "model": "deepseek-chat",
    "temperature": 0.0,
    "max_tokens": 8192,
    "disable_thinking": true,
    "retry_base_delay_ms": 1000,
    "max_retries": 3
}
```

### 18.2 妯″瀷閫夋嫨鎸囧崡

| 浠诲姟绫诲瀷 | 鎺ㄨ崘妯″瀷 | 璇存槑 |
|----------|----------|------|
| 閫氱敤瀵硅瘽 | deepseek-chat | 蹇€熴€佺粡娴?|
| 澶嶆潅鎺ㄧ悊 | deepseek-reasoner | 鏇撮暱鎬濊€冩椂闂?|
| 浠ｇ爜鐢熸垚 | deepseek-coder | 浠ｇ爜涓撻」浼樺寲 |
| 浠ｇ爜瀹℃煡 | deepseek-coder | 鎿呴暱鍙戠幇浠ｇ爜闂 |

### 18.3 Token 绠＄悊

```python
# 閽堝 DeepSeek 鐨勪笂涓嬫枃绠＄悊
MAX_TOKENS = 8192
CONTEXT_WINDOW = 65536  # DeepSeek 涓婁笅鏂囩獥鍙?
COMPRESS_THRESHOLD = 0.85  # 85% 瑙﹀彂鍘嬬缉
```

### 18.4 閿欒澶勭悊

| 閿欒绫诲瀷 | 澶勭悊绛栫暐 |
|----------|----------|
| 瓒呮椂 (Timeout) | 鎸囨暟閫€閬块噸璇曪紝鏈€澶?3 娆?|
| 闄愭祦 (429) | 璇诲彇 Retry-After 澶达紝绛夊緟鍚庨噸璇?|
| 杩炴帴閿欒 | 绔嬪嵆閲嶈瘯 1 娆?|
| 璁よ瘉閿欒 (401) | 鍋滄閲嶈瘯锛屾彁绀虹敤鎴锋鏌?API Key |

---

> SlayHot v2.1 鈥?Model (DeepSeek) + Harness (Go Native) = Agent
>
> 鏂囨。鏇存柊: 2026-07-18
