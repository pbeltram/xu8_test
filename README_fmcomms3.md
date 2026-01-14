## XU8+ST1 Analog FMCOMMS3 test

Demo for Enclustra XU8+ST1 with Analog FMCOMMS3 board with AD9361 chip.
In XU8+ST1 FMCOMMS3 FPGA [xu8_fmcomms3 block design](./pics/xu8_fmcomms3/xu8_fmcomms3_fpga_rev1084.png) there are 3 independent data streams. All 3 data streams are originating from AD9361 12bit IQ sampled data.

- Stream 0 is raw RX1/RX2 12bit IQ data stream. Resulting 48bits stream data sample is packed into 64bit DMA stream (4x 48bit to 3x 64bit).

- Stream 1 is RX1 64k FFT IQ points continous pipline data stream. Resulting 58bits stream data sample is sign extended to 64bit DMA stream (1x 58bits to 1x 64bits).

- Stream 2 is RX2 2k FFT IQ points continous pipline data stream. Resulting 48bits stream data sample is packed into 64bit DMA stream (4x 48bit to 3x 64bit)

For each of data streams there are Python scripts in `./python` directory to visualize captured data.

Total stream data bandwidth from FPGA is: AD9361_MSPS*(6+8+6) bytes/sec. The maximum bandwidth of 9.830Gbits/sec was achieved with this demo, when data from all 3 data streams are captured at AD9361 maximum 61.44MSPS sampling frequency. 

Stream selection capturing is configurable via stream bit mask setting in PC SW, any streaming combination is configurable.

You will need Analog IIO oscilloscope application to configure AD9361. Instructions are available [here](https://wiki.analog.com/resources/tools-software/linux-software/iio_oscilloscope). Analog IIO oscilloscope for xu8_fmcomms3 is used only to configure AD9361 settings. There is no IIO data acquisition support on xu8_fmcomms3, data acquisition is done via proprietary NPAPI protocol interface.

NOTE: A patch of 4 wires is needed because there are missing SPI link connections from XU8+ST1 FMC connector to Analog FMCOMMS3 board. 
Missing SPI lines (DI, DO, CS and CLK) need to be routed via wires to XU8+ST1 ANIOS IO0 connector.
To make this demo work on Enclustra XU8+ST1, you will have to solder this wires on your FMCOMMS3 board.
In `./pics` directory there are pictures how I did this patch on my FMCOMMS3 board to solder this 4 wires and rout them to Enclustra ST1 ANIOS IO0 connector. 
Consult schematic design document of Analog FMCOMMS3 board to locate soldering points on board and Enclustra ST1 schematics to locate ANIOS IO0 connector and pins.
Connection on XU8+ST1 ANIOS IO0 connector are:

```
DI  to IO0_12 # SPI_MOSI
DO  to IO0_10 # SPI_MISO
CLK to IO0_08 # SPI_CLK
CS  to IO0_06 # SPI_CSN
```

**By doing this soldering wrong, you can permanently damage your FMCOMMS3 board. Doing this patch is on your complete responsibility.**


