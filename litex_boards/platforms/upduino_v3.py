# litex-boards platform file
from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform
from litex.build.lattice.programmer import IceStormProgrammer

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # CLK / RST (short solder bridge labelled "OSC" near usb, or connect  gpio_20 and 12MHz via breadboard/wire etc.)
    ("clk12", 0, Pins("20"), IOStandard("LVCMOS33")),

    # RGB LED (inverted)
    ("user_led_n", 0, Pins("41"), IOStandard("LVCMOS33")),
    ("user_led_n", 1, Pins("39"), IOStandard("LVCMOS33")),
    ("user_led_n", 2, Pins("40"), IOStandard("LVCMOS33")),
    #Color Specific alias
    ("user_ledr_n", 0, Pins("41"), IOStandard("LVCMOS33")),
    ("user_ledg_n", 0, Pins("39"), IOStandard("LVCMOS33")),
    ("user_ledb_n", 0, Pins("40"), IOStandard("LVCMOS33")),
    
     #Serial (FT232H UART pins shared with flash so use external UART to USB on pins 2 and 3)   #FIXME
    ("serial", 0,
        Subsignal("tx", Pins("3")),
        Subsignal("rx", Pins("2")),
        IOStandard("LVCMOS33")
    ),
    # SPIFlash
    ("spiflash", 0,
        Subsignal("cs_n", Pins("16"), IOStandard("LVCMOS33")),
        Subsignal("clk",  Pins("15"), IOStandard("LVCMOS33")),
        Subsignal("mosi", Pins("17"), IOStandard("LVCMOS33")),
        Subsignal("miso", Pins("14"), IOStandard("LVCMOS33")),
    )
 ]

# Connectors ----------------------------------------------------------------------------------------

_connectors = [

    # J2 (left side when usb pointed up)
    ("J2", "23 25 26 27 32 31 37 34 43 36 42 38 28"),
    
    # J3 (right side when usb pointed up)
    ("J3", "12 21 13 19 11  9  6 44  4  48 45 47 46 ")
]

class Platform(LatticePlatform):
    default_clk_name   = "clk12"
    default_clk_period = 1e9/12e6

    def __init__(self, toolchain="icestorm"):
        LatticePlatform.__init__(self, "ice40-up5k-sg48", _io, _connectors, toolchain=toolchain)

    def create_programmer(self):
        return IceStormProgrammer()

    def do_finalize(self, fragment):
        LatticePlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk12", loose=True), 1e9/12e6)
