
import sys

def test_sensor():
    print("testing sensor...")
    from sensor import ProxSensor
    s = ProxSensor("North", threshold=0.6)
    reads = [s.read() for _ in range(15)]
    assert len(reads) == 15
    assert isinstance(s.detection_rate(), float)
    print(f"  detections: {sum(reads)}/15, rate={s.detection_rate()}%  OK")

def test_audio():
    print("testing audio...")
    import numpy as np
    from audio_engine import get_audio, FREQS
    for state in ["GREEN", "YELLOW", "RED"]:
        audio = get_audio(state)
        assert len(audio) > 0
        assert audio.dtype == np.float32
    print(f"  all states generated OK")
    print(f"  freqs: GREEN={FREQS['GREEN']}hz  YELLOW={FREQS['YELLOW']}hz  RED={FREQS['RED']}hz")

def test_config():
    print("testing config...")
    from config import CONFIG
    assert CONFIG["green_time"] > 0
    assert CONFIG["red_time"] > 0
    assert 0 < CONFIG["threshold"] < 1
    assert len(CONFIG["directions"]) == 4
    print(f"  config OK")

if __name__ == "__main__":
    print("running tests\n" + "-"*30)
    failed = 0
    for fn in [test_sensor, test_audio, test_config]:
        try:
            fn()
        except Exception as e:
            print(f"  FAILED: {e}")
            failed += 1
    print("-"*30)
    print(f"done. {3-failed}/3 passed")
    sys.exit(failed)
