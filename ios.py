from migen import *

from litex.soc.interconnect.csr import *
from litex.soc.cores import gpio

# See: https://github.com/enjoy-digital/litex/blob/master/litex/soc/cores/gpio.py

class Led(gpio.GPIOOut):
    pass

