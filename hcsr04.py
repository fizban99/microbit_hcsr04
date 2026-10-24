from microbit import spi
from microbit import pin13, pin14, pin15


class HCSR04:

    def __init__(self, tpin=pin15, epin=pin14, spin=pin13):
        self.trigger_pin = tpin
        self.echo_pin = epin
        self.sclk_pin = spin

    def distance_mm(self):
        spi.init(baudrate=125000, sclk=self.sclk_pin,
                 mosi=self.trigger_pin, miso=self.echo_pin)
        length = 500
        resp = bytearray(length)
        resp[0] = 0xFF
        spi.write_readinto(resp, resp)
        # A capture starting high has no observed rising edge.
        if resp[0] & 0x80:
            return -1
        pulse_bits = 0
        for value in resp:
            # SPI captures the most significant bit first.
            for shift in range(7, -1, -1):
                if value & (1 << shift):
                    pulse_bits += 1
                elif pulse_bits:
                    return round((pulse_bits * 8 * 0.172) / 2)
        # No pulse, or the falling edge lies outside the capture.
        return -1
