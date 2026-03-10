## PicoZED SDR++ test

Demo for PicoZED board PicoZED SDR [ADRV9364-Z7020](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/adrv9364-z7020.html) mounted on carrier [ADRV1CRR-BOB](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/ADRV1CRR-BOB.html).

FPGA design is custom build with constrains timing catch for 182Mhz AD9364 data clock (246Mhz would be required max for AD9364 chip). This then results in max 182/4=45.5 MSPS data rate. 12bit IQ data is packed to 64bit for DMA transfer to PS DDR. On Zynq PS Linux v6.6.40 is running with user space control application. From there it is then streamed to SDR++ via Zynq Z7020 GEM 1G Etherent controller using UDP protocol. UDP protocol utilizes GEM jumbo frames. This means that also other network equipment in path (switches, PC NIC) must support at least 4K jumbo frames.

SDR++ (tag 1.0.4) is running on LX Ubuntu 20.04 PC with NVIDIA Quadro K4000. I have build custom source module to handle protocol data. This source module unpacks 12bit IQ data and pass them to SDR++ for further calcs and display. It handles also requests to resend lost UDP packets. Result is reliable 1Gbps Ethernet wire speed continuous data transfer.

With this setup I can continuously stream 12bit IQ data over GEM 1Gbps Ethernet link at 40 MSPS with no(!) data lost. Resulting Ethernet link BW 40*3*8=960Mbps is very close to theoretical 1Gbps wire speed. 

