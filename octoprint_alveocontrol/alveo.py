import re

import serial


class AlveoController:
    status_regex = r"\#([a-z0-9A-Z]+:?[0-9]*%?)\#"

    def __init__(self, port: str = "/dev/AMA0"):
        self.baudrate = 9600
        self.port = port

    def _send_command(self, command: str):
        retries = 0
        while self.status != command:
            with serial.Serial(self.port, self.baudrate) as ser:
                ser.write(bytes(command, "ascii"))
            retries += 1
            if retries > 3:
                return

    @property
    def status(self):
        with serial.Serial(self.port, self.baudrate) as ser:
            line = ser.readline()
        matches = re.search(self.status_regex, line)
        return matches.group(1)

    def start(self):
        self._send_command("start;")

    def stop(self):
        self._send_command("stop;")

    def fast(self):
        self._send_command("fast;")

    def speed(self, speed: int):
        if speed > 100 or speed < 0:
            raise ValueError("Fan speed has to be between 0 and 100%.")

        self._send_command(f"pwm:{speed}%;")
