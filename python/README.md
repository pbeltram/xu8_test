**papi_check_data**

Script will read captured data and perform some checks on captured data.
For captured DataType=0 (ADC decimated counter) it will verify that `diff(succ-pred) == 1` for all captured data.
By default scripts plots only first 200000 data samples (or less if length of captured data is shorter).

Parameters:

```
-i : input file (required, default None).
-h : Help.
```

Run python script on Ubuntu:

```
./papi_check_data.py -i ./samples_v1.dat
```

Run python script on Windows 11:

```
python.exe .\papi_check_data.py -i .\samples_v1.dat
```

**papi_image_data**

Script will read captured data and perform some checks on captured data.
It will unpack captured raw12 image data to 16bit pixel data and display first captured image in gray scale.
Parameters:

```
-i : input file (required, default None).
-h : Help.
```

Run python script on Ubuntu:

```
./papi_image_data.py -i ./samples_v1.dat
```

**papi_iq_data**

Script will read captured RX1/RX2 IQ data from xu8_fmcomms3 and display plot of sampled data.
Parameters:

```
-i : input file (required, default None).
-h : Help.
```

**papi_fft_data**

Script will read captured FFT IQ data from xu8_fmcomms3 stream=1 (64k FFT from RX1) or stream=2 (2k FFT from RX2) display FFT plot.
Parameters:

```
-i : input file (required, default None).
-s : FFT size in 1k samples (required, default None).
-h : Help.
```

Example for 64k FFT captured from stream=1:
```
./papi_fft_data.py -i ./samples_v1.dat -s 64
```

