/**
 * @SlayHot/cli 瀹夎鑴氭湰
 *
 * 鑱岃矗锛?
 *   1. 妫€娴嬪钩鍙?
 *   2. 涓嬭浇瀵瑰簲鐨勫師鐢?Harness 浜岃繘鍒讹紙濡傛灉涓嶅瓨鍦級
 *   3. 楠岃瘉瀹屾暣鎬?
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const https = require('https');
const os = require('os');

const PKG_VERSION = '1.0.0';
const CDN_BASE = 'https://github.com/SlayHot/harness/releases/download';

function getPlatform() {
  const type = os.type();
  const arch = os.arch();

  if (type === 'Windows_NT' && arch === 'x64') return 'win32-x64';
  if (type === 'Darwin' && arch === 'arm64') return 'darwin-arm64';
  if (type === 'Darwin' && arch === 'x64') return 'darwin-arm64';
  if (type === 'Linux' && arch === 'x64') return 'linux-x64';
  if (type === 'Linux' && arch === 'arm64') return 'linux-arm64';

  return null;
}

function getBinaryName(platform) {
  return platform.startsWith('win') ? 'SlayHot.exe' : 'SlayHot';
}

async function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    https.get(url, (response) => {
      if (response.statusCode !== 200) {
        reject(new Error(`涓嬭浇澶辫触: ${response.statusCode}`));
        return;
      }
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
    }).on('error', (err) => {
      fs.unlinkSync(dest);
      reject(err);
    });
  });
}

async function install() {
  const platform = getPlatform();
  if (!platform) {
    console.error(`[瀹夎] 涓嶆敮鎸佺殑骞冲彴: ${os.type()} ${os.arch()}`);
    console.error('[瀹夎] 灏嗕娇鐢?Python 妯″紡杩愯');
    return;
  }

  const binaryName = getBinaryName(platform);
  const targetDir = path.join(__dirname, '..', `@SlayHot/harness-${platform}`, 'bin');
  const targetPath = path.join(targetDir, binaryName);

  // 濡傛灉宸插瓨鍦紝璺宠繃锛堝悗缁彲鍔犵増鏈牎楠岋級
  if (fs.existsSync(targetPath)) {
    console.error(`[瀹夎] Harness 浜岃繘鍒跺凡瀛樺湪: ${targetPath}`);
    return;
  }

  // 灏濊瘯浠?CDN 涓嬭浇
  const url = `${CDN_BASE}/v${PKG_VERSION}/${binaryName}`;
  console.error(`[瀹夎] 涓嬭浇 Harness 浜岃繘鍒? ${url}`);

  try {
    fs.mkdirSync(targetDir, { recursive: true });
    await downloadFile(url, targetPath);
    fs.chmodSync(targetPath, 0o755);
    console.error(`[瀹夎] 涓嬭浇瀹屾垚: ${targetPath}`);
  } catch (err) {
    console.error(`[瀹夎] 涓嬭浇澶辫触: ${err.message}`);
    console.error('[瀹夎] 灏嗕娇鐢?Python 妯″紡杩愯');
    if (fs.existsSync(targetPath)) fs.unlinkSync(targetPath);
  }
}

install().catch(console.error);
