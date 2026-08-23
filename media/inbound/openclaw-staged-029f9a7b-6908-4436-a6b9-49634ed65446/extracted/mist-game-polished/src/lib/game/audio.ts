// MIST Game Engine — Audio System (Expanded v2.0)
type SoundName =
  | 'move' | 'collect' | 'discover' | 'teach' | 'levelup'
  | 'error' | 'complete' | 'bark' | 'quest' | 'quest_complete'
  | 'splash' | 'step_grass' | 'step_stone' | 'ambient_farm'
  | 'ambient_forest' | 'ambient_village';

let ctx: AudioContext | null = null;
let muted = false;

function getCtx(): AudioContext {
  if (!ctx) ctx = new AudioContext();
  if (ctx.state === 'suspended') ctx.resume();
  return ctx;
}

function tone(
  context: AudioContext, freq: number, startAt: number, duration: number,
  wave: OscillatorType = 'sine', volume = 0.15,
): GainNode {
  const osc = context.createOscillator();
  const gain = context.createGain();
  osc.type = wave;
  osc.frequency.setValueAtTime(freq, startAt);
  gain.gain.setValueAtTime(volume, startAt);
  gain.gain.exponentialRampToValueAtTime(0.001, startAt + duration);
  osc.connect(gain); gain.connect(context.destination);
  osc.start(startAt); osc.stop(startAt + duration + 0.05);
  return gain;
}

export function playSound(name: SoundName): void {
  if (muted) return;
  const c = getCtx();
  const now = c.currentTime;

  switch (name) {
    case 'move':
      tone(c, 440, now, 0.08, 'sine', 0.06);
      break;
    case 'collect': {
      tone(c, 523, now, 0.1, 'sine', 0.12);
      tone(c, 659, now + 0.1, 0.12, 'sine', 0.12);
      break;
    }
    case 'discover': {
      const osc = c.createOscillator(); const gain = c.createGain();
      const vibrato = c.createOscillator(); const vibratoGain = c.createGain();
      osc.type = 'sine'; osc.frequency.setValueAtTime(880, now);
      vibrato.type = 'sine'; vibrato.frequency.setValueAtTime(6, now);
      vibratoGain.gain.setValueAtTime(20, now);
      vibrato.connect(vibratoGain); vibratoGain.connect(osc.frequency);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
      osc.connect(gain); gain.connect(c.destination);
      vibrato.start(now); osc.start(now);
      vibrato.stop(now + 0.35); osc.stop(now + 0.35);
      break;
    }
    case 'teach':
      tone(c, 660, now, 0.4, 'triangle', 0.12);
      break;
    case 'levelup': {
      [262, 330, 392, 523].forEach((freq, i) => tone(c, freq, now + i * 0.12, 0.2, 'sine', 0.12));
      break;
    }
    case 'error':
      tone(c, 220, now, 0.15, 'sawtooth', 0.06);
      break;
    case 'complete': {
      [262, 330, 392, 523, 659].forEach((freq, i) => tone(c, freq, now + i * 0.15, 0.25, 'sine', 0.12));
      break;
    }
    case 'bark': {
      tone(c, 180, now, 0.08, 'square', 0.15);
      tone(c, 220, now + 0.06, 0.12, 'square', 0.12);
      break;
    }
    case 'quest':
      tone(c, 440, now, 0.1, 'triangle', 0.1);
      tone(c, 550, now + 0.1, 0.15, 'triangle', 0.1);
      break;
    case 'quest_complete': {
      [392, 494, 587, 659, 784].forEach((freq, i) => tone(c, freq, now + i * 0.1, 0.2, 'sine', 0.1));
      break;
    }
    case 'splash': {
      const noise = c.createBufferSource();
      const buf = c.createBuffer(1, c.sampleRate * 0.2, c.sampleRate);
      const data = buf.getChannelData(0);
      for (let i = 0; i < data.length; i++) data[i] = (Math.random() * 2 - 1) * (1 - i / data.length);
      noise.buffer = buf;
      const g = c.createGain();
      g.gain.setValueAtTime(0.08, now);
      g.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
      const filter = c.createBiquadFilter(); filter.type = 'lowpass'; filter.frequency.value = 2000;
      noise.connect(filter); filter.connect(g); g.connect(c.destination);
      noise.start(now);
      break;
    }
    case 'step_grass':
      tone(c, 800 + Math.random() * 200, now, 0.03, 'sine', 0.02);
      break;
    case 'step_stone':
      tone(c, 200 + Math.random() * 100, now, 0.04, 'triangle', 0.04);
      break;
    default:
      break;
  }
}

export function toggleMute(): boolean { muted = !muted; return muted; }
export function isMuted(): boolean { return muted; }
