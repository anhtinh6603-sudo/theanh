import './style.css';
import { FFmpeg } from '@ffmpeg/ffmpeg';
import { fetchFile, toBlobURL } from '@ffmpeg/util';

const CORE_BASE = '/ffmpeg-core';

let ffmpegInstance = null;
let ffmpegLoadPromise = null;
let recentLogs = [];

const logEl = document.getElementById('log');
const progressBar = document.getElementById('progress-bar');
const outputArea = document.getElementById('output-area');
const outputVideo = document.getElementById('output-preview');
const outputImage = document.getElementById('output-image');
const outputDownload = document.getElementById('output-download');

function clearLog() {
  logEl.textContent = '';
}

function appendLog(line) {
  logEl.textContent += `${line}\n`;
  logEl.scrollTop = logEl.scrollHeight;
}

function setProgress(ratio) {
  const pct = Math.min(100, Math.max(0, ratio * 100));
  progressBar.style.width = `${pct}%`;
}

async function getFFmpeg() {
  if (ffmpegInstance) return ffmpegInstance;
  if (!ffmpegLoadPromise) {
    ffmpegLoadPromise = (async () => {
      const instance = new FFmpeg();
      instance.on('log', ({ message }) => {
        recentLogs.push(message);
        appendLog(message);
      });
      instance.on('progress', ({ progress }) => setProgress(progress));
      appendLog('Đang tải ffmpeg core (chỉ tải một lần)...');
      await instance.load({
        coreURL: await toBlobURL(`${CORE_BASE}/ffmpeg-core.js`, 'text/javascript'),
        wasmURL: await toBlobURL(`${CORE_BASE}/ffmpeg-core.wasm`, 'application/wasm'),
      });
      appendLog('Đã tải xong ffmpeg core.');
      ffmpegInstance = instance;
      return instance;
    })();
  }
  return ffmpegLoadPromise;
}

async function hasAudioStream(ff, filename) {
  recentLogs = [];
  try {
    await ff.exec(['-i', filename]);
  } catch {
    // ffmpeg exits non-zero when called with no output file; that's expected here,
    // we only care about the stream info it printed to the log while probing.
  }
  return recentLogs.some((line) => line.includes('Audio:'));
}

function extOf(filename, fallback = 'mp4') {
  const match = /\.([a-zA-Z0-9]+)$/.exec(filename || '');
  return match ? match[1].toLowerCase() : fallback;
}

function setRunning(button, running, idleLabel) {
  button.disabled = running;
  button.textContent = running ? 'Đang xử lý...' : idleLabel;
}

function showOutput(blob, filename, kind = 'video') {
  const url = URL.createObjectURL(blob);
  if (kind === 'image') {
    outputImage.src = url;
    outputImage.style.display = 'block';
    outputVideo.style.display = 'none';
    outputVideo.removeAttribute('src');
  } else {
    outputVideo.src = url;
    outputVideo.style.display = 'block';
    outputImage.style.display = 'none';
    outputImage.removeAttribute('src');
  }
  outputDownload.href = url;
  outputDownload.download = filename;
  outputArea.hidden = false;
  outputArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function runFFmpeg(button, idleLabel, task) {
  setRunning(button, true, idleLabel);
  clearLog();
  setProgress(0);
  try {
    await task();
  } catch (err) {
    appendLog(`Lỗi: ${err?.message || err}`);
    alert('Có lỗi xảy ra trong quá trình xử lý. Xem log bên dưới để biết chi tiết.');
  } finally {
    setRunning(button, false, idleLabel);
    setProgress(0);
  }
}

// ---------- Tabs ----------
document.querySelectorAll('.tab-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach((b) => b.classList.remove('active'));
    document.querySelectorAll('.panel').forEach((p) => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(`panel-${btn.dataset.tab}`).classList.add('active');
  });
});

// ---------- Trim ----------
const trimInput = document.getElementById('trim-input');
const trimPreview = document.getElementById('trim-preview');
const trimRun = document.getElementById('trim-run');
let trimFile = null;

trimInput.addEventListener('change', () => {
  trimFile = trimInput.files[0] || null;
  if (trimFile) trimPreview.src = URL.createObjectURL(trimFile);
});

trimRun.addEventListener('click', () => {
  if (!trimFile) return alert('Hãy chọn video trước.');
  const start = parseFloat(document.getElementById('trim-start').value) || 0;
  const end = parseFloat(document.getElementById('trim-end').value) || 0;
  if (end <= start) return alert('Thời gian kết thúc phải lớn hơn thời gian bắt đầu.');

  runFFmpeg(trimRun, 'Cắt video', async () => {
    const ff = await getFFmpeg();
    const inputName = `input.${extOf(trimFile.name)}`;
    const outputName = 'output.mp4';
    await ff.writeFile(inputName, await fetchFile(trimFile));
    await ff.exec([
      '-i', inputName,
      '-ss', String(start),
      '-to', String(end),
      '-c:v', 'libx264',
      '-c:a', 'aac',
      '-preset', 'ultrafast',
      outputName,
    ]);
    const data = await ff.readFile(outputName);
    showOutput(new Blob([data.buffer], { type: 'video/mp4' }), 'trimmed.mp4');
    await ff.deleteFile(inputName);
    await ff.deleteFile(outputName);
  });
});

// ---------- Merge ----------
const mergeInput = document.getElementById('merge-input');
const mergeListEl = document.getElementById('merge-list');
const mergeRun = document.getElementById('merge-run');
let mergeFiles = [];

mergeInput.addEventListener('change', () => {
  mergeFiles = Array.from(mergeInput.files || []);
  mergeListEl.innerHTML = mergeFiles.map((f, i) => `<li>${i + 1}. ${f.name}</li>`).join('');
});

mergeRun.addEventListener('click', () => {
  if (mergeFiles.length < 2) return alert('Hãy chọn ít nhất 2 video.');

  runFFmpeg(mergeRun, 'Ghép video', async () => {
    const ff = await getFFmpeg();
    const names = [];
    for (let i = 0; i < mergeFiles.length; i++) {
      const name = `in${i}.${extOf(mergeFiles[i].name)}`;
      await ff.writeFile(name, await fetchFile(mergeFiles[i]));
      names.push(name);
    }

    // Only keep the merged audio track if every input has one — mixing
    // audio-having and silent clips in one concat filter fails otherwise.
    let allHaveAudio = true;
    for (const name of names) {
      if (!(await hasAudioStream(ff, name))) {
        allHaveAudio = false;
        break;
      }
    }

    const filterParts = [];
    const concatRefs = [];
    names.forEach((_, i) => {
      filterParts.push(
        `[${i}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[v${i}]`,
      );
      if (allHaveAudio) {
        filterParts.push(`[${i}:a]aresample=44100[a${i}]`);
        concatRefs.push(`[v${i}][a${i}]`);
      } else {
        concatRefs.push(`[v${i}]`);
      }
    });
    const outputLabels = allHaveAudio ? '[outv][outa]' : '[outv]';
    filterParts.push(`${concatRefs.join('')}concat=n=${names.length}:v=1:a=${allHaveAudio ? 1 : 0}${outputLabels}`);

    const args = [];
    names.forEach((n) => args.push('-i', n));
    args.push('-filter_complex', filterParts.join(';'), '-map', '[outv]');
    if (allHaveAudio) args.push('-map', '[outa]', '-c:a', 'aac');
    args.push('-c:v', 'libx264', '-preset', 'ultrafast', 'output.mp4');

    await ff.exec(args);
    const data = await ff.readFile('output.mp4');
    showOutput(new Blob([data.buffer], { type: 'video/mp4' }), 'merged.mp4');
    for (const n of names) await ff.deleteFile(n);
    await ff.deleteFile('output.mp4');
  });
});

// ---------- Watermark / text overlay ----------
const watermarkInput = document.getElementById('watermark-input');
const watermarkPreview = document.getElementById('watermark-preview');
const watermarkRun = document.getElementById('watermark-run');
let watermarkFile = null;

watermarkInput.addEventListener('change', () => {
  watermarkFile = watermarkInput.files[0] || null;
  if (watermarkFile) watermarkPreview.src = URL.createObjectURL(watermarkFile);
});

function renderTextToPng(text, fontSize) {
  const canvas = document.createElement('canvas');
  const measureCtx = canvas.getContext('2d');
  measureCtx.font = `bold ${fontSize}px sans-serif`;
  const textWidth = Math.ceil(measureCtx.measureText(text).width);

  const padding = Math.ceil(fontSize * 0.5);
  canvas.width = textWidth + padding * 2;
  canvas.height = Math.ceil(fontSize * 1.6);

  const ctx = canvas.getContext('2d');
  ctx.font = `bold ${fontSize}px sans-serif`;
  ctx.textBaseline = 'middle';
  ctx.lineJoin = 'round';
  ctx.lineWidth = Math.max(2, fontSize * 0.1);
  ctx.strokeStyle = 'rgba(0,0,0,0.85)';
  ctx.fillStyle = 'rgba(255,255,255,0.95)';
  ctx.strokeText(text, padding, canvas.height / 2);
  ctx.fillText(text, padding, canvas.height / 2);

  return new Promise((resolve) => canvas.toBlob(resolve, 'image/png'));
}

const OVERLAY_POSITIONS = {
  'bottom-right': 'x=main_w-overlay_w-20:y=main_h-overlay_h-20',
  'bottom-left': 'x=20:y=main_h-overlay_h-20',
  'top-right': 'x=main_w-overlay_w-20:y=20',
  'top-left': 'x=20:y=20',
  center: 'x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2',
};

watermarkRun.addEventListener('click', () => {
  if (!watermarkFile) return alert('Hãy chọn video trước.');
  const text = document.getElementById('watermark-text').value.trim();
  if (!text) return alert('Hãy nhập nội dung chữ.');
  const position = document.getElementById('watermark-position').value;
  const fontSize = parseInt(document.getElementById('watermark-size').value, 10) || 24;

  runFFmpeg(watermarkRun, 'Chèn watermark', async () => {
    const ff = await getFFmpeg();
    const inputName = `input.${extOf(watermarkFile.name)}`;
    await ff.writeFile(inputName, await fetchFile(watermarkFile));

    const pngBlob = await renderTextToPng(text, fontSize);
    await ff.writeFile('watermark.png', await fetchFile(pngBlob));

    await ff.exec([
      '-i', inputName,
      '-i', 'watermark.png',
      '-filter_complex', `overlay=${OVERLAY_POSITIONS[position]}`,
      '-c:v', 'libx264',
      '-c:a', 'aac',
      '-preset', 'ultrafast',
      'output.mp4',
    ]);

    const data = await ff.readFile('output.mp4');
    showOutput(new Blob([data.buffer], { type: 'video/mp4' }), 'watermarked.mp4');
    await ff.deleteFile(inputName);
    await ff.deleteFile('watermark.png');
    await ff.deleteFile('output.mp4');
  });
});

// ---------- Convert / compress ----------
const convertInput = document.getElementById('convert-input');
const convertPreview = document.getElementById('convert-preview');
const convertRun = document.getElementById('convert-run');
const convertCrf = document.getElementById('convert-crf');
const convertCrfValue = document.getElementById('convert-crf-value');
let convertFile = null;

convertInput.addEventListener('change', () => {
  convertFile = convertInput.files[0] || null;
  if (convertFile) convertPreview.src = URL.createObjectURL(convertFile);
});

convertCrf.addEventListener('input', () => {
  convertCrfValue.textContent = convertCrf.value;
});

convertRun.addEventListener('click', () => {
  if (!convertFile) return alert('Hãy chọn video trước.');
  const format = document.getElementById('convert-format').value;
  const resolution = document.getElementById('convert-resolution').value;
  const crf = convertCrf.value;

  runFFmpeg(convertRun, 'Chuyển đổi', async () => {
    const ff = await getFFmpeg();
    const inputName = `input.${extOf(convertFile.name)}`;
    const outputName = `output.${format}`;
    await ff.writeFile(inputName, await fetchFile(convertFile));

    const args = ['-i', inputName];
    const vf = [];
    if (resolution !== 'original') vf.push(`scale=${resolution}`);

    if (format === 'gif') {
      vf.push('fps=10');
      args.push('-vf', vf.join(','), outputName);
    } else {
      if (vf.length) args.push('-vf', vf.join(','));
      if (format === 'mp4') {
        args.push('-c:v', 'libx264', '-crf', String(crf), '-preset', 'ultrafast', '-c:a', 'aac');
      } else if (format === 'webm') {
        args.push('-c:v', 'libvpx-vp9', '-crf', String(crf), '-b:v', '0', '-c:a', 'libopus');
      }
      args.push(outputName);
    }

    await ff.exec(args);
    const data = await ff.readFile(outputName);
    const kind = format === 'gif' ? 'image' : 'video';
    const mime = format === 'gif' ? 'image/gif' : `video/${format}`;
    showOutput(new Blob([data.buffer], { type: mime }), `converted.${format}`, kind);
    await ff.deleteFile(inputName);
    await ff.deleteFile(outputName);
  });
});
