// Renders index.html frame-by-frame with headless Chromium and pipes
// the frames into ffmpeg.  Usage:
//   node render.mjs [uz|en]            -> out/art-suzani-<lang>.mp4
//   node render.mjs uz --stills 2,5,9  -> out/still-<t>.jpg (quick check)
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdirSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const lang = process.argv[2] === 'en' ? 'en' : 'uz';
const stillsArg = process.argv.indexOf('--stills');
const FPS = 30, DUR = 20;
mkdirSync(path.join(dir, 'out'), { recursive: true });

const browser = await chromium.launch({
  executablePath: existsSync('/opt/pw-browsers/chromium') ? undefined : undefined,
  args: ['--allow-file-access-from-files'],
});
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto(`file://${dir}/index.html?render=1&lang=${lang}`);
await page.evaluate(() => window.ready);

const grab = async t => {
  const b64 = await page.evaluate(t => {
    window.renderFrame(t);
    return document.getElementById('c').toDataURL('image/jpeg', 0.95).split(',')[1];
  }, t);
  return Buffer.from(b64, 'base64');
};

if (stillsArg > 0) {
  const { writeFileSync } = await import('node:fs');
  for (const s of process.argv[stillsArg + 1].split(',')) {
    writeFileSync(path.join(dir, 'out', `still-${lang}-${s}.jpg`), await grab(parseFloat(s)));
  }
} else {
  const out = path.join(dir, 'out', `video-${lang}.mp4`);
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out],
    { stdio: ['pipe', 'ignore', 'inherit'] });
  const N = FPS * DUR;
  for (let i = 0; i < N; i++) {
    const buf = await grab(i / FPS);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 60 === 0) console.log(`frame ${i}/${N}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log('wrote', out);
}
await browser.close();
