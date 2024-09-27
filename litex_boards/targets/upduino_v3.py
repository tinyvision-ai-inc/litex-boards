#!/usr/bin/env python3

#
# This file is not yet a part of LiteX-Boards
#

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex.gen import *

from litex_boards.platforms import upduino_v3

from litex.soc.cores.ram import Up5kSPRAM
# from litex.soc.cores.clock import iCE40PLL
from litex.soc.integration.soc_core import *
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.builder import *

kB = 1024
mB = 1024*kB


# CRG ----------------------------------------------------------------------------------------------

class _CRG(LiteXModule):
    def __init__(self, platform, sys_clk_freq):
        self.rst       = Signal()
        self.cd_sys    = ClockDomain()
        self.cd_por    = ClockDomain()

        # Clk/Rst
        sys = platform.request("clk12")
        platform.add_period_constraint(sys, 1e9/12e6)

        # Power On Reset
        por_count = Signal(16, reset=2**16-1)
        por_done  = Signal()
        self.comb += self.cd_por.clk.eq(ClockSignal("sys"))
        self.comb += por_done.eq(por_count == 0)
        self.sync.por += If(~por_done, por_count.eq(por_count - 1))

        # Sys Clk
        self.comb += self.cd_sys.clk.eq(sys)
        self.specials += AsyncResetSynchronizer(self.cd_sys, ~por_done)
     
# BaseSoc -----------------------------------------------------------------------------------------
class BaseSoC(SoCCore):
    def __init__(self, bios_flash_offset, sys_clk_freq=12e6, **kwargs):
        platform = upduino_v3.Platform()
        
        # CRG --------------------------------------------------------------------------------------
        self.crg = _CRG(platform, sys_clk_freq)
        
        # SoCCore ----------------------------------------------------------------------------------
        # Disable Integrated ROM/SRAM since too large for iCE40 and UP5K has specific SPRAM.
        kwargs["integrated_sram_size"] = 0
        kwargs["integrated_rom_size"]  = 0
        SoCCore.__init__(self, platform, sys_clk_freq, ident="LiteX SoC on Upduino_v3", **kwargs)
        
        #128KB SPRAM ------------------------------ -----------------------------------------------
        self.spram = Up5kSPRAM(size=128*kB) 
        self.bus.add_slave("sram", self.spram.bus, SoCRegion(size=128*kB))
           
        # SPI Flash 
        from litespi.modules import W25Q32JV
        from litespi.opcodes import SpiNorFlashOpCodes as Codes
        self.add_spi_flash(mode="1x", module=W25Q32JV(Codes.READ_1_1_1))  

        # Add ROM linker region --------------------------------------------------------------------
        self.bus.add_region("rom", SoCRegion(
            origin = self.bus.regions["spiflash"].origin + bios_flash_offset,
            size   = 32*kB,
            linker = True)
        )
        self.cpu.set_reset_address(self.bus.regions["rom"].origin)
        
# Flash --------------------------------------------------------------------------------------------

def flash(build_dir, build_name, bios_flash_offset):
    from litex.build.lattice.programmer import IceStormProgrammer
    prog = IceStormProgrammer()
    prog.flash(bios_flash_offset, f"{build_dir}/software/bios/bios.bin")
    prog.flash(0x00010000,        f"{build_dir}/gateware/{build_name}.bin")

# Build --------------------------------------------------------------------------------------------

def main():
    from litex.build.parser import LiteXArgumentParser
    parser = LiteXArgumentParser(platform=upduino_v3.Platform, description="LiteX SoC on Upduino_v3")
    parser.add_target_argument("--flash",             action="store_true",      help="Flash Bitstream")
    parser.add_target_argument("--sys-clk-freq",      default=12e6, type=float, help="System clock frequency.")
    parser.add_target_argument("--bios-flash-offset", default="0x20000",        help="BIOS offset in SPI Flash.")
    args = parser.parse_args()

    soc = BaseSoC(
        bios_flash_offset = int(args.bios_flash_offset, 0),
        sys_clk_freq      = args.sys_clk_freq,
        **parser.soc_argdict
    )
    builder = Builder(soc, **parser.builder_argdict)
    if args.build:
        builder.build(**parser.toolchain_argdict)

    if args.flash:
        flash(builder.output_dir, soc.build_name, int(args.bios_flash_offset, 0))

if __name__ == "__main__":
    main()
