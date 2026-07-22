import { copyFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const rootDir = dirname(dirname(fileURLToPath(import.meta.url)));
const srcDir = join(rootDir, 'node_modules/@ffmpeg/core/dist/esm');
const destDir = join(rootDir, 'public/ffmpeg-core');

if (!existsSync(srcDir)) {
  console.warn('[copy-ffmpeg-core] @ffmpeg/core not found, skipping (run npm install first).');
  process.exit(0);
}

mkdirSync(destDir, { recursive: true });
for (const file of ['ffmpeg-core.js', 'ffmpeg-core.wasm']) {
  copyFileSync(join(srcDir, file), join(destDir, file));
}
console.log('[copy-ffmpeg-core] Copied ffmpeg-core files to public/ffmpeg-core/');
