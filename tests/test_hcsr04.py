"""Run the real driver against synthetic SPI captures, without hardware."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, patch


class DistanceTests(unittest.TestCase):
    def measure(self, capture):
        spi = Mock()

        def readinto(outgoing, incoming):
            incoming[:] = bytes(capture) + bytes(500 - len(capture))

        spi.write_readinto.side_effect = readinto
        microbit = types.ModuleType("microbit")
        microbit.spi = spi
        microbit.pin13, microbit.pin14, microbit.pin15 = 13, 14, 15
        spec = importlib.util.spec_from_file_location(
            "driver_under_test", Path(__file__).resolve().parents[1] / "hcsr04.py")
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"microbit": microbit}):
            spec.loader.exec_module(module)
        return module.HCSR04().distance_mm()

    def test_single_full_byte_is_counted_once(self):
        self.assertEqual(self.measure([0, 255, 0]), 6)

    def test_partial_bytes_are_counted_once(self):
        self.assertEqual(self.measure([0, 15, 255, 240, 0]), 11)

    def test_pulse_inside_one_byte(self):
        self.assertEqual(self.measure([0, 60, 0]), 3)

    def test_capture_starting_high_is_incomplete(self):
        self.assertEqual(self.measure([255, 0]), -1)

    def test_no_echo(self):
        self.assertEqual(self.measure([]), -1)

    def test_unfinished_echo(self):
        self.assertEqual(self.measure([0] + [255] * 499), -1)

    def test_complete_echo_at_end_of_capture(self):
        self.assertEqual(self.measure([0] * 499 + [240]), 3)

    def test_only_first_pulse_is_measured(self):
        self.assertEqual(self.measure([0, 240, 255, 0]), 3)

    def test_pulse_length_does_not_depend_on_byte_alignment(self):
        for offset in range(1, 9):
            for width in (1, 4, 8, 9, 16, 31):
                with self.subTest(offset=offset, width=width):
                    bits = "0" * offset + "1" * width + "0" * 8
                    bits += "0" * (-len(bits) % 8)
                    capture = [int(bits[i:i + 8], 2)
                               for i in range(0, len(bits), 8)]
                    self.assertEqual(self.measure(capture),
                                     round(width * 8 * 0.172 / 2))


if __name__ == "__main__":
    unittest.main()
