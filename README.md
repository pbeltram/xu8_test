## XU8+ST1 tests

- xu8+ST1 10Gb Etherent wire speed test [xu8_rec README](./README_rec.md).
- xu8+ST1 RaspberryPi HQ (IMX477) camera test [xu8_cam README](./README_cam.md).

**Directories:**

- `./pics/`. Pictures with references from this README.
- `./bin/`. Prebuilt and staged PC binary files to control and capture data blocks for Linux and Windows (description in [README.md](./bin/README.md)).
- `./sd_disk/`. Files for XU8 board. (description in [README.md](./sd_disk/README.md)).
- `./python/`. Python script to analyze captured data (description in [README.md](./python/README.md)).
- `./sw/`. PC user space sw (description in [README.md](./sw/README.md))..

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
