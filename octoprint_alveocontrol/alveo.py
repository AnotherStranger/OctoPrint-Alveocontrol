from typing import Union

import serial


class AlveoController:
    def __init__(self, port: str = "/dev/ttyAMA0"):
        self.baudrate = 9600
        self.port = port
        self.status_regex = r"\#(.*)\#"

    def _send_command(self, command: str):
        with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
            ser.write(bytes(f"{command};", "ascii"))
            try:
                status = ser.read_until(expected=b"#{command}#")
            except serial.SerialTimeoutException:
                raise ValueError("Command not acked: {status}")

    def start(self, speed=100):
        self._send_command("start")
        self.speed(speed)

    def stop(self):
        self._send_command("stop")

    def fast(self):
        self._send_command("fast")

    def speed(self, speed: Union[str, int]):
        if not isinstance(speed, int):
            speed = int(speed)

        if speed > 100 or speed < 0:
            raise ValueError("Fan speed has to be between 0 and 100%.")

        self._send_command(f"pwm:{speed}%")
