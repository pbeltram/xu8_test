## XU8+ST1 10Gb Ethernet test

Demo for Enclustra XU8+ST1 with AMD FMCXM105 board to demonstrate reliable data transfer at wire speed over 10Gb Ethernet link on AMD ZynqUS+ system.
On XU8+ST1 only LX v6.6.40 is running and it continuously stream out data at 9.5Gbits/sec. In the remaining data bandwidth of the 10Gb Etherent link other internet protocols (e.g. SSH, HTTP) can be used. 

In FPGA 32bit data is sampled at 312.5Mhz and than streamed as AXI data stream out via DMA to 10Gb Ethernet. 
Sampled data can be selected as continuous 32bit counter or 32 DIO routed from FMCXM105 board (22 differential LVDS) and ST1 ANIOS IO0 connector (10 single ended). Sampled data is decimated by 1.1 to produce continuous stream at 284.1 MSPS (1.136G bytes/sec).

Data on Ethernet is transferred via UDP protocol to PC . Since UDP packets can be (and will be) lost, a capturing SW implements requests to resend missing data blocks. With this resend request feature the data link becomes reliable source to stream data from FPGA to PC. To underline is that CPU load during data transfer is negligible. It is below 3% (CPU0=4%, CPU1=1%), data transfer is done almost completely by ZynqUS+ HW. This basically leaves all CPU power to do some other tasks while data is transferred out.

**Directories:**

- `./pics/`. Pictures with references from this README.
- `./bin/`. Prebuilt and staged PC binary files to control and capture data blocks for Linux and Windows (description in [README.md](./bin/README.md)).
- `./sd_disk/`. Files for XU8 board. (description in [README.md](./lnx/README.md)).
- `./python/`. Python script to analyze captured data (description in [README.md](./python/README.md)).

#### XU8+ST1 Board configuration

You will have to create SD card to boot your XU8+ST1 board with it. Files and instructions are located in `./sd_disk/README.md` file. 
Current IP address/netmask is set in `/etc/network/interface` file. For XU8 it is set to `169.254.50.80/24`. 

#### PC configuration

For 10Gb Etherent you need to have working 10G network connection. For example PC network card card `Intel 82599ES 10-Gigabit SFI/SFP+` Ethernet NIC and some 10Gb Etherent capable network switch for example `MicroTik CRS305-1G-4S+`.

PC NIC must be configured to use jumbo frames with MTU=8192 (or larger). NIC IP address must be set on the same IP network address/netmask as XU8, for example `169.254.50.23/24`.

Set IP address/netmask of PC NIC to `169.254.50.23/24` and MTU to at least 8192.

Next you have to change Ubuntu configuration to boost UDP performance with changes in system file `sudo /etc/sysctl.cfg`. Append this lines at the end of file:

```
# UDP performance settings
net.core.rmem_max=2147483647
net.core.rmem_default=2147483647
net.core.netdev_max_backlog=20000
kernel.shmmni=32768
```

After all this changes it is good to do a reboot of PC and verify all settings are OK with `ping 169.254.50.80` xu8 connection and UDP performance settings with:

```
sudo sysctl net.core.rmem_default # 2147483647
sudo sysctl net.core.wmem_default # 2147483647
sudo sysctl net.core.netdev_max_backlog # 20000
```

PC disks must be capable to write at least of 1.14G bytes/sec data in order to save captured data to files.
For example disks on HP workstation Z420 are not so fast (cca 150Mbytes/sec). With HP Z420 and 32G byte of memory only 5 consecutive 1G byte data files (limiting with command line option --files=5) can be successfully saved. More than this does not go on HP Z420.
System becomes too busy with filesystem cache flushing writes and it starts to fail UDP data capturing.

**Mapping of DIO pins**

Pins are on FMCXM105 J1 and J20 connectors and XU8+ST1 ANIOS IO_0 connector.
32 DIO are 10x 1V8 Single ended and 22x differential 100Ohm terminated LVDS.

**NOTE: Consult XU8 and FPMXM105 schematics before connecting your signals to connectors!**
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
