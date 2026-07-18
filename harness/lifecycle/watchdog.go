// lifecycle/watchdog.go 鈥?杩涚▼鐪嬮棬鐙?
//
// 鏂囨。瀵归綈锛氬師鐢?Harness 杩涚▼鐢熷懡鍛ㄦ湡绠＄悊
// 鍔熻兘锛氬惎鍔?Python 鏍稿績銆佸穿婧冩娴嬨€佽嚜鍔ㄩ噸鍚紙闄愭锛夈€佷紭闆呭叧闂?

package lifecycle

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"os/exec"
	"sync"
	"time"
)

// 鈹€鈹€ 甯搁噺 鈹€鈹€

const (
	DefaultMaxRestarts     = 3
	DefaultRestartDelay    = 2 * time.Second
	DefaultShutdownTimeout = 5 * time.Second
	HeartbeatInterval      = 5 * time.Second
)

// 鈹€鈹€ 杩涚▼鐘舵€?鈹€鈹€

type ProcessState int

const (
	StateStopped ProcessState = iota
	StateStarting
	StateRunning
	StateRestarting
	StateStopping
	StateFailed
)

func (s ProcessState) String() string {
	switch s {
	case StateStopped:
		return "stopped"
	case StateStarting:
		return "starting"
	case StateRunning:
		return "running"
	case StateRestarting:
		return "restarting"
	case StateStopping:
		return "stopping"
	case StateFailed:
		return "failed"
	default:
		return "unknown"
	}
}

// 鈹€鈹€ 浜嬩欢鍥炶皟 鈹€鈹€

type EventHandler interface {
	OnStdout(line string)
	OnStderr(line string)
	OnStateChange(old, new ProcessState)
	OnCrash(err error, restartCount int)
	OnHeartbeatTimeout()
}

// 鈹€鈹€ 鐪嬮棬鐙?鈹€鈹€

type Watchdog struct {
	mu sync.RWMutex

	pythonPath string
	corePath   string
	args       []string

	cmd          *exec.Cmd
	stdin        io.WriteCloser
	stdoutReader *bufio.Scanner
	stderrReader *bufio.Scanner
	state        ProcessState
	restartCount int
	maxRestarts  int
	restartDelay time.Duration
	shutdownTO   time.Duration

	handler     EventHandler
	quit        chan struct{}
	done        chan struct{}
	pid         int
	lastHeartbe time.Time
}

type WatchdogOption func(*Watchdog)

func WithMaxRestarts(n int) WatchdogOption {
	return func(w *Watchdog) { w.maxRestarts = n }
}

func WithRestartDelay(d time.Duration) WatchdogOption {
	return func(w *Watchdog) { w.restartDelay = d }
}

func WithShutdownTimeout(d time.Duration) WatchdogOption {
	return func(w *Watchdog) { w.shutdownTO = d }
}

func WithEventHandler(h EventHandler) WatchdogOption {
	return func(w *Watchdog) { w.handler = h }
}

func NewWatchdog(pythonPath, corePath string, args []string, opts ...WatchdogOption) *Watchdog {
	w := &Watchdog{
		pythonPath:   pythonPath,
		corePath:     corePath,
		args:         args,
		maxRestarts:  DefaultMaxRestarts,
		restartDelay: DefaultRestartDelay,
		shutdownTO:   DefaultShutdownTimeout,
		state:        StateStopped,
		quit:         make(chan struct{}),
		done:         make(chan struct{}),
	}
	for _, opt := range opts {
		opt(w)
	}
	return w
}

// 鈹€鈹€ 鍚姩 鈹€鈹€

func (w *Watchdog) Start() error {
	w.mu.Lock()
	if w.state != StateStopped {
		w.mu.Unlock()
		return fmt.Errorf("鐪嬮棬鐙楀凡鍦ㄨ繍琛? %s", w.state)
	}
	w.state = StateStarting
	w.restartCount = 0
	w.mu.Unlock()

	go w.runLoop()
	return nil
}

func (w *Watchdog) runLoop() {
	defer close(w.done)

	for {
		select {
		case <-w.quit:
			w.shutdown()
			return
		default:
		}

		err := w.startProcess()
		if err != nil {
			w.setState(StateFailed)
			if w.handler != nil {
				w.handler.OnCrash(err, w.restartCount)
			}
			return
		}

		w.setState(StateRunning)
		err = w.waitProcess()

		select {
		case <-w.quit:
			w.shutdown()
			return
		default:
		}

		if err != nil {
			w.restartCount++
			if w.handler != nil {
				w.handler.OnCrash(err, w.restartCount)
			}

			if w.restartCount >= w.maxRestarts {
				fmt.Fprintf(os.Stderr, "[鐪嬮棬鐙梋 杈惧埌鏈€澶ч噸鍚鏁?%d锛屽仠姝n", w.maxRestarts)
				w.setState(StateFailed)
				return
			}

			w.setState(StateRestarting)
			fmt.Fprintf(os.Stderr, "[鐪嬮棬鐙梋 杩涚▼宕╂簝 (restart %d/%d)锛?v 鍚庨噸鍚?..\n",
				w.restartCount, w.maxRestarts, w.restartDelay)

			select {
			case <-time.After(w.restartDelay):
			case <-w.quit:
				return
			}
		}
	}
}

func (w *Watchdog) startProcess() error {
	cmdArgs := []string{w.corePath, "--harness-mode"}
	cmdArgs = append(cmdArgs, w.args...)

	cmd := exec.Command(w.pythonPath, cmdArgs...)

	stdin, err := cmd.StdinPipe()
	if err != nil {
		return fmt.Errorf("鍒涘缓 stdin 绠￠亾澶辫触: %w", err)
	}

	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return fmt.Errorf("鍒涘缓 stdout 绠￠亾澶辫触: %w", err)
	}

	stderr, err := cmd.StderrPipe()
	if err != nil {
		return fmt.Errorf("鍒涘缓 stderr 绠￠亾澶辫触: %w", err)
	}

	cmd.Env = append(os.Environ(),
		"SlayHot_MODE=harness",
		fmt.Sprintf("SlayHot_HARNESS_PID=%d", os.Getpid()),
	)

	if err := cmd.Start(); err != nil {
		return fmt.Errorf("鍚姩 Python 鏍稿績澶辫触: %w", err)
	}

	w.mu.Lock()
	w.cmd = cmd
	w.stdin = stdin
	w.stdoutReader = bufio.NewScanner(stdout)
	w.stderrReader = bufio.NewScanner(stderr)
	w.pid = cmd.Process.Pid
	w.lastHeartbeat = time.Now()
	w.mu.Unlock()

	return nil
}

func (w *Watchdog) waitProcess() error {
	// stdout 璇诲彇
	stdoutDone := make(chan error, 1)
	go func() {
		for w.stdoutReader.Scan() {
			line := w.stdoutReader.Text()
			if w.handler != nil {
				w.handler.OnStdout(line)
			}

			// 蹇冭烦鏇存柊锛氭敹鍒颁换浣?stdout 琛岄兘绠?
			w.mu.Lock()
			w.lastHeartbeat = time.Now()
			w.mu.Unlock()
		}
		stdoutDone <- w.stdoutReader.Err()
	}()

	// stderr 璇诲彇
	stderrDone := make(chan error, 1)
	go func() {
		for w.stderrReader.Scan() {
			line := w.stderrReader.Text()
			if w.handler != nil {
				w.handler.OnStderr(line)
			}
		}
		stderrDone <- w.stderrReader.Err()
	}()

	// 蹇冭烦鐩戞帶
	heartbeatDone := make(chan struct{}, 1)
	go func() {
		ticker := time.NewTicker(HeartbeatInterval)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				w.mu.RLock()
				elapsed := time.Since(w.lastHeartbeat)
				w.mu.RUnlock()
				if elapsed > w.shutdownTO*2 {
					if w.handler != nil {
						w.handler.OnHeartbeatTimeout()
					}
					w.cmd.Process.Kill()
					return
				}
			case <-heartbeatDone:
				return
			}
		}
	}()

	// 绛夊緟杩涚▼閫€鍑?
	err := w.cmd.Wait()
	close(heartbeatDone)
	<-stdoutDone
	<-stderrDone

	return err
}

// 鈹€鈹€ 鍋滄 鈹€鈹€

func (w *Watchdog) Stop() {
	close(w.quit)
	<-w.done
}

func (w *Watchdog) shutdown() {
	w.setState(StateStopping)

	w.mu.RLock()
	cmd := w.cmd
	stdin := w.stdin
	w.mu.RUnlock()

	if cmd != nil && cmd.Process != nil {
		// 鍏堝彂 SIGTERM
		cmd.Process.Signal(os.Interrupt)

		// 绛夊緟鎴栧己鍒舵潃姝?
		done := make(chan struct{}, 1)
		go func() {
			cmd.Wait()
			done <- struct{}{}
		}()

		select {
		case <-done:
		case <-time.After(w.shutdownTO):
			cmd.Process.Kill()
		}
	}

	if stdin != nil {
		stdin.Close()
	}

	w.setState(StateStopped)
}

// 鈹€鈹€ 鐘舵€?鈹€鈹€

func (w *Watchdog) State() ProcessState {
	w.mu.RLock()
	defer w.mu.RUnlock()
	return w.state
}

func (w *Watchdog) PID() int {
	w.mu.RLock()
	defer w.mu.RUnlock()
	return w.pid
}

func (w *Watchdog) RestartCount() int {
	w.mu.RLock()
	defer w.mu.RUnlock()
	return w.restartCount
}

func (w *Watchdog) Send(data []byte) (int, error) {
	w.mu.RLock()
	stdin := w.stdin
	w.mu.RUnlock()
	if stdin == nil {
		return 0, fmt.Errorf("stdin 鏈氨缁?)
	}
	return stdin.Write(data)
}

func (w *Watchdog) Stdin() io.WriteCloser {
	w.mu.RLock()
	defer w.mu.RUnlock()
	return w.stdin
}

func (w *Watchdog) setState(s ProcessState) {
	w.mu.Lock()
	old := w.state
	w.state = s
	w.mu.Unlock()
	if w.handler != nil {
		w.handler.OnStateChange(old, s)
	}
}

// 鈹€鈹€ JSON-RPC 杈呭姪 鈹€鈹€

type RPCRequest struct {
	ID     int64           `json:"id"`
	Method string          `json:"method"`
	Params json.RawMessage `json:"params,omitempty"`
}

type RPCResponse struct {
	ID     int64           `json:"id,omitempty"`
	Result json.RawMessage `json:"result,omitempty"`
	Error  *string         `json:"error,omitempty"`
}

func (w *Watchdog) SendRPC(method string, params interface{}) error {
	data, err := json.Marshal(params)
	if err != nil {
		return err
	}
	req := RPCRequest{
		ID:     time.Now().UnixNano(),
		Method: method,
		Params: data,
	}
	raw, err := json.Marshal(req)
	if err != nil {
		return err
	}
	_, err = w.Send(append(raw, '\n'))
	return err
}
