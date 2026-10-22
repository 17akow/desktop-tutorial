"""Generates an original 20s soundtrack (no licensing issues):
drone pad + plucked melody in a Hijaz-like mode + doira-style frame drum,
with whooshes on scene transitions.  Output: out/music.wav"""
import numpy as np, wave, os

SR, DUR = 44100, 20.0
N = int(SR * DUR)
t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(5)

def add(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR); j = min(N, i + len(sig))
    if i >= N: return
    s = sig[: j - i] * gain
    L[i:j] += s * np.sqrt(0.5 * (1 - pan)); R[i:j] += s * np.sqrt(0.5 * (1 + pan))

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

# --- drone pad (D + A), slow swell, slightly detuned saws low-passed ---
def lowpass(x, a):
    y = np.empty_like(x); acc = 0.0
    for k in range(len(x)): acc += a * (x[k] - acc); y[k] = acc
    return y
pad = np.zeros(N)
for m, g in [(38, 1.0), (45, .7), (50, .5), (57, .25)]:
    for d in (-0.12, 0.12):
        f = hz(m + d)
        pad += g * (2 * ((t * f) % 1) - 1)
pad = lowpass(pad, 0.035)
env = np.clip(t / 2.5, 0, 1) * (1 - np.clip((t - 18.3) / 1.7, 0, 1))
pad *= env * 0.05
L += pad; R += pad

# --- plucked string (Karplus-Strong), dutar/rubab-like ---
def pluck(f, dur=1.4, bright=0.5):
    n = int(SR * dur); p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p) * bright + (1 - bright) * np.sin(np.linspace(0, 2 * np.pi, p))
    out = np.zeros(n)
    for k in range(n):
        out[k] = buf[k % p]
        buf[k % p] = 0.5 * (buf[k % p] + buf[(k + 1) % p]) * 0.996
    return out * np.exp(-np.arange(n) / SR * 1.6)

BPM = 100; beat = 60 / BPM; e = beat / 2
# D Hijaz: D Eb F# G A Bb C D
scale = [62, 63, 66, 67, 69, 70, 72, 74, 75, 78]
phrase = [0, 2, 3, 4, None, 3, 2, 1, 0, None, 4, 5, 4, 3, 2, None,
          4, 6, 7, None, 6, 5, 4, 3, 4, None, 2, 3, 1, None, 0, None]
cache = {}
for rep, off in enumerate([0.4, 0.4 + 32 * e]):
    for k, deg in enumerate(phrase):
        if deg is None: continue
        st = off + k * e
        if st > 18.6: break
        m = scale[deg] + (12 if rep == 1 and k > 16 else 0)
        if m not in cache: cache[m] = pluck(hz(m))
        add(cache[m], st, pan=0.25 if k % 2 else -0.25, gain=0.22)
# octave bass notes on downbeats
for k in range(int(18 / (4 * beat))):
    m = 38 if (k % 4) != 3 else 43
    if m not in cache: cache[m] = pluck(hz(m), 2.0, 0.2)
    add(cache[m], 3.6 + k * 4 * beat, gain=0.3)

# --- doira (frame drum) ---
def dum():
    n = int(SR * .45); tt = np.arange(n) / SR
    f = 55 + 70 * np.exp(-tt * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
def tak(bright=1.0):
    n = int(SR * .12); tt = np.arange(n) / SR
    x = rng.uniform(-1, 1, n); x = x - lowpass(x, 0.25 * bright)
    return x * np.exp(-tt * 45) + 0.3 * np.sin(2 * np.pi * 380 * tt) * np.exp(-tt * 30)
D, Tk = dum(), tak()
pattern = ['D', None, 'T', 'T', None, 'T', 'D', 'T']  # 8ths
start = 3.9
for k in range(int((19.2 - start) / e)):
    s = pattern[k % 8]
    st = start + k * e
    if 15.4 < st < 16.0: continue           # breath before the final reveal
    if s == 'D': add(D, st, gain=0.75)
    elif s == 'T': add(Tk, st, pan=0.35, gain=0.22 + 0.06 * (k % 3 == 0))
# fills into scenes
for st in (7.2, 12.0):
    for q in range(4): add(Tk, st + q * e / 2, pan=-0.3, gain=0.25)

# --- whooshes and impacts at transitions ---
def whoosh(d=0.9):
    n = int(SR * d); x = rng.uniform(-1, 1, n)
    k = np.linspace(0, 1, n); y = np.zeros(n); acc = 0.0
    for i in range(n):
        a = 0.01 + 0.25 * k[i] ** 2; acc += a * (x[i] - acc); y[i] = acc
    return y * (k ** 2) * (1 - k) ** 0.3 * 4
for at in (3.9, 7.9, 12.65, 16.05):
    add(whoosh(), at - 0.85, gain=0.35)
boom = dum(); boom = np.concatenate([boom, np.zeros(SR)])
add(np.sin(2 * np.pi * 45 * np.arange(int(SR * 1.6)) / SR) * np.exp(-np.arange(int(SR * 1.6)) / SR * 3), 16.05, gain=0.5)
# shimmer (gold sparkle) on the logo reveal
for q in range(14):
    f = hz(86 + [0, 3, 7, 10, 12][q % 5])
    tt = np.arange(int(SR * .6)) / SR
    add(np.sin(2 * np.pi * f * tt) * np.exp(-tt * 7), 16.4 + q * 0.07, pan=(q % 5 - 2) / 3, gain=0.05)

# master: soft clip, fades
mix = np.stack([L, R], 1)
mix *= (np.clip(t / .3, 0, 1) * (1 - np.clip((t - 19.2) / .8, 0, 1)))[:, None]
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
mix /= np.max(np.abs(mix)) + 1e-9; mix *= 0.89
os.makedirs('out', exist_ok=True)
with wave.open('out/music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('wrote out/music.wav')
