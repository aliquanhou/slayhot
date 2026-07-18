// SlayHot Harness 鈥?鍘熺敓澹冲眰
//
// 鏂囨。瀵归綈锛欳laude Code Harness 鏍稿績宸ヤ綔鍘熺悊
// 鏋舵瀯锛欸o Harness 鈫?stdin/stdout JSON-RPC 鈫?Python Core
//
// 鑱岃矗锛?
//   1. 杩涚▼鐢熷懡鍛ㄦ湡绠＄悊锛堢湅闂ㄧ嫍 + 鑷姩閲嶅惎锛?
//   2. 缁堢 TUI 娓叉煋锛坆ubbletea 鍒嗗睆锛?
//   3. IPC 閫氫俊锛坰tdin/stdout JSON-RPC + 娴佸紡浜嬩欢锛?
//   4. 鑷姩鏇存柊妫€鏌?
//   5. 骞冲彴鍒嗗彂鍏ュ彛

package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"os/exec"
	"os/signal"
	"path/filepath"
	"runtime"
	"strings"
	"sync"
	"syscall"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/mattn/go-isatty"

	"github.com/SlayHot/harness/lifecycle"
	"github.com/SlayHot/harness/tui"
	"github.com/SlayHot/harness/updater"
)

// 鈹€鈹€ 鐗堟湰淇℃伅 鈹€鈹€

const (
	Version    = "2.1.0"
	Codename   = "SlayHot"
	BuildDate  = "2026-07-17"
)

// 鈹€鈹€ 鍏ㄥ眬鐘舵€?鈹€鈹€

var (
	logFile    *os.File
	logger     *logWriter
	uiModel    *tui.Model
	watchdog   *lifecycle.Watchdog
	updChecker *updater.Checker
	program    *tea.Program
)

// 鈹€鈹€ 鏃ュ織 鈹€鈹€

type logWriter struct {
	mu     sync.Mutex
	file   *os.File
	prefix string
}

func newLogWriter(path string) (*logWriter, error) {
	f, err := os.OpenFile(path, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		return nil, err
	}
	return &logWriter{file: f, prefix: time.Now().Format("2006-01-02")}, nil
}

func (l *logWriter) write(level, msg string) {
	l.mu.Lock()
	defer l.mu.Unlock()
	t := time.Now().Format("15:04:05.000")
	fmt.Fprintf(l.file, "[%s] [%s] %s\n", t, level, msg)
}

func (l *logWriter) Info(msg string)  { l.write("INFO", msg) }
func (l *logWriter) Warn(msg string)  { l.write("WARN", msg) }
func (l *logWriter) Error(msg string) { l.write("ERROR", msg) }

func (l *logWriter) Close() { l.file.Close() }

// 鈹€鈹€ 鍏ュ彛 鈹€鈹€

func main() {
	// 鈹€鈹€ 瑙ｆ瀽鍙傛暟 鈹€鈹€
	args := os.Args[1:]

	if len(args) > 0 {
		switch args[0] {
		case "--version", "-v":
			fmt.Printf("%s Harness v%s (%s) %s/%s\n",
				Codename, Version, BuildDate, runtime.GOOS, runtime.GOARCH)
			return
		case "--help", "-h":
			printHelp()
			return
		case "--standalone":
			runStandalone(args[1:])
			return
		}
	}

	// 鈹€鈹€ 鍒濆鍖栨棩蹇?鈹€鈹€
	logDir := filepath.Join(homeDir(), ".SlayHot", "logs")
	os.MkdirAll(logDir, 0755)
	logPath := filepath.Join(logDir, fmt.Sprintf("harness-%s.log",
		time.Now().Format("20060102")))
	lw, err := newLogWriter(logPath)
	if err == nil {
		logger = lw
		defer logger.Close()
		logInfo("Harness v%s starting", Version)
	}
	logInfo("Platform: %s/%s", runtime.GOOS, runtime.GOARCH)
	logInfo("Args: %v", args)

	// 鈹€鈹€ 鏇存柊妫€鏌ワ紙鍚庡彴锛?鈹€鈹€
	go checkUpdate()

	// 鈹€鈹€ 鍒濆鍖?TUI 鈹€鈹€
	uiModel = tui.NewModel()
	uiModel.SetModelName(getDefaultModel())

	// 鈹€鈹€ 缁戝畾淇″彿 鈹€鈹€
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM, syscall.SIGHUP)

	// 鈹€鈹€ 鏄惁浜や簰寮忕粓绔?鈹€鈹€
	if isatty.IsTerminal(os.Stdout.Fd()) {
		// TUI 妯″紡
		program = tea.NewProgram(uiModel, tea.WithAltScreen())
		go func() {
			<-sigCh
			logInfo("鏀跺埌缁堟淇″彿锛屾鍦ㄥ叧闂?..")
			shutdown()
			program.Quit()
		}()
		go runCore(args)
		if _, err := program.Run(); err != nil {
			fmt.Fprintf(os.Stderr, "TUI 閿欒: %v\n", err)
			os.Exit(1)
		}
	} else {
		// 闈?TTY 妯″紡锛堢閬撹緭鍑猴級
		go func() {
			<-sigCh
			shutdown()
			os.Exit(0)
		}()
		runCore(args)
	}
}

// 鈹€鈹€ 杩愯 Python 鏍稿績 鈹€鈹€

func runCore(args []string) {
	logInfo("鍚姩 Python 鏍稿績...")

	// 瀹氫綅鏍稿績璺緞
	corePath := findCorePath()
	logInfo("Core path: %s", corePath)

	// 鏋勫缓鍛戒护琛屽弬鏁帮紙杩囨护鎺夊凡澶勭悊鐨勬爣蹇楋級
	coreArgs := []string{}
	for _, a := range args {
		if a == "--standalone" || a == "-v" || a == "--version" || a == "-h" || a == "--help" {
			continue
		}
		coreArgs = append(coreArgs, a)
	}

	// 鍒涘缓鐪嬮棬鐙?
	watchdog = lifecycle.NewWatchdog(
		"python",
		corePath,
		coreArgs,
		lifecycle.WithMaxRestarts(3),
		lifecycle.WithRestartDelay(2*time.Second),
		lifecycle.WithShutdownTimeout(5*time.Second),
		lifecycle.WithEventHandler(&watchdogHandler{}),
	)

	// 鍚姩
	if err := watchdog.Start(); err != nil {
		errMsg := fmt.Sprintf("鍚姩 Python 鏍稿績澶辫触: %v", err)
		logError(errMsg)
		if uiModel != nil {
			uiModel.PushError(errMsg)
		} else {
			fmt.Fprintf(os.Stderr, "[Harness] %s\n", errMsg)
		}
		os.Exit(1)
	}

	// 绛夊緟鐪嬮棬鐙楅€€鍑?
	// 鐪嬮棬鐙楄繍琛屽湪鍚庡彴锛宮ain 涓嶇瓑寰呪€斺€擳UI 浜嬩欢寰幆浼氫繚鎸佽繘绋嬪瓨娲?
}

// 鈹€鈹€ 鐪嬮棬鐙椾簨浠跺鐞嗗櫒 鈹€鈹€

type watchdogHandler struct{}

func (h *watchdogHandler) OnStdout(line string) {
	if uiModel != nil {
		handleIPCLine(line)
	}
}

func (h *watchdogHandler) OnStderr(line string) {
	logInfo("[py-stderr] %s", line)
	if uiModel != nil {
		// stderr 閫氬父鏄棩蹇楋紝涓嶆覆鏌撳埌 TUI 涓荤晫闈?
		// 浣嗛敊璇骇鍒渶瑕佹樉绀?
		if strings.Contains(line, "ERROR") || strings.Contains(line, "Traceback") {
			uiModel.PushError(line)
		}
	}
}

func (h *watchdogHandler) OnStateChange(old, new lifecycle.ProcessState) {
	logInfo("Python 鏍稿績鐘舵€? %s 鈫?%s", old, new)
	if uiModel != nil {
		uiModel.SetStatus(fmt.Sprintf("core:%s", new))
	}
}

func (h *watchdogHandler) OnCrash(err error, restartCount int) {
	errMsg := fmt.Sprintf("Python 鏍稿績宕╂簝 (restart %d/3): %v", restartCount, err)
	logError(errMsg)
	if uiModel != nil {
		uiModel.PushError(errMsg)
	}
}

func (h *watchdogHandler) OnHeartbeatTimeout() {
	errMsg := "Python 鏍稿績蹇冭烦瓒呮椂锛屽皢寮哄埗閲嶅惎"
	logError(errMsg)
	if uiModel != nil {
		uiModel.PushError(errMsg)
	}
}

// 鈹€鈹€ IPC 娑堟伅澶勭悊 鈹€鈹€

type IPCMessage struct {
	ID     *int64          `json:"id,omitempty"`
	Method string          `json:"method"`
	Params json.RawMessage `json:"params,omitempty"`
	Result json.RawMessage `json:"result,omitempty"`
	Error  *string         `json:"error,omitempty"`
}

type IPCResponse struct {
	ID     int64           `json:"id"`
	Result json.RawMessage `json:"result,omitempty"`
	Error  *string         `json:"error,omitempty"`
}

func handleIPCLine(line string) {
	line = strings.TrimSpace(line)
	if line == "" {
		return
	}

	var msg IPCMessage
	if err := json.Unmarshal([]byte(line), &msg); err != nil {
		return
	}

	switch msg.Method {
	case "event":
		handleEvent(msg.Params)
	case "ping":
		handlePing(msg.ID)
	case "stream":
		handleStream(msg.Params)
	default:
		// 鍙兘鏄搷搴旓紙甯?id 浣嗘病鏈?method锛?
		if msg.ID != nil && msg.Result != nil {
			// 鍝嶅簲鈥斺€斿拷鐣ワ紝鐢?Watchdog 閫忎紶
		}
	}
}

func handleEvent(raw json.RawMessage) {
	var evt struct {
		Type string          `json:"type"`
		Data json.RawMessage `json:"data"`
	}
	if err := json.Unmarshal(raw, &evt); err != nil {
		return
	}

	switch evt.Type {
	case "text":
		var text string
		json.Unmarshal(evt.Data, &text)
		uiModel.PushText(text)

	case "tool_start":
		var tool struct {
			Name string `json:"name"`
			Args string `json:"args"`
		}
		json.Unmarshal(evt.Data, &tool)
		uiModel.PushToolStart(tool.Name, tool.Args)

	case "tool_result":
		var result struct {
			Success bool   `json:"success"`
			Data    string `json:"data"`
		}
		json.Unmarshal(evt.Data, &result)
		uiModel.PushToolResult(result.Data, result.Success)

	case "error":
		var errMsg string
		json.Unmarshal(evt.Data, &errMsg)
		uiModel.PushError(errMsg)

	case "thinking":
		var thought string
		json.Unmarshal(evt.Data, &thought)
		uiModel.PushThinking(thought)

	case "complete":
		uiModel.PushComplete()

	case "status":
		var status string
		json.Unmarshal(evt.Data, &status)
		uiModel.SetStatus(status)
	}
}

func handleStream(raw json.RawMessage) {
	var chunk string
	if err := json.Unmarshal(raw, &chunk); err != nil {
		return
	}
	// 娴佸紡瀛楃鎺ㄩ€侊紙鐢ㄤ簬鎵撳瓧鏈烘晥鏋滐級
	if uiModel != nil {
		// 鎵归噺鎺ㄩ€侊紝姣忓潡浣滀负涓€涓簨浠?
		uiModel.PushStream(chunk)
	}
}

func handlePing(id *int64) {
	if id == nil || watchdog == nil {
		return
	}
	resp, _ := json.Marshal(IPCResponse{
		ID:     *id,
		Result: json.RawMessage(`"pong"`),
	})
	watchdog.Send(append(resp, '\n'))
}

// 鈹€鈹€ 鍏抽棴 鈹€鈹€

func shutdown() {
	logInfo("寮€濮嬪叧闂?..")
	if watchdog != nil {
		watchdog.Stop()
	}
	logInfo("鍏抽棴瀹屾垚")
}

// 鈹€鈹€ Standalone 妯″紡 鈹€鈹€

func runStandalone(args []string) {
	fmt.Fprintf(os.Stderr, "[Harness] 绾?Python 妯″紡\n")
	corePath := findCorePath()
	cmdArgs := append([]string{corePath}, args...)

	cmd := execCommand("python", cmdArgs...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.Run()
}

// 鈹€鈹€ 杈呭姪鍑芥暟 鈹€鈹€

func findCorePath() string {
	// 鐜鍙橀噺浼樺厛
	if v := os.Getenv("SlayHot_CORE"); v != "" {
		if _, err := os.Stat(v); err == nil {
			return v
		}
	}

	// 鐩稿 Harness 浜岃繘鍒剁殑浣嶇疆
	exePath, err := os.Executable()
	if err == nil {
		exeDir := filepath.Dir(exePath)
		candidates := []string{
			filepath.Join(exeDir, "..", "..", "..", "main.py"),
			filepath.Join(exeDir, "..", "..", "main.py"),
			filepath.Join(exeDir, "..", "main.py"),
		}
		for _, p := range candidates {
			abs, _ := filepath.Abs(p)
			if _, err := os.Stat(abs); err == nil {
				return abs
			}
		}
	}

	// fallback
	return "main.py"
}

func getDefaultModel() string {
	if v := os.Getenv("SlayHot_MODEL"); v != "" {
		return v
	}
	return "claude-sonnet-4-20250514"
}

func homeDir() string {
	if v := os.Getenv("HOME"); v != "" {
		return v
	}
	if v := os.Getenv("USERPROFILE"); v != "" {
		return v
	}
	return "."
}

func printHelp() {
	fmt.Printf(`%s Harness v%s 鈥?鍘熺敓 AI 鏅鸿兘浣撳３灞?

鐢ㄦ硶:
  %s [閫夐」] [娑堟伅...]

閫夐」:
  -h, --help       鏄剧ず甯姪
  -v, --version    鏄剧ず鐗堟湰
  --standalone     绾?Python 妯″紡锛堜笉浣跨敤鍘熺敓澹冲眰锛?
  -m, --model      鎸囧畾妯″瀷锛堝 claude-sonnet-4-20250514锛?
  -p, --provider   鎸囧畾鎻愪緵鍟嗭紙anthropic | openai | deepseek锛?
  -w, --workflow   鎸囧畾宸ヤ綔娴佹ā寮?
  --interactive    浜や簰妯″紡

绀轰緥:
  %s "甯垜鍐欎竴涓?Python 鍑芥暟"
  %s --interactive
  %s -w coding "鍐欎竴涓?Web 鏈嶅姟鍣?

鐜鍙橀噺:
  SlayHot_CORE      Python 鏍稿績璺緞
  SlayHot_MODEL     榛樿妯″瀷
  SlayHot_LOG_LEVEL 鏃ュ織绾у埆
`,
		Codename, Version,
		os.Args[0],
		os.Args[0], os.Args[0], os.Args[0],
	)
}

func checkUpdate() {
	updChecker = updater.NewChecker()
	result := updChecker.Check()
	if result.Status == updater.StatusAvailable {
		msg := fmt.Sprintf("鍙戠幇鏂扮増鏈? %s 鈫?%s (杩愯 --version 鏌ョ湅璇︽儏)", result.Current, result.Latest)
		if uiModel != nil {
			uiModel.PushText(fmt.Sprintf("\n  馃摝 %s\n", msg))
		}
		logInfo("鏇存柊鍙敤: %s 鈫?%s", result.Current, result.Latest)
	} else if result.Status == updater.StatusCheckFailed {
		logInfo("鏇存柊妫€鏌ュけ璐? %v", result.Error)
	}
}

// 鈹€鈹€ exec 鍖呰 鈹€鈹€

func execCommand(name string, arg ...string) *exec.Cmd {
	return exec.Command(name, arg...)
}

// 鈹€鈹€ 鏃ュ織杈呭姪 鈹€鈹€

func logInfo(format string, args ...interface{}) {
	if logger != nil {
		logger.Info(fmt.Sprintf(format, args...))
	}
}

func logError(format string, args ...interface{}) {
	if logger != nil {
		logger.Error(fmt.Sprintf(format, args...))
	}
}
