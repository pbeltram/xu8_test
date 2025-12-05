## XU8+ST1 10Gb Ethernet test

Demo for Enclustra XU8+ST1 with AMD FMCXM105 board to demonstrate reliable data transfer at wire speed over 10Gb Ethernet link on AMD ZynqUS+ system.
On XU8+ST1 only LX v6.6.40 is running and it continuously stream out data at 9.5Gbits/sec. In the remaining data bandwidth of the 10Gb Etherent link other internet protocols (e.g. SSH, HTTP) can be used. 

In FPGA 32bit data is sampled at 312.5Mhz and than streamed as AXI data stream out via DMA to 10Gb Ethernet. 
Sampled data can be selected as continuous 32bit counter or 32 DIO routed from FMCXM105 board (22 differential LVDS) and ST1 ANIOS IO0 connector (10 single ended). Sampled data is decimated by 1.1 to produce continuous stream at 284.1 MSPS (1.136G bytes/sec).

Data on Ethernet is transferred via UDP protocol to PC . Since UDP packets can be (and will be) lost, a capturing SW implements requests to resend missing data blocks. With this resend request feature the data link becomes reliable source to stream data from FPGA to PC. To underline is that CPU load during data transfer is negligible. It is below 3% (CPU0=4%, CPU1=1%), data transfer is done almost completely by ZynqUS+ HW. This basically leaves all CPU power to do some other tasks while data is transferred out.

**Mapping of DIO pins**

Pins are on FMCXM105 J1 and J20 connectors and XU8+ST1 ANIOS IO_0 connector.
32 DIO are 10x 1V8 Single ended and 22x differential 100Ohm terminated LVDS.

**NOTE: Consult XU8 and FMCXM105 schematics before connecting your signals to connectors!**
**Wrong connections or wrong voltages can permanently damage your HW!**

```
data( 0) <= FMC_LA16   ;-- NOTE: FMCXM105 J1  26-28  LVDS 100Ohm terminated diff_pair
data( 1) <= FMC_LA17_CC;-- NOTE: FMCXM105 J1  30-32  LVDS 100Ohm terminated diff_pair
data( 2) <= FMC_LA19   ;-- NOTE: FMCXM105 J1  38-40  LVDS 100Ohm terminated diff_pair
data( 3) <= FMC_LA20   ;-- NOTE: FMCXM105 J20 1-3    LVDS 100Ohm terminated diff_pair
data( 4) <= FMC_LA21   ;-- NOTE: FMCXM105 J20 5-7    LVDS 100Ohm terminated diff_pair
data( 5) <= FMC_LA22   ;-- NOTE: FMCXM105 J20 9-11   LVDS 100Ohm terminated diff_pair
data( 6) <= IO0_D23_N  ;-- NOTE: ANIOS IO_0   6      LVCMOS18 Single ended
data( 7) <= IO0_D21_N  ;-- NOTE: ANIOS IO_0   8      LVCMOS18 Single ended
data( 8) <= IO0_D19_N  ;-- NOTE: ANIOS IO_0   10     LVCMOS18 Single ended
data( 9) <= IO0_D17_N  ;-- NOTE: ANIOS IO_0   12     LVCMOS18 Single ended
data(10) <= IO0_D15_N  ;-- NOTE: ANIOS IO_0   16     LVCMOS18 Single ended
data(11) <= IO0_D13_N  ;-- NOTE: ANIOS IO_0   18     LVCMOS18 Single ended
data(12) <= IO0_D11_N  ;-- NOTE: ANIOS IO_0   20     LVCMOS18 Single ended
data(13) <= IO0_D9_N   ;-- NOTE: ANIOS IO_0   22     LVCMOS18 Single ended
data(14) <= IO0_D7_N   ;-- NOTE: ANIOS IO_0   26     LVCMOS18 Single ended
data(15) <= IO0_D5_N   ;-- NOTE: ANIOS IO_0   28     LVCMOS18 Single ended
data(16) <= FMC_LA00_CC;-- NOTE: FMCXM105 J1  1-3    LVDS 100Ohm terminated diff_pair
data(17) <= FMC_LA01_CC;-- NOTE: FMCXM105 J1  5-7    LVDS 100Ohm terminated diff_pair
data(18) <= FMC_LA02   ;-- NOTE: FMCXM105 J1  9-11   LVDS 100Ohm terminated diff_pair
data(19) <= FMC_LA03   ;-- NOTE: FMCXM105 J1  13-15  LVDS 100Ohm terminated diff_pair
data(20) <= FMC_LA04   ;-- NOTE: FMCXM105 J1  17-19  LVDS 100Ohm terminated diff_pair
data(21) <= FMC_LA05   ;-- NOTE: FMCXM105 J1  21-23  LVDS 100Ohm terminated diff_pair
data(22) <= FMC_LA06   ;-- NOTE: FMCXM105 J1  25-27  LVDS 100Ohm terminated diff_pair
data(23) <= FMC_LA07   ;-- NOTE: FMCXM105 J1  29-31  LVDS 100Ohm terminated diff_pair
data(24) <= FMC_LA08   ;-- NOTE: FMCXM105 J1  33-35  LVDS 100Ohm terminated diff_pair
data(25) <= FMC_LA09   ;-- NOTE: FMCXM105 J1  37-39  LVDS 100Ohm terminated diff_pair
data(26) <= FMC_LA10   ;-- NOTE: FMCXM105 J1  2-4    LVDS 100Ohm terminated diff_pair
data(27) <= FMC_LA11   ;-- NOTE: FMCXM105 J1  6-8    LVDS 100Ohm terminated diff_pair
data(28) <= FMC_LA12   ;-- NOTE: FMCXM105 J1  10-12  LVDS 100Ohm terminated diff_pair
data(29) <= FMC_LA13   ;-- NOTE: FMCXM105 J1  14-16  LVDS 100Ohm terminated diff_pair
data(30) <= FMC_LA14   ;-- NOTE: FMCXM105 J1  18-20  LVDS 100Ohm terminated diff_pair
data(31) <= FMC_LA15   ;-- NOTE: FMCXM105 J1  22-24  LVDS 100Ohm terminated diff_pair
```
