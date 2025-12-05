
---

Program will display images in captured data file. Format of data file is the same as for Python test scripts in top `/python/` directory.
Program is in source code, so fell free to modify it.

**Program options**

```
"-i, --input fname  Input file name (<dir>/samples_vX.dat). (Optional, default is ./samples_v1.dat)."
"-v, --verbose      Print debug messages to console."
```

---

On Linux:
```
./Debug/papi_cam_viewer --input=./samples_v1.dat
./Debug/papi_cam_viewer --input=./samples_v1_1.dat --verbose
```
---

**Build**

Build and test was done with Qt 5.15.
It is Qt qmake based build. Make file is created via `qmake -o Makefile papi_cam_player.pro`.
After that you start build with `make`. Result is in `./Debug/` directory.

---

