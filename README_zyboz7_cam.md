## ZyboZ7-20 RaspberryPi HQ (Sony IMX477) camera test

Demo for Digilent ZyboZ7-20 with RaspberryPI HQ camera. Camera has Sony IMX477 sensor with 2 MIPI CSI-2 lanes. Focus of this demo was to investigate maximum FPS rate for this camera on ZynqZ7. Test was limited to full ROI mode 4056x3040 with 12bpp, the maximum image information that sensor can provide.

The maximum rate of 7.684 FPS was achieved with this demo. 
Amount of data created at this FPS rates generates bandwidth of 142Mbytes/sec. This is too much to stream over Zynq-Z7 1Gbps GEM Ethernet, so in fpga is implemented fractional decimation on images FPS. With decimation=1.2 a sustainable data bandwidth of cca 950Mbps is generated.

Images are transferred via Ethernet UDP protocol to PC. Since UDP packets can be (and will be) lost, a capturing SW implements requests to resend missing data blocks. With this resend request feature the data link becomes reliable source to stream data from FPGA to PC. CPU load on Zynq-Z7 during data transfer is cca 24% (CPU0=4%, CPU1=40%). CPU load is low and leavse some CPU power to do some other tasks while data is transferred out. Note that Zynq-Z7 GEM 1Gbps Etherent controler is used, so no additional resources in FPGA are needed for Etherent transfer.
