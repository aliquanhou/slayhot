#!/usr/bin/env node

/**
 * SlayHot CLI 鍏ュ彛 鈥?妫€娴嬪師鐢?Harness 浜岃繘鍒跺苟鍚姩銆?
 *
 * 娴佺▼锛?
 *   1. 妫€娴嬪钩鍙板搴旂殑鍘熺敓 Harness 浜岃繘鍒?
 *   2. 濡傛灉瀛樺湪 鈫?鍚姩鍘熺敓浜岃繘鍒讹紙瀛愯繘绋嬶級
 *   3. 濡傛灉涓嶅瓨鍦?鈫?鍥為€€鍒?python main.py
 */

const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

// 鈹€鈹€ 骞冲彴妫€娴?鈹€鈹€

function getPlatform() {
  const type = os.type();
  const arch = os.arch();

  if (type === 'Windows_NT' && arch === 'x64') return 'win32-x64';
  if (type === 'Darwin' && arch === 'arm64') return 'darwin-arm64';
  if (type === 'Darwin' && arch === 'x64') return 'darwin-arm64'; // Rosetta
  if (type === 'Linux' && arch === 'x64') return 'linux-x64';
  if (type === 'Linux' && arch === 'arm64') return 'linux-x64';   // 鍥為€€

  return null;
}

// 鈹€鈹€ 鏌ユ壘 Harness 浜岃繘鍒?鈹€鈹€

function findHarnessBinary() {
  const platform = getPlatform();
  if (!platform) return null;

  const binaryName = platform.startsWith('win') ? 'SlayHot.exe' : 'SlayHot';

  // 1. 妫€鏌?@SlayHot/harness-{platform} 鍖?
  try {
    const pkgPath = path.join(__dirname, '..', '..', `@SlayHot/harness-${platform}`);
    const binaryPath = path.join(pkgPath, 'bin', binaryName);
    if (fs.existsSync(binaryPath)) return binaryPath;
  } catch (e) { /* ignore */ }

  // 2. 妫€鏌?node_modules
  try {
    const pkgPath = path.join(__dirname, '..', '..', '..', `@SlayHot/harness-${platform}`);
    const binaryPath = path.join(pkgPath, 'bin', binaryName);
    if (fs.existsSync(binaryPath)) return binaryPath;
  } catch (e) { /* ignore */ }

  // 3. 妫€鏌ラ」鐩牴鐩綍
  const projectRoot = path.join(__dirname, '..', '..', '..');
  const binaryPath = path.join(projectRoot, 'bin', binaryName);
  if (fs.existsSync(binaryPath)) return binaryPath;

  return null;
}

// 鈹€鈹€ 鏌ユ壘 Python 鏍稿績 鈹€鈹€

function findPythonCore() {
  const searchPaths = [
    path.join(__dirname, '..', '..', '..', 'main.py'),
    path.join(__dirname, '..', '..', 'main.py'),
    path.join(process.cwd(), 'main.py'),
  ];

  for (const p of searchPaths) {
    if (fs.existsSync(p)) return p;
  }

  return null;
}

// 鈹€鈹€ 涓婚€昏緫 鈹€鈹€

async function main() {
  const args = process.argv.slice(2);
  const harnessBinary = findHarnessBinary();
  const pythonCore = findPythonCore();

  if (harnessBinary) {
    // 鍚姩鍘熺敓 Harness
    console.error(`[SlayHot] 鍚姩鍘熺敓 Harness: ${harnessBinary}`);
    const child = spawn(harnessBinary, args, {
      stdio: 'inherit',
      env: { ...process.env },
    });

    child.on('exit', (code) => {
      process.exit(code || 0);
    });
  } else if (pythonCore) {
    // 鍥為€€鍒?Python 妯″紡
    console.error('[SlayHot] 鏈娴嬪埌鍘熺敓 Harness锛屽洖閫€鍒?Python 妯″紡');

    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
    const child = spawn(pythonCmd, [pythonCore, ...args], {
      stdio: 'inherit',
      env: { ...process.env },
    });

    child.on('exit', (code) => {
      process.exit(code || 0);
    });
  } else {
    console.error('[SlayHot] 閿欒: 鎵句笉鍒?SlayHot 鏍稿績鏂囦欢');
    console.error('璇风‘淇濆湪 SlayHot 椤圭洰鐩綍涓繍琛?);
    console.error('');
    console.error('瀹夎鏂瑰紡:');
    console.error('  npm install -g @SlayHot/cli        # 鍏ㄥ眬瀹夎锛堝惈鍘熺敓 Harness锛?);
    console.error('  pip install SlayHot                 # Python 妯″紡瀹夎');
    process.exit(1);
  }
}

main().catch(console.error);
