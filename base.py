#!/usr/bin/env python3

import argparse
import os

from migen import *

from migen.genlib.io import CRG

from litex.build.generic_platform import IOStandard, Subsignal, Pins
from litex.build.openfpgaloader import OpenFPGALoader

from litex_boards.platforms import colorlight_5a_75b
from litex_boards.platforms import colorlight_i5

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
    def __init__(self, version, revision):
        sys_clk_freq = int(25e6)

        if version == "5A-75B":
            platform = colorlight_5a_75b.Platform(revision)
            # custom serial using j1 pins instead of led & button
            platform.add_extension(_serial)
            serial_name = "serialJ1"
            reset_name = "user_btn_n"
        else:
            platform = colorlight_i5.Platform(revision)
            serial_name = "serial"
            reset_name = "cpu_reset_n"

        # SoC with CPU
        SoCCore.__init__(self, platform,
            cpu_type                 = "vexriscv",
            clk_freq                 = 25e6,
            ident                    = f"LiteX CPU Test SoC {version}", ident_version=True,
            integrated_rom_size      = 0x8000,
            integrated_main_ram_size = 0x4000,
            uart_name                = serial_name)

        # Clock Reset Generation
        self.submodules.crg = CRG(platform.request("clk25"),
                ~platform.request(reset_name))

        # Led
        user_leds = Cat(*[platform.request("user_led_n", i) for i in range(1)])
        self.submodules.leds = Led(user_leds)
        self.add_csr("leds")


# Build --------------------------------------------------------------------------------------------

def main():

    #programmer = OpenFPGALoader("colorlight-i5")
    #programmer = OpenFPGALoader(cable="digilent_hs2")
    #programmer = OpenFPGALoader(freq=30e6)
    #programmer = OpenFPGALoader("colorlight-i5", "digilent_hs2", 30e6)
    #programmer = OpenFPGALoader("colorlight-i5", cable="digilent_hs2", freq=30e6)
    #programmer = OpenFPGALoader(cable="digilent_hs2", freq=30e6)
    #RETUrn
    parser = argparse.ArgumentParser(description="LiteX SoC on Colorlight 5A-75B")
    builder_args(parser)
    soc_core_args(parser)
    trellis_args(parser)
    parser.add_argument("--build", action="store_true", help="Build bitstream")
    parser.add_argument("--load",  action="store_true", help="Load bitstream")
    parser.add_argument("--cable", default="ft2232",    help="JTAG probe model")
    parser.add_argument("--version", default="5A-75B",  help="colorlight model (5A-75B / I5)")
    args = parser.parse_args()

    soc = BaseSoC(args.version, revision="7.0")

    builder = Builder(soc, **builder_argdict(args))
    builder.build(**trellis_argdict(args), run=args.build)

    if args.load:
        if args.version == "5A-75B":
            #programmer = OpenFPGALoader("colorlight", args.cable)
            os.system("openFPGALoader " + "-b colorlight -c " +  args.cable +
                " " + bitstream_file)
        else:
            programmer = OpenFPGALoader("colorlight-i5", freq=20e6)
            programmer.load_bitstream(os.path.join(builder.gateware_dir, soc.build_name + ".bit"))

if __name__ == "__main__":
    main()
