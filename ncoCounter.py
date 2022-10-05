import os

from migen import *
from migen.genlib.cdc import MultiReg

from litex.soc.interconnect.csr import *

from litex.build.VHDLWrapper import *

class NCOCounter(Module, AutoCSR):
    def __init__(self, platform, counter_size, data_size):

        self.platform = platform

        # next interface
        self.cos = Signal(data_size)
        self.sin = Signal(data_size)
        self.en = Signal()
        self.sq_cos = Signal()
        self.sq_sin = Signal()
        self.sq_en  = Signal()
        self.trig   = Signal()

        self.enable = Signal()
        self.max_accum = Signal(32)
        self.poff = Signal(12)
        self.pinc_l = Signal(32)
        self.pinc_h = Signal(32)
        self.pinc = Signal(64)
        self.comb += self.pinc.eq(Cat(self.pinc_l, self.pinc_h))
        lut_size = 12

        self.ip_params = dict(
            p_LUT_SIZE     = lut_size,
            p_DATA_SIZE    = data_size,
            p_COUNTER_SIZE = counter_size,
            i_cpu_clk_i    = ClockSignal(),
            i_clk_i        = ClockSignal(),
            i_rst_i        = ResetSignal(),
            i_enable_i     = self.enable,
            i_sync_i       = 0,
            i_trig_i       = 1,#trig,
            i_max_accum_i  = self.max_accum,
            i_cpt_off_i    = 0,#self.poff,
            i_cpt_inc_i    = self.pinc[0:counter_size],
            o_cos_o        = self.cos,
            o_sin_o        = self.sin,
            o_wave_en_o    = self.en,
            o_sq_en_o      = self.sq_en,
            o_cos_fake_o   = self.sq_cos,
            o_sin_fake_o   = self.sq_sin
        )

        #vdir = os.path.join("nco_counter", "hdl")
        vdir = os.path.join(os.getenv("OSCIMP_DIGITAL_IP"), "nco_counter", "hdl")
        print(vdir)
        sources = [
            os.path.join(vdir, "nco_counter_logic.vhd"),
            os.path.join(vdir, "nco_counter_cos_rom.vhd"),
            os.path.join(vdir, "nco_counter_cos_rom_a12_d16.vhd"),
            os.path.join(vdir, "nco_counter_cos_rom_a16_d16.vhd"),
        ]

        self.submodules += VHDLWrapper(platform,
                "nco_counter_logic",
                build_dir     = os.path.abspath(os.path.dirname(__file__)),
                force_convert = False,
                add_instance  = True,
                params=self.ip_params,
                files=sources)

        self._enable    = CSRStorage()
        self._max_accum = CSRStorage(32)
        self._poff      = CSRStorage(12)
        self._pinc_l    = CSRStorage(32)
        self._pinc_h    = CSRStorage(32)
        self.specials  += MultiReg(self._enable.storage, self.enable)
        self.specials  += MultiReg(self._max_accum.storage, self.max_accum)
        self.specials  += MultiReg(self._poff.storage, self.poff)
        self.specials  += MultiReg(self._pinc_l.storage, self.pinc_l)
        self.specials  += MultiReg(self._pinc_h.storage, self.pinc_h)
