#!/usr/bin/env python3

from migen import *

from migen.genlib.io import CRG

from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *

from ios import Led

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # clock
    ("clk25", 0, Pins("P6"), IOStandard("LVCMOS33")),

    # led (n)
    ("user_led", 0, Pins("P11"), IOStandard("LVCMOS33")),
    
    # btn (n)
    ("cpu_reset", 0, Pins("M13"), IOStandard("LVCMOS33")),
    
    ("serial", 0,
        Subsignal("tx", Pins("F3")), # J1.1
        Subsignal("rx", Pins("F1")), # J1.2
        IOStandard("LVCMOS33")),

]

# Platform -----------------------------------------------------------------------------------------

class Platform(LatticePlatform):
    default_clk_name   = "clk25"
    default_clk_period = 1e9/25e6

    def __init__(self):
        LatticePlatform.__init__(self, "LFE5U-25F-6BG256C", _io, toolchain="trellis")

# Design -------------------------------------------------------------------------------------------

# Create our platform (fpga interface)
platform = Platform()

# Create our soc (fpga description)
class BaseSoC(SoCCore):
    def __init__(self, platform):
        sys_clk_freq = int(25e6)

        # SoC with CPU
        SoCCore.__init__(self, platform,
            cpu_type                 = "vexriscv",
            clk_freq                 = 25e6,
            ident                    = "LiteX CPU Test SoC 5A-75B", ident_version=True,
            integrated_rom_size      = 0x8000,
            integrated_main_ram_size = 0x4000)

        # Clock Reset Generation
        self.submodules.crg = CRG(platform.request("clk25"), ~platform.request("cpu_reset"))

        # Led
        user_leds = Cat(*[platform.request("user_led", i) for i in range(1)])
        self.submodules.leds = Led(user_leds)
        self.add_csr("leds")

soc = BaseSoC(platform)

# Build --------------------------------------------------------------------------------------------

builder = Builder(soc, output_dir="build", csr_csv="test/csr.csv")
builder.build()
