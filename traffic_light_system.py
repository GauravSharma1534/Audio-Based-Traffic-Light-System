# traffic light system for visually impaired pedestrians
# gaurav sharma | 23bda70050 | chandigarh university
# minor project sem 3 - 2024
#
# HOW IT WORKS:
# sensor detects if someone is standing at crossing
# based on signal color it plays different beep sounds
# green = fast high beep (safe to walk)
# red = slow low beep (dont walk)
# yellow = medium beep (signal about to change)
#
# currently in simulation mode
# for raspberry pi deployment uncomment the GPIO and sounddevice parts

import time
import random
import threading
import numpy as np
import json
from datetime import datetime

# ---- config ----
GREEN_TIME  = 30
RED_TIME    = 20
YELLOW_TIME = 5
THRESHOLD   = 0.6      # sensor sensitivity

SAMPLE_RATE = 44100
DIRECTIONS  = ["North", "South", "East", "West"]


def make_tone(freq, dur, vol=0.5):
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
    return (vol * np.sin(2 * np.pi * freq * t)).astype(np.float32)

def beep_sequence(freq, beep_dur=0.1, pause=0.05, n=3):
    beep    = make_tone(freq, beep_dur)
    silence = np.zeros(int(SAMPLE_RATE * pause), dtype=np.float32)
    result  = []
    for _ in range(n):
        result.append(beep)
        result.append(silence)
    return np.concatenate(result)

def play(signal_state, direction):
    # i chose these frequencies after some testing - they sound clearly different
    # 880hz = bright/positive -> walk
    # 550hz = neutral         -> caution
    # 330hz = dull/warning    -> stop
    freq_map = {"GREEN": 880, "YELLOW": 550, "RED": 330}
    freq = freq_map[signal_state]

    if signal_state == "GREEN":
        audio = beep_sequence(freq, beep_dur=0.08, pause=0.04, n=4)
        print(f"    [sound] WALK  {direction}  ({freq}hz fast)")
    elif signal_state == "YELLOW":
        audio = beep_sequence(freq, beep_dur=0.15, pause=0.1, n=2)
        print(f"    [sound] WAIT  {direction}  ({freq}hz)")
    else:
        audio = beep_sequence(freq, beep_dur=0.2, pause=0.3, n=2)
        print(f"    [sound] STOP  {direction}  ({freq}hz slow)")

    # real hardware output:
    # import sounddevice as sd
    # sd.play(audio, SAMPLE_RATE)
    # sd.wait()

    return audio


class ProxSensor:
    def __init__(self, direction):
        self.direction = direction

    def read(self):
        # simulation - random pedestrian arrivals
        val = random.random()
        return val > (1 - THRESHOLD)

        # real hardware (raspberry pi):
        # import RPi.GPIO as GPIO
        # GPIO.output(TRIG, True)
        # time.sleep(0.00001)
        # GPIO.output(TRIG, False)
        # while GPIO.input(ECHO) == 0: pulse_start = time.time()
        # while GPIO.input(ECHO) == 1: pulse_end = time.time()
        # distance = (pulse_end - pulse_start) * 17150
        # return distance < 100


class TrafficSignal:
    def __init__(self, direction, initial_state="RED"):
        self.direction = direction
        self.state     = initial_state
        self.sensor    = ProxSensor(direction)
        self.crossings = 0
        self.waits     = []
        self.cycles    = 0

    def get_time(self):
        if self.state == "GREEN":  return GREEN_TIME
        if self.state == "YELLOW": return YELLOW_TIME
        return RED_TIME

    def next_state(self):
        nxt = {"GREEN": "YELLOW", "YELLOW": "RED", "RED": "GREEN"}
        self.state = nxt[self.state]
        self.cycles += 1

    def run_loop(self, stop_flag):
        while not stop_flag.is_set():
            t   = self.get_time()
            ela = 0
            print(f"\n  [{self.direction}]  {self.state}  ({t}s)")

            while ela < t and not stop_flag.is_set():
                if self.sensor.read():
                    play(self.state, self.direction)
                    if self.state == "GREEN":
                        self.crossings += 1
                        self.waits.append(round(ela, 1))
                time.sleep(0.5)
                ela += 0.5

            self.next_state()

    def stats(self):
        avg = round(sum(self.waits)/len(self.waits), 2) if self.waits else 0
        return {"direction": self.direction, "crossings": self.crossings,
                "avg_wait": avg, "cycles": self.cycles}


class Intersection:
    def __init__(self):
        self._stop = threading.Event()
        # north-south start green, east-west wait (mirrors real intersection)
        init = {"North": "GREEN", "South": "GREEN", "East": "RED", "West": "RED"}
        self.signals = {d: TrafficSignal(d, init[d]) for d in DIRECTIONS}

    def start(self, run_for=30):
        print("=" * 46)
        print("  audio traffic light system")
        print("  gaurav sharma  |  23bda70050")
        print("  chandigarh university  |  2024")
        print("=" * 46)
        print(f"\nrunning for {run_for}s ...\n")

        threads = []
        for sig in self.signals.values():
            t = threading.Thread(target=sig.run_loop, args=(self._stop,), daemon=True)
            threads.append(t)
            t.start()

        try:
            time.sleep(run_for)
        except KeyboardInterrupt:
            print("\nstopped manually")

        self._stop.set()
        for t in threads:
            t.join(timeout=2)

        print("\n" + "=" * 46)
        print("  stats")
        print("=" * 46)
        for sig in self.signals.values():
            s = sig.stats()
            print(f"  {s['direction']:6s}  crossings={s['crossings']:3d}  avg_wait={s['avg_wait']}s  cycles={s['cycles']}")
        print("=" * 46)

        with open("traffic_log.json", "w") as f:
            json.dump({"run_at": datetime.now().strftime("%d-%m-%Y %H:%M"),
                       "results": [s.stats() for s in self.signals.values()]}, f, indent=2)
        print("\nlog -> traffic_log.json\ndone.")


if __name__ == "__main__":
    system = Intersection()
    system.start(run_for=30)
