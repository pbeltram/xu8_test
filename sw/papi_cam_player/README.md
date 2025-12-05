**papi_cam_player**

Program will display images from captured data file. Format of data file is the same as for Python test scripts in top `/python/` directory.
Images are displayed as gray scale 16 bit where each RGGB pixel is transformed to gray scale pixel.
Program is in source code, so fell free to modify it.

**Program options**

```
"-i, --input fname  Input file name (<dir>/samples_vX.dat). (Optional, default is ./samples_v1.dat)."
"-v, --verbose      Print debug messages to console."
```

---

On Linux:

```
./Debug/papi_cam_player -i ./samples_v1.dat
./Debug/papi_cam_player -i ./samples_v1_1.dat --verbose
```

**Build**

Build and test was done with Qt 5.15.
It is Qt qmake based build. Make file is created via `qmake -o Makefile papi_cam_player.pro`. After that you build binary with `make`. Result is in `./Debug/` directory.
