import serial


class AlveoController:
    def __init__(self, port: str = "/dev/AMA0"):
        self.baudrate = 9600
        self.port = port

    def _send_command(self, command: str):
        with serial.Serial(self.port, self.baudrate) as ser:
            ser.write(bytes(command, "ascii"))

    def start(self):
        self._send_command("start;")

    def stop(self):
        self._send_command("stop;")

    def fast(self):
        self._send_command("fast;")
