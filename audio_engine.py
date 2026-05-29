

import numpy as np

SAMPLE_RATE = 44100


FREQS = {
    "GREEN":  880,
    "YELLOW": 550,
    "RED":    330
}

def sine_wave(freq, duration, volume=0.5):
    t    = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = volume * np.sin(2 * np.pi * freq * t)
    return wave.astype(np.float32)

def beeps(freq, beep_len=0.1, gap=0.05, count=3):
    tone    = sine_wave(freq, beep_len)
    silence = np.zeros(int(SAMPLE_RATE * gap), dtype=np.float32)
    parts   = []
    for _ in range(count):
        parts.append(tone)
        parts.append(silence)
    return np.concatenate(parts)

def get_audio(state):
    """returns numpy audio array for given signal state"""
    freq = FREQS[state]
    if state == "GREEN":
        return beeps(freq, beep_len=0.08, gap=0.04, count=4)
    elif state == "YELLOW":
        return beeps(freq, beep_len=0.15, gap=0.1, count=2)
    else:
        return beeps(freq, beep_len=0.2, gap=0.3, count=2)

def play(state, direction):
    audio = get_audio(state)
    msgs = {
        "GREEN":  f"WALK  {direction}  ({FREQS[state]}hz)",
        "YELLOW": f"WAIT  {direction}  ({FREQS[state]}hz)",
        "RED":    f"STOP  {direction}  ({FREQS[state]}hz)"
    }
    print(f"    [sound] {msgs[state]}")

    
    return audio


if __name__ == "__main__":
    import time
    print("testing audio engine...")
    for state in ["GREEN", "YELLOW", "RED"]:
        print(f"state: {state}")
        play(state, "TestDir")
        time.sleep(0.3)
    print("done")
