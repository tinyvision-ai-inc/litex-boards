#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2022 FAYE Joseph <joseph-wagane.faye@insa-rennes.fr>
# Copyright (c) 2023 Ryohei Niwase <niwase@lila.cs.tsukuba.ac.jp>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxUSPPlatform, VivadoProgrammer


# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk125", 0,
        Subsignal("p", Pins("G21"), IOStandard("LVDS_25")),
        Subsignal("n", Pins("F21"), IOStandard("LVDS_25")),
    ),
    ("clk300", 0,
        Subsignal("p", Pins("AL8"), IOStandard("DIFF_SSTL12_DCI")),
        Subsignal("n", Pins("AL7"), IOStandard("DIFF_SSTL12_DCI")),
    ),
    ("cpu_reset", 0, Pins("AM13"), IOStandard("LVCMOS33")),

    # Leds
    ("user_led", 0, Pins("AG14"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("AF13"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("AE13"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("AJ14"), IOStandard("LVCMOS33")),
    ("user_led", 4, Pins("AJ15"), IOStandard("LVCMOS33")),
    ("user_led", 5, Pins("AH13"), IOStandard("LVCMOS33")),
    ("user_led", 6, Pins("AH14"), IOStandard("LVCMOS33")),
    ("user_led", 7, Pins("AL12"), IOStandard("LVCMOS33")),

    # Buttons
    ("user_btn", 0, Pins("AG15"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("AE14"), IOStandard("LVCMOS33")),
    ("user_btn", 2, Pins("AF15"), IOStandard("LVCMOS33")),
    ("user_btn", 3, Pins("AE15"), IOStandard("LVCMOS33")),
    ("user_btn", 3, Pins("AG13"), IOStandard("LVCMOS33")),

    # Switches
    ("user_dip", 0, Pins("AN14"), IOStandard("LVCMOS33")),
    ("user_dip", 1, Pins("AP14"), IOStandard("LVCMOS33")),
    ("user_dip", 2, Pins("AM14"), IOStandard("LVCMOS33")),
    ("user_dip", 3, Pins("AN13"), IOStandard("LVCMOS33")),
    ("user_dip", 4, Pins("AN12"), IOStandard("LVCMOS33")),
    ("user_dip", 5, Pins("AP12"), IOStandard("LVCMOS33")),
    ("user_dip", 6, Pins("AL13"), IOStandard("LVCMOS33")),
    ("user_dip", 7, Pins("AK13"), IOStandard("LVCMOS33")),

    # Serial
    ("serial", 0,
        Subsignal("cts", Pins("E12")),
        Subsignal("rts", Pins("D12")),
        Subsignal("rx",  Pins("E13")),
        Subsignal("tx",  Pins("F13")),
        IOStandard("LVCMOS33")
    ),

    # I2C
    ("i2c", 0,
        Subsignal("sda", Pins("J11")),
        Subsignal("scl", Pins("J10")),
        IOStandard("LVCMOS33")
    ),

    # DDR4 SDRAM
    ("ddram", 0,
        Subsignal("a",       Pins(
            "AM8  AM9  AP8  AN8  AK10 AJ10 AP9  AN9",
            "AP10 AP11 AM10 AL10 AM11 AL11"),
            IOStandard("SSTL12_DCI")),
        Subsignal("ba",      Pins("AK12 AJ12"), IOStandard("SSTL12_DCI")),
        Subsignal("bg",      Pins("AK7"), IOStandard("SSTL12_DCI")),
        Subsignal("ras_n",   Pins("AJ9"), IOStandard("SSTL12_DCI")), # A16
        Subsignal("cas_n",   Pins("AL5"), IOStandard("SSTL12_DCI")), # A15
        Subsignal("we_n",    Pins("AJ7"), IOStandard("SSTL12_DCI")), # A14
        Subsignal("cs_n",    Pins("AP2"), IOStandard("SSTL12_DCI")),
        Subsignal("act_n",   Pins("AK8"), IOStandard("SSTL12_DCI")),
        #Subsignal("par",     Pins("AP1"), IOStandard("SSTL12_DCI")),
        Subsignal("dm",      Pins("AL6 AN2"),
            IOStandard("POD12_DCI")),
        Subsignal("dq",      Pins(
                "AK4 AK5 AN4 AM4 AP4 AP5 AM5 AM6",
                "AK2 AK3 AL1 AK1 AN1 AM1 AP3 AN3"),
            IOStandard("POD12_DCI"),
            Misc("PRE_EMPHASIS=RDRV_240"),
            Misc("EQUALIZATION=EQ_LEVEL2")),
        Subsignal("dqs_p",   Pins("AN6 AL3"),
            IOStandard("DIFF_POD12"),
            Misc("PRE_EMPHASIS=RDRV_240"),
            Misc("EQUALIZATION=EQ_LEVEL2")),
        Subsignal("dqs_n",   Pins("AP6 AL2"),
            IOStandard("DIFF_POD12"),
            Misc("PRE_EMPHASIS=RDRV_240"),
            Misc("EQUALIZATION=EQ_LEVEL2")),
        Subsignal("clk_p",   Pins("AN7"), IOStandard("DIFF_SSTL12")),
        Subsignal("clk_n",   Pins("AP7"), IOStandard("DIFF_SSTL12")),
        Subsignal("cke",     Pins("AM3"), IOStandard("SSTL12_DCI")),
        Subsignal("odt",     Pins("AK9"), IOStandard("SSTL12_DCI")),
        Subsignal("reset_n", Pins("AH9"), IOStandard("LVCMOS18")),
        Misc("SLEW=FAST"),
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("j55", "A20 B20 A22 A21 B21 C21 C22 D21"),
    ("j87", "D20 E20 D22 E22 F20 G20 J20 J19"),
    ("FMC_HPC0", {
        "CLK0_M2C_N"      : "AA6",
        "CLK0_M2C_P"      : "AA7",
        "CLK1_M2C_N"      : "R8",
        "CLK1_M2C_P"      : "T8",
        "DP0_C2M_N"       : "G3",
        "DP0_C2M_P"       : "G4",
        "DP0_M2C_N"       : "H1",
        "DP0_M2C_P"       : "H2",
        "DP1_C2M_N"       : "H5",
        "DP1_C2M_P"       : "H6",
        "DP1_M2C_N"       : "J3",
        "DP1_M2C_P"       : "J4",
        "DP2_C2M_N"       : "F5",
        "DP2_C2M_P"       : "F6",
        "DP2_M2C_N"       : "F1",
        "DP2_M2C_P"       : "F2",
        "DP3_C2M_N"       : "K5",
        "DP3_C2M_P"       : "K6",
        "DP3_M2C_N"       : "K1",
        "DP3_M2C_P"       : "K2",
        "DP4_C2M_N"       : "M5",
        "DP4_C2M_P"       : "M6",
        "DP4_M2C_N"       : "L3",
        "DP4_M2C_P"       : "L4",
        "DP5_C2M_N"       : "P5",
        "DP5_C2M_P"       : "P6",
        "DP5_M2C_N"       : "P1",
        "DP5_M2C_P"       : "P2",
        "DP6_C2M_N"       : "R3",
        "DP6_C2M_P"       : "R4",
        "DP6_M2C_N"       : "T1",
        "DP6_M2C_P"       : "T2",
        "DP7_C2M_N"       : "N3",
        "DP7_C2M_P"       : "N4",
        "DP7_M2C_N"       : "M1",
        "DP7_M2C_P"       : "M2",
        "GBTCLK0_M2C_C_N" : "G7",
        "GBTCLK0_M2C_C_P" : "G8",
        "GBTCLK1_M2C_C_N" : "L7",
        "GBTCLK1_M2C_C_P" : "L8",
        "LA00_CC_N"       : "Y3",
        "LA00_CC_P"       : "Y4",
        "LA01_CC_N"       : "AC4",
        "LA01_CC_P"       : "AB4",
        "LA02_N"          : "V1",
        "LA02_P"          : "V2",
        "LA03_N"          : "Y1",
        "LA03_P"          : "Y2",
        "LA04_N"          : "AA1",
        "LA04_P"          : "AA2",
        "LA05_N"          : "AC3",
        "LA05_P"          : "AB3",
        "LA06_N"          : "AC1",
        "LA06_P"          : "AC2",
        "LA07_N"          : "U4",
        "LA07_P"          : "U5",
        "LA08_N"          : "V3",
        "LA08_P"          : "V4",
        "LA09_N"          : "W1",
        "LA09_P"          : "W2",
        "LA10_N"          : "W4",
        "LA10_P"          : "W5",
        "LA11_N"          : "AB5",
        "LA11_P"          : "AB6",
        "LA12_N"          : "W6",
        "LA12_P"          : "W7",
        "LA13_N"          : "AC8",
        "LA13_P"          : "AB8",
        "LA14_N"          : "AC6",
        "LA14_P"          : "AC7",
        "LA15_N"          : "Y9",
        "LA15_P"          : "Y10",
        "LA16_N"          : "AA12",
        "LA16_P"          : "Y12",
        "LA17_CC_N"       : "N11",
        "LA17_CC_P"       : "P11",
        "LA18_CC_N"       : "N8",
        "LA18_CC_P"       : "N9",
        "LA19_N"          : "K13",
        "LA19_P"          : "L13",
        "LA20_N"          : "M13",
        "LA20_P"          : "N13",
        "LA21_N"          : "N12",
        "LA21_P"          : "P12",
        "LA22_N"          : "M14",
        "LA22_P"          : "M15",
        "LA23_N"          : "K16",
        "LA23_P"          : "L16",
        "LA24_N"          : "K12",
        "LA24_P"          : "L12",
        "LA25_N"          : "L11",
        "LA25_P"          : "M11",
        "LA26_N"          : "K15",
        "LA26_P"          : "L15",
        "LA27_N"          : "L10",
        "LA27_P"          : "M10",
        "LA28_N"          : "T6",
        "LA28_P"          : "T7",
        "LA29_N"          : "U8",
        "LA29_P"          : "U9",
        "LA30_N"          : "U6",
        "LA30_P"          : "V6",
        "LA31_N"          : "V7",
        "LA31_P"          : "V8",
        "LA32_N"          : "T11",
        "LA32_P"          : "U11",
        "LA33_N"          : "V11",
        "LA33_P"          : "V12",        
    }),
    ("FMC_HPC1", {
        "CLK0_M2C_N"      : "AF7",
        "CLK0_M2C_P"      : "AE7",
        "CLK1_M2C_N"      : "P9",
        "CLK1_M2C_P"      : "P10",
        "DP0_C2M_N"       : "F30",
        "DP0_C2M_P"       : "F29",
        "DP0_M2C_N"       : "E32",
        "DP0_M2C_P"       : "E31",
        "DP1_C2M_N"       : "D30",
        "DP1_C2M_P"       : "D29",
        "DP1_M2C_N"       : "D34",
        "DP1_M2C_P"       : "D33",
        "DP2_C2M_N"       : "B30",
        "DP2_C2M_P"       : "B29",
        "DP2_M2C_N"       : "C32",
        "DP2_M2C_P"       : "C31",
        "DP3_C2M_N"       : "A32",
        "DP3_C2M_P"       : "A31",
        "DP3_M2C_N"       : "B34",
        "DP3_M2C_P"       : "B33",
        "DP4_C2M_N"       : "K30",
        "DP4_C2M_P"       : "K29",
        "DP4_M2C_N"       : "L32",
        "DP4_M2C_P"       : "L31",
        "DP5_C2M_N"       : "J32",
        "DP5_C2M_P"       : "J31",
        "DP5_M2C_N"       : "K34",
        "DP5_M2C_P"       : "K33",
        "DP6_C2M_N"       : "H30",
        "DP6_C2M_P"       : "H29",
        "DP6_M2C_N"       : "H34",
        "DP6_M2C_P"       : "H33",
        "DP7_C2M_N"       : "G32",
        "DP7_C2M_P"       : "G31",
        "DP7_M2C_N"       : "F34",
        "DP7_M2C_P"       : "F33",
        "GBTCLK0_M2C_C_N" : "G28",
        "GBTCLK0_M2C_C_P" : "G27",
        "GBTCLK1_M2C_C_N" : "E28",
        "GBTCLK1_M2C_C_P" : "E27",
        "LA00_CC_N"       : "AF5",
        "LA00_CC_P"       : "AE5",
        "LA01_CC_N"       : "AJ5",
        "LA01_CC_P"       : "AJ6",
        "LA02_N"          : "AD1",
        "LA02_P"          : "AD2",
        "LA03_N"          : "AJ1",
        "LA03_P"          : "AH1",
        "LA04_N"          : "AF1",
        "LA04_P"          : "AF2",
        "LA05_N"          : "AH3",
        "LA05_P"          : "AG3",
        "LA06_N"          : "AJ2",
        "LA06_P"          : "AH2",
        "LA07_N"          : "AE4",
        "LA07_P"          : "AD4",
        "LA08_N"          : "AF3",
        "LA08_P"          : "AE3",
        "LA09_N"          : "AE1",
        "LA09_P"          : "AE2",
        "LA10_N"          : "AJ4",
        "LA10_P"          : "AH4",
        "LA11_N"          : "AF8",
        "LA11_P"          : "AE8",
        "LA12_N"          : "AD6",
        "LA12_P"          : "AD7",
        "LA13_N"          : "AH8",
        "LA13_P"          : "AG8",
        "LA14_N"          : "AH6",
        "LA14_P"          : "AH7",
        "LA15_N"          : "AE9",
        "LA15_P"          : "AD10",
        "LA16_N"          : "AG9",
        "LA16_P"          : "AG10",
        "LA17_CC_N"       : "AA5",
        "LA17_CC_P"       : "Y5",
        "LA18_CC_N"       : "Y7",
        "LA18_CC_P"       : "Y8",
        "LA19_N"          : "AA10",
        "LA19_P"          : "AA11",
        "LA20_N"          : "AB10",
        "LA20_P"          : "AB11",
        "LA21_N"          : "AC11",
        "LA21_P"          : "AC12",
        "LA22_N"          : "AG11",
        "LA22_P"          : "AF11",
        "LA23_N"          : "AF12",
        "LA23_P"          : "AE12",
        "LA24_N"          : "AH11",
        "LA24_P"          : "AH12",
        "LA25_N"          : "AF10",
        "LA25_P"          : "AE10",
        "LA26_N"          : "R12",
        "LA26_P"          : "T12",
        "LA27_N"          : "T10",
        "LA27_P"          : "U10",
        "LA28_N"          : "R13",
        "LA28_P"          : "T13",
        "LA29_N"          : "W11",
        "LA29_P"          : "W12",
    }),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxUSPPlatform):
    default_clk_name   = "clk125"
    default_clk_period = 1e9/125e6

    def __init__(self, toolchain="vivado"):
        XilinxUSPPlatform.__init__(self, "xczu9eg-ffvb1156-2-i", _io, _connectors, toolchain=toolchain)

    def create_programmer(self):
        return VivadoProgrammer()

    def do_finalize(self, fragment):
        XilinxUSPPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk125", loose=True), 1e9/125e6)
        self.add_period_constraint(self.lookup_request("clk300", loose=True), 1e9/300e6)
        self.add_platform_command("set_property INTERNAL_VREF 0.84 [get_iobanks 64]")
        self.add_platform_command("set_property INTERNAL_VREF 0.84 [get_iobanks 65]")
