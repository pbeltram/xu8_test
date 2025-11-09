## Program options

**Program options for `papi_test`**

```
"-d, --device n              Device IP address. (Mandatory, 169.254.50.28)."
"-h, --host n                Host ip (Mandatory)."
"-c, --count n               Number of images to acquire, 0 -> endless loop. (Optional, default=0)."
"-p, --print                 Print console messages. (Optional, default is off)."
"-v, --verbose n             Dump n atoms of data content. (Optional, default is off)."
"-m, --decimate n            Data decimation. (Optional, 0=leave HW default min=1.0 max=16.0)."
"-l, --length n              Number of data atoms (Optional, default=250006, min=2054)."
"-t, --mtu                   MTU (Optional, 0=leave HW default))."
"-x, --mux n                 Data mux selector (Optional, 0=default) 0-Decimated counter, 3-DIO).
```

- On Ubuntu 20.04 the binary application to use is **./lnx64/papi_test** (md5sum: 71b7398c3ff0cbe7940a9f360ce72b97)

- On Windows 11 the binary application to use is **./win64/papi_test_64bit.exe** (md5sum: 073c1466a4d9593fab9f7aaab63e75c3)

## Examples:

Capture 10 data buffers with 2056 data atoms from decimated counter and then exit. Decimation is 16.0.

Print data buffer info and dump first 5 data atoms from each captured data buffer.

```
./lnx64/papi_test --device=169.254.50.80 --host=169.254.50.23 --decimate=16.0 --count=10 --length=2056 --mux=0 --print --verbose=5
```

Continuous capture of data buffers with 2000000 data atoms from DIO data. Decimation is 1.1 (network bw cca 9.5Gbits/sec). 

This is minimum decimation without network saturation and will stream payload data at 1.136G bytes/sec.
Going over network bandwidth limit, the fatal error messages `Data chn=0 Overflow.` will start to appear on device console output.

For missing UDP packets you will see on console output messages `send_resend:` requests and `on_packet_resend:` responses when missed UDP packet was received. 

To exit press `<CTRL>-C`.

```
./lnx64/papi_test --device=169.254.50.80 --host=169.254.50.23 --decimate=1.1 --count=0 --length=2000000 --mux=3
```

**Program options for `papi_recorder`**

```
"-d, --device n              Device IP address. (Mandatory, 169.254.50.28)."
"-h, --host n                Host ip (Mandatory)."
"-c, --count n               Number of images to acquire, 0 -> endless loop. (Optional, default=0)."
"-p, --print                 Print console messages. (Optional, default is off)."
"-v, --verbose n             Dump n atoms of data content. (Optional, default is off)."
"-m, --decimate n            Data decimation. (Optional, 0=leave HW default min=1.0 max=16.0)."
"-l, --length n              Number of data atoms (Optional, default=250006, min=2054))."
"-t, --mtu                   MTU (Optional, 0=leave HW default))."
"-w, --wait                  Max number msec to wait for all packets (Optional, default=300 min=100))."
"-r, --resend                Max number resend retries for missing packets (Optional, default=2 min=1))."
"-n, --files                 Max number of 1Gbyte data files to write (Optional, default=5 min=1))."
"-x, --mux n                 Data mux selector (Optional, 0=default) 0-Decimated counter, 3-DIO).
"-o, --out dir               Write results to directory (<dir>/samples_vX.dat). (Optional, default is false. X=raw format version)."
```

- On Ubuntu 20.04 the binary application to use is **./lnx64/papi_recorder** (md5sum: f34b41f93cfb6dccbab6c995881b6863)

- On Windows 11 the binary application to use is **./win64/papi_recorder_64bit.exe** (md5sum: c52fe012d20c5b976f49f60d6592a771)

## Examples:

Continuous capture decimated counter data using default data buffer size of 250006 atoms (one data atom is 4 bytes).
Wait max two times for 500 msec for missed UDP packets. If first timeout is consumed then resend request is repeated.

```
./lnx64/papi_recorder --device=169.254.50.80 --host=169.254.50.23 --decimate=1.1 --count=0 --mux=0 --wait=500
```

Capture 100 buffers of 2000000 atoms of counter data and save data in file. Wait max two times for 500 msec for missed UDP packets.

```
./lnx64/papi_recorder --device=169.254.50.80 --host=169.254.50.23 --length=2000000 --decimate=1.1 --count=100 --mux=0  --wait=500 --out=.
```

Continuouse capture of DIO data, write 5 1Gbyte files of captured DIO data at 284.1 MSPS.  Wait max two times of 500 msec for missed UDP packets.
For missing UDP packets you will output messages `RESEND req:` on serial console. 

```
./lnx64/papi_recorder --device=169.254.50.80 --host=169.254.50.23 --length=1000000 --decimate=1.1 --count=0 --mux=3 --wait=500 --files=5 --out=.
```

To exit press `<CTRL>-C`.

Continuouse capture 32 DIO data at 284.1 MSPS (9.5Gbits/sec).

```
./lnx64/papi_recorder --device=169.254.50.80 --host=169.254.50.23 --length=2000000 --decimate=1.1 --mux=3 --count=0 --wait=500
```

To exit press `<CTRL>-C`.

If not all UDP packets are received for a data block, an ERROR message will be logged on console but incomplete data buffer will still be written in file with a hole in missing packets.
When capture is terminated statistic data are dumped on console. You could see `WARN: Resend data block not found.` messages, which means that resend request was repeated, but in the mean time all the missing data for block was received and data block was successfully completed (it was moved out of uncompleted block queue). Changing `--wait` parameter sometimes help to tune better the resend requests handling.
