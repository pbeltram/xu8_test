## XU8+ST1 RaspberryPi HQ (IMX477) camera test

Demo for Enclustra XU8+ST1 with RaspberryPI HQ camera. Camera has Sony IMX477 sensor with 2 MIPI CSI-2 lanes. According to product data brief flyer it is capable to create 40 FPS (frames per second) for its full ROI (max resolution) 4056x3040 with 12bpp (bits per pixel).
Focus of this demo was to investigate reliable data capture and transfer at sensor maximum FPS rate. 

The maximum rate of 36.130 FPS was achieved with this demo. 
Amount of data created at this FPS rates requires at least 5.4Gbps of data bandwidth, so for this demo it is mandatory to use 10Gb Ethernet connection to PC.

Images are transferred via Ethernet UDP protocol to PC. Since UDP packets can be (and will be) lost, a capturing SW implements requests to resend missing data blocks. With this resend request feature the data link becomes reliable source to stream data from FPGA to PC. To underline is that CPU load during data transfer is negligible. It is below 3% (CPU0=4%, CPU1=1%), data transfer is done almost completely by ZynqUS+ HW. This basically leaves all CPU power to do some other tasks while data is transferred out.

NOTE: FMCXM105 (on setup picture) is not needed for xu8_cam test.
