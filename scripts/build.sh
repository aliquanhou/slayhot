#!/bin/bash
# scripts/build.sh 鈥?鏋勫缓 SlayHot 缁勪欢
# 鐢ㄦ硶: bash scripts/build.sh [harness|py|all]

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "馃敤 SlayHot Build Script"
echo "========================"

build_harness() {
    echo ""
    echo "馃摝 鏋勫缓 Go Harness..."

    cd harness

    # 鏋勫缓鍚勫钩鍙?
    echo "  鈫?Windows x64..."
    GOOS=windows GOARCH=amd64 go build -ldflags="-s -w" -o "../@SlayHot/harness-win32-x64/bin/SlayHot.exe" .

    echo "  鈫?macOS ARM64..."
    GOOS=darwin GOARCH=arm64 go build -ldflags="-s -w" -o "../@SlayHot/harness-darwin-arm64/bin/SlayHot" .

    echo "  鈫?Linux x64..."
    GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o "../@SlayHot/harness-linux-x64/bin/SlayHot" .

    cd "$ROOT"
    echo "  鉁?Harness 鏋勫缓瀹屾垚"
}

build_py() {
    echo ""
    echo "馃摝 鏋勫缓 Python 鍖?.."

    # 妫€鏌ヤ緷璧?
    python -c "import anthropic, openai, chromadb, psutil" 2>/dev/null || {
        echo "  鈿狅笍  瀹夎 Python 渚濊禆..."
        pip install anthropic openai chromadb psutil
    }

    # 楠岃瘉瀵煎叆
    python -c "
import sys
sys.path.insert(0, '.')
from agent.core import Agent
from agent.providers import create_provider
from agent.tools import get_all_tools
from agent.prompt import build_system_prompt, PromptContext
print('  鉁?Python 鏍稿績瀵煎叆鎴愬姛')
print(f'  宸ュ叿鏁伴噺: {len(get_all_tools())}')
" || {
        echo "  鉂?Python 鏍稿績楠岃瘉澶辫触"
        exit 1
    }

    cd "$ROOT"
    echo "  鉁?Python 鍖呴獙璇佸畬鎴?
}

case "${1:-all}" in
    harness)
        build_harness
        ;;
    py)
        build_py
        ;;
    all)
        build_py
        build_harness
        ;;
esac

echo ""
echo "鉁?鏋勫缓瀹屾垚"
