# SlayHot Architecture Guide

## Module Dependency

```
main.py
  鈹溾攢鈹€ agent.cli            (CLI mode)
  鈹溾攢鈹€ agent.core           (Agent main loop)
  鈹?  鈹溾攢鈹€ agent.prompt            (Dynamic prompt engine)
  鈹?  鈹溾攢鈹€ agent.providers         (LLM providers)
  鈹?  鈹溾攢鈹€ agent.session           (Session management)
  鈹?  鈹溾攢鈹€ agent.tools             (Tool system)
  鈹?  鈹溾攢鈹€ agent.memory            (Short-term + Semantic memory)
  鈹?  鈹溾攢鈹€ agent.permissions       (Permission control)
  鈹?  鈹溾攢鈹€ agent.workflow          (Workflow engine)
  鈹?  鈹斺攢鈹€ agent.debug_stream      (Debug logging)
  鈹溾攢鈹€ agent.web_gui.server  (Web GUI)
  鈹斺攢鈹€ harness.runner        (IPC harness mode)
```

## Core Loop Flow

```
run(user_message)
  鈹?  鈹溾攢 session.add_message("user", ...)
  鈹?  鈹斺攢 while _running:
       鈹?       鈹溾攢 messages = session.get_recent_messages()
       鈹?       鈹溾攢 system_prompt = prompt_builder.build(PromptContext{
       鈹?     tools=get_all_tools(),
       鈹?     workflow_mode="agent",
       鈹?     memories=search_memories(),
       鈹?     session_state=get_state(),
       鈹?     constraints={...},
       鈹? })
       鈹?       鈹溾攢 response = provider.chat_with_retry(
       鈹?     system_prompt, messages, tools)
       鈹?       鈹溾攢 if response.tool_calls:
       鈹?   鈹?       鈹?   鈹溾攢 separate concurrency_safe vs serial tools
       鈹?   鈹溾攢 parallel(concurrency_safe)  # ThreadPoolExecutor
       鈹?   鈹溾攢 serial(remaining)
       鈹?   鈹?       鈹?   鈹溾攢 auto-store tool memories
       鈹?   鈹溾攢 session.append(assistant + tool messages)
       鈹?   鈹斺攢 continue
       鈹?       鈹斺攢 else:
            鈹溾攢 auto-store response memory
            鈹斺攢 return response.content
```

## Memory System Architecture

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                 Memory System                       鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?  ShortTermMemory   鈹?     SemanticMemory           鈹?鈹?  (session scope)   鈹?   (ChromaDB vector store)    鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?鈥?facts (key/value) 鈹?鈥?store(content, metadata)    鈹?鈹?鈥?notes (timeline)  鈹?鈥?search(query, top_k)        鈹?鈹?鈥?tags              鈹?鈥?get_recent(limit)           鈹?鈹?鈥?task_stack        鈹?鈥?delete / clear / count      鈹?鈹?鈥?clear()           鈹?鈥?auto-persisted to disk      鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?         鈹?                      鈹?         鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                    鈻?         PromptContext.memories
                    鈹?                    鈻?         _build_memory_block()
                    鈹?                    鈻?         System prompt (dynamic injection)
```

## Web GUI Event Flow

```
Browser                    FastAPI                    Agent
  鈹?                        鈹?                        鈹?  鈹傗攢鈹€GET /api/stream鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈻垛攤                         鈹?  鈹?                        鈹?SSE connection           鈹?  鈹傗梹鈹€鈹€鈹€event: text_delta鈹€鈹€鈹€鈹€鈹傗梹鈹€鈹€鈹€on_stream(chunk)鈹€鈹€鈹€鈹€鈹€鈹?  鈹傗梹鈹€鈹€鈹€event: tool_use_start鈹傗梹鈹€鈹€鈹€on_tool_start()鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹傗梹鈹€鈹€鈹€event: tool_output鈹€鈹€鈹傗梹鈹€鈹€鈹€on_tool_output()鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹傗梹鈹€鈹€鈹€event: tool_result鈹€鈹€鈹傗梹鈹€鈹€鈹€on_tool_call()鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹傗梹鈹€鈹€鈹€event: session_end鈹€鈹€鈹傗梹鈹€鈹€鈹€run() complete鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?                        鈹?                        鈹?  鈹傗攢鈹€POST /api/send鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈻垛攤                         鈹?  鈹傗攢鈹€{"text": "message"}鈹€鈹€鈹€鈹€鈹傗攢鈹€thread: agent.run()鈹€鈹€鈹€鈻垛攤
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Index HTML |
| GET | `/api/stream` | SSE event stream |
| POST | `/api/send` | Send message |
| POST | `/api/stop` | Stop agent |
| POST | `/api/clear` | Clear session |
| GET | `/api/config` | Get config |
| POST | `/api/config` | Set config |
| GET | `/api/context` | Get context |
| GET | `/api/health` | Health check |
| GET | `/api/debug` | Export debug JSON |
| GET | `/api/debug/markdown` | Export debug MD |
| GET | `/api/memory` | Memory stats + recent |
| POST | `/api/memory/search` | Semantic memory search |
| POST | `/api/memory/store` | Store memory |
| POST | `/api/memory/clear` | Clear all memories |
| GET | `/api/plugins` | List plugins + tools |
| POST | `/api/plugins/discover` | Rescan plugins |

## Tool Execution Model

1. LLM returns `tool_calls` with N tools
2. Each tool is classified: `is_concurrency_safe` or serial
3. Concurrency-safe tools (read, glob, grep, web_search, memory_search, memory_stats) 鈫?**ThreadPoolExecutor (max 8 workers)**
4. Serial tools (write, edit, bash, subagent, artifact) 鈫?**sequential execution**
5. Results are assembled in original order and appended to session
6. Memory is auto-stored after tool round

## Extension Points

- **Add a tool**: Create a function with `@tool()` decorator, import in `agent/tools/__init__.py`
- **Add a provider**: Subclass `LLMProvider` in `agent/providers/base.py`, add to `create_provider()`
- **Add a prompt section**: Call `prompt_builder.register_section()` with a builder function
- **Add a plugin**: Create `plugin.py` + `manifest.json` in a plugin directory
- **Add an API endpoint**: Add route handlers in `agent/web_gui/server.py`
