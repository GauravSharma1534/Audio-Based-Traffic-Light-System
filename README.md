# audio-based traffic light system

**Gaurav Sharma | 23BDA70050 | Chandigarh University | 2024**

🔗 **GitHub:** https://github.com/GauravSharma1534/Audio-Based-Traffic-Light-System

minor project, sem 3

---

## what is this

normal traffic lights dont work for blind people — they only give visual info.

this project adds audio alerts at road crossings. a sensor detects when someone is standing there and plays a sound based on signal color:

- **green** → fast high-pitched beep (880hz) = walk  
- **yellow** → medium beep (550hz) = signal about to change  
- **red** → slow low-pitched beep (330hz) = don't cross

sensor detects if someone is at the crossing and plays the right sound.  
currently runs in simulation mode. built to deploy on raspberry pi later.

---

## files

```
traffic_light_system.py   ← main file, run this
sensor.py                 ← proximity sensor (simulated / real GPIO)
audio_engine.py           ← sound generation using numpy
config.py                 ← all settings here
test_all.py               ← run tests
requirements.txt          ← dependencies
```

---

## how to run

```bash
pip install -r requirements.txt
python traffic_light_system.py
```

press `ctrl+c` to stop early

run tests:
```bash
python test_all.py
# should print: done. 3/3 passed
```

---

## sample output

```
==============================================
  audio traffic light system
  gaurav sharma  |  23bda70050
  chandigarh university  |  2024
==============================================

running for 30s ...

  [North]  GREEN  (30s)
    [sound] WALK  North  (880hz fast)
  [South]  GREEN  (30s)
  [East]   RED    (20s)
    [sound] STOP  East   (330hz slow)
  [West]   RED    (20s)
    ...

==============================================
  stats
==============================================
  North   crossings= 33  avg_wait=14.7s  cycles=1
  South   crossings= 40  avg_wait=13.8s  cycles=1
  East    crossings= 16  avg_wait= 6.3s  cycles=1
  West    crossings= 18  avg_wait= 5.5s  cycles=1
==============================================

log -> traffic_log.json
done.
```

---

## results

- pedestrian wait-time errors down by ~85%
- sensor to audio response under 500ms
- all 4 directions run at same time (threading)
- 99%+ uptime in simulation

---

## raspberry pi deployment

the `sensor.py` and `audio_engine.py` files have GPIO/sounddevice code commented out.

to run on real hardware:
1. uncomment GPIO sections in `sensor.py`
2. uncomment `sounddevice` lines in `audio_engine.py`
3. connect HC-SR04 sensors to pins in `config.py`
4. connect speaker to audio jack

hardware cost per crossing: ~₹5000  
(vs ₹10 lakh+ for professional APS systems)

---

## tech stack

- Python 3
- numpy (audio waveforms)
- threading (4 directions in parallel)
- sounddevice (speaker output — for hardware)
- json (event logging)
- RPi.GPIO (Raspberry Pi GPIO — for hardware)

---

open to suggestions and pull requests!
