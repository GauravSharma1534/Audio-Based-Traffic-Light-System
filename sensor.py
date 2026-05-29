

import random
import threading

class ProxSensor:
    """
    ultrasonic proximity sensor wrapper
    simulation mode by default
    for real hardware see commented GPIO code below
    """

    def __init__(self, direction, threshold=0.6):
        self.direction = direction
        self.threshold = threshold
        self._lock = threading.Lock()
        self._count = 0
        self._hits  = 0

    def read(self):
        with self._lock:
            self._count += 1
            # simulation
            val = random.random()
            detected = val > (1 - self.threshold)
            if detected:
                self._hits += 1
            return detected

        # --- raspberry pi gpio (uncomment) ---
        # import RPi.GPIO as GPIO
        # TRIG = 23
        # ECHO = 24
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(TRIG, GPIO.OUT)
        # GPIO.setup(ECHO, GPIO.IN)
        # GPIO.output(TRIG, True)
        # time.sleep(0.00001)
        # GPIO.output(TRIG, False)
        # while GPIO.input(ECHO) == 0:
        #     pulse_start = time.time()
        # while GPIO.input(ECHO) == 1:
        #     pulse_end = time.time()
        # distance = (pulse_end - pulse_start) * 17150  # cm
        # return distance < 100  # within 1 meter

    def detection_rate(self):
        with self._lock:
            if self._count == 0:
                return 0
            return round((self._hits / self._count) * 100, 1)


if __name__ == "__main__":
    # quick test
    s = ProxSensor("North")
    results = [s.read() for _ in range(20)]
    print(f"detections: {sum(results)}/20")
    print(f"rate: {s.detection_rate()}%")
