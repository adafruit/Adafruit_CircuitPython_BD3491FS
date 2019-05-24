# The MIT License (MIT)
#
# Copyright (c) 2019 Bryan Siepert for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_bd3491fs`
================================================================================

A driver for the Rohm BD3491FS audio processor

* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**
 * Adafruit CircuitPython firmware for the supported boards:
    https://github.com/adafruit/circuitpython/releases
 * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
 * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register

"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BD3491FS.git"

from micropython import const
import adafruit_bus_device.i2c_device as i2cdevice
from adafruit_register.i2c_struct import UnaryStruct
from adafruit_register.i2c_bits import RWBits, ROBits
from adafruit_register.i2c_bit import RWBit
# pylint: disable=bad-whitespace
_INPUT_SELECTOR	 = const(0x04)
_INPUT_GAIN      = const(0x06)
_VOLUME_GAIN_CH1 = const(0x21)
_VOLUME_GAIN_CH2 = const(0x22)
_BASS_GAIN       = const(0x51)
_TREBLE_GAIN     = const(0x57)
_SURROUND_GAIN        = const(0x78)
_TEST_MODE       = const(0xF0)
_SYSTEM_RESET    = const(0xFE)
# pylint: enable=bad-whitespace

class Input: # pylint: disable=too-few-public-methods
    """Options for ``active_input``

        +---------------+------------------+
        | ``Input``       | Input Pair       |
        +===============+==================+
        | ``Input.A``     | Inputs A1 and A2 |
        +-----------------+------------------+
        | ``Input.B``     | Inputs B1 and B2 |
        +-----------------+------------------+
        | ``Input.C``     | Inputs C1 and C2 |
        +-----------------+------------------+
        | ``Input.D``     | Inputs D1 and D2 |
        +-----------------+------------------+
        | ``Input.E``     | Inputs E1 and E2 |
        +-----------------+------------------+
        | ``Input.F``     | Inputs F1 and F2 |
        +-----------------+------------------+
        | ``Input.SHORT`` | Short inputs     |
        +-----------------+------------------+
        | ``Input.MUTE``  | Mute all         |
        +-----------------+------------------+

    """
    A = const(0x00)
    B = const(0x01)
    C = const(0x02)
    D = const(0x03)
    E = const(0x04)
    F = const(0x06)
    SHORT = const(0x05)
    MUTE = const(0x07)
class InputGain: # pylint: disable=too-few-public-methods
    """Options for ``active_input``

        +---------------+------------------+
        | ``Input``       | Input Pair       |
        +===============+==================+
        | ``Input.A``     | Inputs A1 and A2 |
        +-----------------+------------------+
        | ``Input.B``     | Inputs B1 and B2 |
        +-----------------+------------------+
        | ``Input.C``     | Inputs C1 and C2 |
        +-----------------+------------------+
        | ``Input.D``     | Inputs D1 and D2 |
        +-----------------+------------------+
        | ``Input.E``     | Inputs E1 and E2 |
        +-----------------+------------------+
        | ``Input.F``     | Inputs F1 and F2 |
        +-----------------+------------------+
        | ``Input.SHORT`` | Short inputs     |
        +-----------------+------------------+
        | ``Input.MUTE``  | Mute all         |

    """
    GAIN_0DB = const(0x00)
    GAIN_2DB = const(0x01)
    GAIN_4DB = const(0x02)
    GAIN_6DB = const(0x03)
    GAIN_8DB = const(0x04)
    GAIN_10DB = const(0x05)
    GAIN_12DB = const(0x06)
    GAIN_14DB = const(0x07)
    GAIN_16DB = const(0x08)
    GAIN_20DB = const(0x0A)
    GAIN_OFF = const(0x00)
    GAIN_LOW = const(0x05)
    GAIN_MED = const(0x0A)
    GAIN_HIGH = const(0x0F)

    
class BD3491FS: # pylint: disable=too-many-instance-attributes
    """Driver for the Rohm BD3491FS audio processor

        :param ~busio.I2C i2c_bus: The I2C bus the BD3491FS is connected to.
        :param address: The I2C device address for the sensor. Default is ``WAKKA WAKKA WAKKA`` but will accept
            ``WAKKA WAKKA WAKKA`` when the ``SDO`` pin is connected to Ground.

    """

    _input_selector = RWBits(3, _INPUT_SELECTOR, 0, 1)
    _input_gain = RWBits(4, _INPUT_GAIN, 1, 1)
    _volume_gain_ch1 = RWBits(7, _VOLUME_GAIN_CH1, 0, 1)
    _volume_gain_ch2 = RWBits(7, _VOLUME_GAIN_CH2, 0, 1)
    _bass_gain = RWBits(3, _BASS_GAIN, 1, 1)
    bass_gain_cut = RWBit(_BASS_GAIN, 7)
    """Bass gain direcrtion. Set to True to cut the bass by the amount set in ``bass_gain``, or false
        to boost the bass by the given amount"""

    _treble_gain = RWBits(3, _TREBLE_GAIN, 1, 1)
    _treble_gain_cut = RWBit(_TREBLE_GAIN, 7)
    _surround_gain = RWBits(4, _SURROUND_GAIN, 0, 1)
    _surround_mode = RWBit(_SURROUND_GAIN, 7)

    _test_mode = UnaryStruct(_TEST_MODE, "<B")
    _system_reset = UnaryStruct(_SYSTEM_RESET, "<B")
    # _reset = RWBit(_CTRL_REG2, 2)
    # _reset_filter = ROBits(8, _LPFP_RES, 0, 1)
    # _chip_id = UnaryStruct(_WHO_AM_I, "<B")

    def __init__(self, i2c_bus, address=0x41):
        self.i2c_device = i2cdevice.I2CDevice(i2c_bus, address)
        # if self._chip_id != 0xb1:
        #     raise RuntimeError('Failed to find BD3491FS! Chip ID 0x%x' % self._chip_id)

        # self.reset()



        self._block_updates = True
        self._interrupt_latch = True

    def reset(self):
        """Reset the sensor, restoring all configuration registers to their defaults"""
        self._reset = True
        # wait for the reset to finish
        while self._reset:
            pass

    @property
    def active_input(self):
        """The currently selected input"""
        return self._input_selector

    @active_input.setter
    def active_input(self, value):
        self._input_selector = value

    @property
    def input_gain(self):
        """The gain applied to all inputs equally"""
        return self._input_gain
    
    @input_gain.setter
    def input_gain(self, value):
        allowed_gains = [0, 1, 2, 3, 4, 6, 8, 10]
        if not( value in allowed_gains):
            raise ValueError("input gain must be one of 0, 2, 4, 6, 8, 12, 16, 20 dB")
        

    @property
    def channel_1_gain(self):
        "The gain applied to channel 1 of the currently selected input pair in -dB"
        self._volume_gain_ch1

    @channel_1_gain.setter
    def channel_1_gain(self, value):
        if ((value < 0 ) or (value > 87)):
            raise ArgumentError("channel gain must be from 0-87db")
        self._volume_gain_ch1 = value
    
    @property
    def channel_2_gain(self):
        "The gain applied to channel 2 of the currently selected input pair in -dB"
        return self._volume_gain_ch2

    @channel_2_gain.setter
    def channel_2_gain(self, value):
        if ((value < 0 ) or (value > 87)):
            raise ArgumentError("channel gain must be from 0-87db")
        self._volume_gain_ch2 = value

    @property
    def bass_gain(self):
        """The amount of gain applied to the bass channel in dB"""
        return self._bass_gain

    @bass_gain.setter
    def bass_gain(self, value):
        allowed_gains = [0, 1, 2, 3, 4, 6, 7]
        if not( value in allowed_gains):
            raise ValueError("input gain must be one of 0, 2, 4, 6, 8, 12, 14 dB")
        self._bass_gain = value
    
    @property
    def treble_gain(self):
        """The amount of gain applied to the treble channel in dB"""
        return self._treble_gain 

    @treble_gain.setter
    def treble_gain(self, value):
        allowed_gains = [0, 1, 2, 3, 4, 6, 7]
        if not( value in allowed_gains):
            raise ValueError("input gain must be one of 0, 2, 4, 6, 8, 12, 14 dB")
        self._treble_gain = value

