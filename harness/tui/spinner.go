// tui/spinner.go 鈥?鍔犺浇鍔ㄧ敾鏍峰紡
package tui

import "github.com/charmbracelet/bubbles/spinner"

// NewSpinner 鍒涘缓 SlayHot 椋庢牸鐨勫姞杞藉姩鐢?
func NewSpinner() spinner.Model {
	s := spinner.New()
	s.Style = StyleSpinner
	s.Spinner = spinner.Dot
	return s
}

// SpinnerFrames 鑷畾涔夊抚锛堝彲閫夛級
var SpinnerFrames = []string{"猓?, "猓?, "猓?, "猗?, "狻?, "猓?, "猓?, "猓?}
