#!/usr/bin/env python3

import argparse
import os

from migen import *

from migen.genlib.io import CRG

from litex.build.generic_platform import IOStandard, Subsignal, Pins
from litex_boards.platforms import colorlight_5a_75b

from litex.build.lattice.trellis import trellis_args, trellis_argdict

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *

from ios import Led

# IOs ----------------------------------------------------------------------------------------------

_serial = [
    ("serialJ1", 0,
        Subsignal("tx", Pins("j1:0")), # J1.1
        Subsignal("rx", Pins("j1:1")), # J1.2
        IOStandard("LVCMOS33")
    ),
]

# BaseSoC -----------------------------------------------------------------------------------------

class BaseSoC(SoCCore):
    def __init__(self, revision):
        platform = colorlight_5a_75b.Platform(revision)
        sys_clk_freq = int(25e6)

        # custom serial using j1 pins instead of led & button
        platform.add_extension(_serial)

        # SoC with CPU
        SoCCore.__init__(self, platform,
            cpu_type                 = "vexriscv",
            clk_freq                 = 25e6,
            ident                    = "LiteX CPU Test SoC 5A-75B", ident_version=True,
            integrated_rom_size      = 0x8000,
            integrated_main_ram_size = 0x4000,
            uart_name                = "serialJ1")

        # Clock Reset Generation
        self.submodules.crg = CRG(platform.request("clk25"), ~platform.request("user_btn_n"))

        # Led
        user_leds = Cat(*[platform.request("user_led_n", i) for i in range(1)])
        self.submodules.leds = Led(user_leds)
        self.add_csr("leds")


# Build --------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LiteX SoC on Colorlight 5A-75B")
    builder_args(parser)
    soc_core_args(parser)
    trellis_args(parser)
    parser.add_argument("--build", action="store_true", help="Build bitstream")
    parser.add_argument("--load",  action="store_true", help="Load bitstream")
    parser.add_argument("--cable", default="ft2232",    help="JTAG probe model")
    args = parser.parse_args()

    soc = BaseSoC(revision="7.0")

    builder = Builder(soc, **builder_argdict(args))
    builder.build(**trellis_argdict(args), run=args.build)

    if args.load:
        print(args.cable)
        os.system("openFPGALoader -c " + args.cable + " " + \
            os.path.join(builder.gateware_dir, soc.build_name + ".bit"))

if __name__ == "__main__":
    main()
