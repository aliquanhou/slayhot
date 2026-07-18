// updater/check.go 鈥?鑷姩鏇存柊妫€鏌?
//
// 鏂囨。瀵归綈锛氬師鐢?Harness 鑷姩鏇存柊鏈哄埗
// 鍔熻兘锛欸itHub Release 妫€鏌ャ€佺増鏈姣斻€佸閲忎笅杞?

package updater

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"runtime"
	"time"
)

// 鈹€鈹€ 鐗堟湰淇℃伅 鈹€鈹€

const (
	Owner = "SlayHot"
	Repo  = "SlayHot"
)

var (
	CurrentVersion = "1.0.0"
	CheckURL       = fmt.Sprintf("https://api.github.com/repos/%s/%s/releases/latest", Owner, Repo)
)

// 鈹€鈹€ Release 淇℃伅 鈹€鈹€

type ReleaseInfo struct {
	Version     string `json:"tag_name"`
	PublishedAt string `json:"published_at"`
	Body        string `json:"body"`
	Assets      []AssetInfo `json:"assets"`
}

type AssetInfo struct {
	Name        string `json:"name"`
	URL         string `json:"browser_download_url"`
	Size        int64  `json:"size"`
	ContentType string `json:"content_type"`
}

type UpdateStatus int

const (
	StatusCurrent UpdateStatus = iota
	StatusAvailable
	StatusCheckFailed
)

type UpdateResult struct {
	Status    UpdateStatus
	Current   string
	Latest    string
	Release   *ReleaseInfo
	Error     error
}

// 鈹€鈹€ 鏇存柊妫€鏌ュ櫒 鈹€鈹€

type Checker struct {
	CurrentVersion string
	CheckURL       string
	HTTPClient     *http.Client
	Platform       string
	Arch           string
}

func NewChecker() *Checker {
	return &Checker{
		CurrentVersion: CurrentVersion,
		CheckURL:       CheckURL,
		HTTPClient: &http.Client{
			Timeout: 10 * time.Second,
			Transport: &http.Transport{
				IdleConnTimeout: 5 * time.Second,
			},
		},
		Platform: runtime.GOOS,
		Arch:     runtime.GOARCH,
	}
}

func (c *Checker) Check() *UpdateResult {
	result := &UpdateResult{
		Current: c.CurrentVersion,
	}

	req, err := http.NewRequest("GET", c.CheckURL, nil)
	if err != nil {
		result.Status = StatusCheckFailed
		result.Error = fmt.Errorf("鍒涘缓璇锋眰澶辫触: %w", err)
		return result
	}
	req.Header.Set("Accept", "application/vnd.github.v3+json")
	req.Header.Set("User-Agent", "SlayHot-Harness/"+c.CurrentVersion)

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		result.Status = StatusCheckFailed
		result.Error = fmt.Errorf("妫€鏌ユ洿鏂板け璐? %w", err)
		return result
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		result.Status = StatusCheckFailed
		result.Error = fmt.Errorf("璇诲彇鍝嶅簲澶辫触: %w", err)
		return result
	}

	var release ReleaseInfo
	if err := json.Unmarshal(body, &release); err != nil {
		result.Status = StatusCheckFailed
		result.Error = fmt.Errorf("瑙ｆ瀽鍝嶅簲澶辫触: %w", err)
		return result
	}

	// 鍘婚櫎鐗堟湰鍙峰墠鐨?'v'
	latest := release.Version
	if len(latest) > 0 && latest[0] == 'v' {
		latest = latest[1:]
	}
	result.Latest = latest
	result.Release = &release

	if latest > c.CurrentVersion {
		result.Status = StatusAvailable
	} else {
		result.Status = StatusCurrent
	}

	return result
}

// 鈹€鈹€ 骞冲彴璧勪骇鏌ユ壘 鈹€鈹€

func (c *Checker) FindPlatformAsset(release *ReleaseInfo) *AssetInfo {
	pattern := fmt.Sprintf("SlayHot-harness-%s-%s", c.Platform, c.Arch)
	for _, asset := range release.Assets {
		if matchesPlatform(asset.Name, c.Platform, c.Arch) {
			return &asset
		}
		_ = pattern
	}
	return nil
}

func matchesPlatform(name, platform, arch string) bool {
	patterns := []string{
		fmt.Sprintf("%s-%s", platform, arch),
		fmt.Sprintf("%s_%s", platform, arch),
	}
	if platform == "windows" {
		patterns = append(patterns,
			fmt.Sprintf("win32-%s", arch),
			fmt.Sprintf("win-%s", arch),
		)
	}
	for _, p := range patterns {
		if contains(name, p) {
			return true
		}
	}
	return false
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr ||
		(len(s) > len(substr) && (s[:len(substr)] == substr || s[len(s)-len(substr):] == substr)))
}

// 鈹€鈹€ 涓嬭浇鏇存柊 鈹€鈹€

func (c *Checker) Download(asset *AssetInfo, destDir string) (string, error) {
	resp, err := c.HTTPClient.Get(asset.URL)
	if err != nil {
		return "", fmt.Errorf("涓嬭浇澶辫触: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("涓嬭浇澶辫触: HTTP %d", resp.StatusCode)
	}

	destPath := filepath.Join(destDir, asset.Name)
	f, err := os.Create(destPath)
	if err != nil {
		return "", fmt.Errorf("鍒涘缓鏂囦欢澶辫触: %w", err)
	}
	defer f.Close()

	written, err := io.Copy(f, resp.Body)
	if err != nil {
		return "", fmt.Errorf("鍐欏叆鏂囦欢澶辫触: %w", err)
	}

	// 楠岃瘉澶у皬
	if asset.Size > 0 && written != asset.Size {
		return "", fmt.Errorf("鏂囦欢澶у皬涓嶅尮閰? 鏈熸湜 %d, 瀹為檯 %d", asset.Size, written)
	}

	// 璁剧疆鍙墽琛屾潈闄?(Unix)
	if runtime.GOOS != "windows" {
		os.Chmod(destPath, 0755)
	}

	return destPath, nil
}

// 鈹€鈹€ 鏍煎紡鍖栧伐鍏锋湁鏃犳洿鏂?鈹€鈹€

func (r *UpdateResult) String() string {
	switch r.Status {
	case StatusCurrent:
		return fmt.Sprintf("宸叉槸鏈€鏂扮増鏈? %s", r.Current)
	case StatusAvailable:
		return fmt.Sprintf("鍙戠幇鏂扮増鏈? %s 鈫?%s", r.Current, r.Latest)
	case StatusCheckFailed:
		return fmt.Sprintf("妫€鏌ユ洿鏂板け璐? %v", r.Error)
	default:
		return "鏈煡鐘舵€?
	}
}
