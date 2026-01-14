#!/usr/bin/env python3

"""Description of papi_iq_data.py"""
"""Read captured IQ raw data and verify content."""

import sys
import numpy as np
import getopt
import matplotlib
matplotlib.use('TKAgg')
#matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import struct
from collections import namedtuple

g_fft_size: int = 0
g_fs_freq: float = 61.44 #MHz

#-------------------------------------------------------------------------------
def dump_help(script_name):
    print("Parameters:")
    print("  -v : Verbose (default False).")
    print("  -i : input file (required, default None).")
    print("  -s : size of FFT frame in 1k points(required, default 0).")
    print("  -h : Help.")
    print("")
    print("Usage:")
    print("  python3 %s -i ./samples_v1.dat -s 2" % script_name)
    return
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class DataCursor(object):
    """A simple data cursor widget that displays the x,y location of a
    matplotlib artist when it is selected."""
    def __init__(self, artists, tolerance=5, offsets=(-20, 20), template='x: %0.2f\ny: %0.2f', display_all=False):
        """Create the data cursor and connect it to the relevant figure.
        "artists" is the matplotlib artist or sequence of artists that will be
            selected.
        "tolerance" is the radius (in points) that the mouse click must be
            within to select the artist.
        "offsets" is a tuple of (x,y) offsets in points from the selected
            point to the displayed annotation box
        "template" is the format string to be used. Note: For compatibility
            with older versions of python, this uses the old-style (%)
            formatting specification.
        "display_all" controls whether more than one annotation box will
            be shown if there are multiple axes.  Only one will be shown
            per-axis, regardless.
        """
        self.template = template
        self.offsets = offsets
        self.display_all = display_all
        if not np.iterable(artists):
            artists = [artists]
        self.artists = artists
        self.axes = tuple(set(art.axes for art in self.artists))
        self.figures = tuple(set(ax.figure for ax in self.axes))

        self.annotations = {}
        for ax in self.axes:
            self.annotations[ax] = self.annotate(ax)

        for artist in self.artists:
            artist.set_picker(tolerance)
        for fig in self.figures:
            fig.canvas.mpl_connect('pick_event', self)

    def annotate(self, ax):
        """Draws and hides the annotation box for the given axis "ax"."""
        annotation = ax.annotate(self.template, xy=(0, 0), ha='right',
                xytext=self.offsets, textcoords='offset points', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                )
        annotation.set_visible(False)
        return annotation

    def __call__(self, event):
        """Intended to be called through "mpl_connect"."""
        # Rather than trying to interpolate, just display the clicked coords
        # This will only be called if it's within "tolerance", anyway.
        x, y = event.mouseevent.xdata, event.mouseevent.ydata
        annotation = self.annotations[event.artist.axes]
        if x is not None:
            if not self.display_all:
                # Hide any other annotation boxes...
                for ann in self.annotations.values():
                    ann.set_visible(False)
            # Update the annotation in the current axis..
            annotation.xy = x, y
            annotation.set_text(self.template % (x, y))
            annotation.set_visible(True)
            event.canvas.draw()
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def plot_sig(a_name, a_siga, a_sigb = None):

    if a_sigb is None:
        a_sigb = []    
    
    plt.figure(a_name)
    line_a, = plt.plot(a_siga, color='blue', label='SigQ')
    artists_to_track = [line_a]
    
    if (len(a_sigb) != 0):
        line_b, = plt.plot(a_sigb, color='orange', label='SigI')
        artists_to_track.append(line_b)
    
    plt.xlabel("Samples")
    plt.grid(True)

    DataCursor(artists=artists_to_track, template='x: %0.0f\ny: %0.1f')

    plt.legend()
    plt.draw()
    
#    plt.show()
    return
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def plot_fft(a_name, a_freqs, a_siga):
    
    plt.figure(figsize=(10, 5))
    line_a, = plt.plot(a_freqs, a_siga, color='blue')
    artists_to_track = [line_a]
    
    plt.title(a_name)
    plt.xlabel("MHz")
    plt.ylabel("dB")
    plt.grid(True)

    DataCursor(artists=artists_to_track, template='x: %0.0f\ny: %0.1f')

#    plt.show()
    return
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#typedef struct Data_StartHeader_tag {
#  uint32_t nTestVersion;
#  char     szDateTime[128];
#  char     szIp[128];
#  uint32_t nMtu;
#  float    fDeviceTemp;
#  uint32_t nNofAtoms;
#  uint32_t nAtomSize;
#  uint32_t nMetaDataSize;
#  uint32_t nDataType;
#  uint32_t nDataSize;
#  uint32_t nSinglePayload;
#  uint32_t nNofPackets;
#  uint32_t nFPGARev;
#} Data_StartHeader_t;
def read_startheader(a_fp):
    
    #NOTE: data in format must be organized by descending size or struct.calcsize() calculates it wrong.
    hdr_fmt = "@I128s128sIfIIIIIIII"
    hdr_len = struct.calcsize(hdr_fmt)
    hdr_unpack = struct.Struct(hdr_fmt).unpack_from

    hdr_data = a_fp.read(hdr_len)
    hdr_struct = namedtuple("Data_StartHeader_t",
                            "nTestVersion szDateTime szIp nMtu fDeviceTemp nNofAtoms "
                            "nAtomSize nMetaDataSize nDataType nDataSize nSinglePayload "
                            "nNofPackets nFPGARev")
    hdr = hdr_struct._make(hdr_unpack(hdr_data))

    return hdr
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#typedef struct Data_Header_tag {
#  uint64_t lDataTimestamp;
#  uint32_t nBlockId;
#  uint32_t nRawDataSize;
#  uint32_t nQueued;
#  uint32_t nPacketsMissed;
#  uint32_t nCPUsLoads;
#  uint32_t nTimesToLeave;
#  uint32_t nTimesToResend;
#  uint32_t nTail;
#} Data_Header_t;
def read_dataheader(a_fp):
    
    #NOTE: data in format must be organized by descending size or struct.calcsize() calculates it wrong.
    hdr_fmt = "@QIIIIIIII"
    hdr_len = struct.calcsize(hdr_fmt)
    hdr_unpack = struct.Struct(hdr_fmt).unpack_from

    hdr_data = a_fp.read(hdr_len)
    if not hdr_data:
        return None, None
    hdr_struct = namedtuple("Data_Header_t",
                            "lDataTimestamp nBlockId nRawDataSize nQueued nPacketsMissed nCPUsLoads nTimesToLeave nTimesToResend nTail")
    hdr = hdr_struct._make(hdr_unpack(hdr_data))

    data = a_fp.read(hdr.nRawDataSize)

    return hdr, data
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def get_bit_reversed_indices(n=2048):
    """Generates an array of bit-reversed indices for length n."""
    # n must be a power of 2
    indices = np.arange(n, dtype=np.uint32)
    # Bit manipulation trick to reverse bits for 2^11 (2048)
    # We use .byteswap() or manual bit manipulation depending on precision
    bits = int(np.log2(n))
    reversed_indices = np.zeros_like(indices)
    for i in range(bits):
        reversed_indices |= ((indices >> i) & 1) << (bits - 1 - i)
    return reversed_indices
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def unpack_raw24(byte_buffer, a_len):

    total_iq_data = a_len
    expected_bytes = total_iq_data * 6
    
    if len(byte_buffer) != expected_bytes:
        print(f"Error: Buffer size mismatch. Expected {expected_bytes} bytes, got {len(byte_buffer)}")
        return None
    
    raw_64 = np.frombuffer(byte_buffer, dtype='<u8').reshape(-1, 3)
    r0, r1, r2 = raw_64[:, 0], raw_64[:, 1], raw_64[:, 2]

    v = np.empty((raw_64.shape[0], 4), dtype=np.uint64)
    v[:, 0] = r0 & 0xFFFFFFFFFFFF
    v[:, 1] = (r0 >> 48) | ((r1 & 0xFFFFFFFF) << 16)
    v[:, 2] = (r1 >> 32) | ((r2 & 0xFFFF) << 32)
    v[:, 3] = r2 >> 16

    I = (((v & 0xFFFFFF) << 8).astype(np.int32) >> 8).astype(np.float32)
    Q = ((((v >> 24) & 0xFFFFFF) << 8).astype(np.int32) >> 8).astype(np.float32)

    complex_data = (I + 1j * Q).ravel()
    
    return complex_data
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def unpack_raw32(byte_buffer, a_len):

    total_iq_data = a_len
    expected_bytes = total_iq_data * 8
    
    if len(byte_buffer) != expected_bytes:
        print(f"Error: Buffer size mismatch. Expected {expected_bytes} bytes, got {len(byte_buffer)}")
        return None
    
    # View buffer as 64-bit unsigned integers
    raw_64 = np.frombuffer(byte_buffer, dtype='<u8')
    iq_split = raw_64.view(np.int32).reshape(-1, 2)
    
    I = iq_split[:, 0].astype(np.float32)
    Q = iq_split[:, 1].astype(np.float32)

    complex_data = (I + 1j * Q).ravel()
    
    return complex_data
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def get_data(a_datas, a_len, a_atom_size, a_data_type):

    global g_fft_size;
    
    data_hdr, data_buff = a_datas
    raw_data = np.frombuffer(data_buff, dtype=np.uint8)

    if (g_fft_size == 2048):
        # nData<Q0|I0> 2x24bit
        unpacked_data = unpack_raw24(raw_data, ((a_len//3)*4))
        nLength = (a_len//3)*4
    elif (g_fft_size == 65536):
        # nData<Q0|I0> 2x32bit
        unpacked_data = unpack_raw32(raw_data, a_len)
        nLength = a_len
    else:
        return None

    DataPoints = namedtuple("Data",
                            "data_ts data_id queued len dtype pckt_missed cpu_loads ttl resend values")

    data_points = DataPoints(data_hdr.lDataTimestamp, data_hdr.nBlockId, data_hdr.nQueued, nLength, raw_data.dtype,
                             data_hdr.nPacketsMissed, data_hdr.nCPUsLoads.to_bytes(4, byteorder='little'), 
                             data_hdr.nTimesToLeave, data_hdr.nTimesToResend, unpacked_data)

    return data_points
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def get_data_line(a_data):

    DataLine = namedtuple("DataLine",
                          "data_ts data_idx queued pckt_missed "
                          "cpu3_load cpu2_load cpu1_load cpu0_load ttl resend values")

    data_ts     = np.array([], dtype=np.uint64)
    data_idx    = np.array([], dtype=np.uint32)
    queued      = np.array([], dtype=np.uint32)
    pckt_missed = np.array([], dtype=np.uint32)
    cpu3_load   = np.array([], dtype=np.uint8)
    cpu2_load   = np.array([], dtype=np.uint8)
    cpu1_load   = np.array([], dtype=np.uint8)
    cpu0_load   = np.array([], dtype=np.uint8)
    ttl         = np.array([], dtype=np.uint32)
    resend      = np.array([], dtype=np.uint32)
    values      = []
     
    for idx in range(len(a_data)):
        data_ts     = np.append(data_ts, np.uint64(a_data[idx].data_ts))
        data_idx    = np.append(data_idx, np.uint32(a_data[idx].data_id-1)) #Zero based index
        queued      = np.append(pckt_missed, np.uint32(a_data[idx].queued))
        pckt_missed = np.append(pckt_missed, np.uint32(a_data[idx].pckt_missed))
        cpu3_load   = np.append(cpu3_load, np.uint8(a_data[idx].cpu_loads[3]))
        cpu2_load   = np.append(cpu2_load, np.uint8(a_data[idx].cpu_loads[2]))
        cpu1_load   = np.append(cpu1_load, np.uint8(a_data[idx].cpu_loads[1]))
        cpu0_load   = np.append(cpu0_load, np.uint8(a_data[idx].cpu_loads[0]))
        ttl         = np.append(ttl, np.uint32(a_data[idx].ttl))
        resend      = np.append(resend, np.uint32(a_data[idx].resend))
        values.append(a_data[idx].values)

    concatenate_array = np.hstack(values)
    data_line = DataLine(data_ts, data_idx, queued, pckt_missed, cpu3_load, cpu2_load, cpu1_load, cpu0_load, ttl, resend, concatenate_array)
    
    return data_line, a_data[idx].len
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def main(argv):
    input_fname = None
    verbose = False
    max_plot_len = 200000 # Limit plot length

    global g_fft_size;
    global g_fs_freq

    try:
        opts, args = getopt.getopt(argv, 'hvi:s:', ['verbose', 'input=', 'size='])
    except getopt.GetoptError:
        dump_help(argv[0])
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            dump_help(argv[0])
            sys.exit()
        elif opt in ('-i', '--input'):
            input_fname = arg
        elif opt in ('-s', '--size'):
            g_fft_size = int(arg)*1024
        elif opt in ('-v', '--verbose'):
            verbose = True

    if (input_fname == None):
        print("Error: Missing required command line parameters. Try with -h option.")
        sys.exit()

    if (g_fft_size == 0):
        print("Error: Missing required command line parameters. Try with -h option.")
        sys.exit()

    #---------------------------------------------------------------------------
    fp = open(input_fname, "rb")

    start_header = read_startheader(fp)

    nTestVersion = start_header.nTestVersion
    szDateTime = start_header.szDateTime.split(b'\0',1)[0]
    szIp = start_header.szIp.split(b'\0',1)[0]
    nMtu = start_header.nMtu
    fDeviceTemp = start_header.fDeviceTemp
    nNofAtoms = start_header.nNofAtoms
    nAtomSize = start_header.nAtomSize
    nMetaDataSize = start_header.nMetaDataSize
    nDataType = start_header.nDataType
    nDataSize = start_header.nDataSize
    nSinglePayload = start_header.nSinglePayload
    nNofPackets = start_header.nNofPackets
    nFPGARev = start_header.nFPGARev

    print(f"Test:{szDateTime} Raw captured version:{nTestVersion}")
    print(f"IP:{szIp} MTU:{nMtu}")
    print(f"DeviceTemp:{fDeviceTemp:.1f}")
    print(f"DataType:{nDataType}")
    print(f"Length:{nNofAtoms} AtomSize:{nAtomSize} MetaDataSize:{nMetaDataSize} DataSize:{nDataSize}")
    print(f"SinglePayloadSize:{nSinglePayload} NofPackets:{nNofPackets}")
    print(f"FPGARev:{nFPGARev}")

    datas = []
    while True:
        data_header, raw_data = read_dataheader(fp)
        if not data_header:
            break
        datas.append((data_header, raw_data))

    fp.close()
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    data_lines = []
    NOF_processing = len(datas)
    for idx in range(NOF_processing):
        dl = get_data(a_datas = datas[idx], a_len = nNofAtoms, a_atom_size = nAtomSize, a_data_type = nDataType)
        data_lines.append(dl)
    
    # Flatten data.
    data_line, nValuesSize = get_data_line(data_lines)

    print(f"INFO: NOF processing:{NOF_processing} out of:{len(datas)} captured data")
    print(f"INFO: Values DataType:{nDataType} length of values:{nValuesSize}")
    #---------------------------------------------------------------------------
    
    #---------------------------------------------------------------------------
    #Checks.

    #Check: BlockId diff == 1
    BlockId_diff = np.ediff1d(data_line.data_idx)
    BlockId_equal = np.all(BlockId_diff == 1)
    if (BlockId_equal == False):
        print(f"ERROR: BlockId NOT continues")
 
    #Check for missed packets
    all_packets = np.all(data_line.pckt_missed == 0)
    if (all_packets == False):
        non_zero_blocks = np.nonzero(data_line.pckt_missed)
        print(f"ERROR: NOT all packets captured")
        #print(f"Data blocks with missed packets:{non_zero_blocks[0]}")
    
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    max_cpu0_load = max(data_line.cpu0_load) 
    max_cpu1_load = max(data_line.cpu1_load) 
    max_cpu2_load = max(data_line.cpu2_load) 
    max_cpu3_load = max(data_line.cpu3_load) 
    #print(f"Max load CPU0:{max_cpu0_load} CPU1:{max_cpu1_load} CPU2:{max_cpu2_load} CPU3:{max_cpu3_load}")
    print(f"Max load CPU0:{max_cpu0_load} CPU1:{max_cpu1_load}")
    #plot_sig("CPU0", data_line.cpu0_load)
    #plot_sig("CPU1", data_line.cpu1_load)
    
    max_queue =  max(data_line.queued)
    print(f"INFO: Max queued:{max_queue}")
    #plot_sig("Queues", data_line.queued)
    
    dt_lTimestamp = np.ediff1d(data_line.data_ts)
    #plot_sig("dt_lTimestamp", dt_lTimestamp)
    #---------------------------------------------------------------------------
    
    rev_idx = get_bit_reversed_indices(g_fft_size)
    window_natural = np.hamming(g_fft_size)
    window_rev = window_natural[rev_idx]
    
    num_ffts = len(data_line.values) // g_fft_size
    complex_frames = data_line.values.reshape(num_ffts, g_fft_size)
    windowed = complex_frames * window_rev
    reordered_frames = windowed[:, rev_idx]
    fft_frames = np.fft.fftshift(reordered_frames, axes=1)
    freqs = np.fft.fftshift(np.fft.fftfreq(g_fft_size, d=1/g_fs_freq))
    
    magnitude_db = 20 * np.log10(np.abs(fft_frames[0]) + 1e-9) # Avoid log(0)
    plot_fft("FFT frame[0]", freqs, magnitude_db)
    
    plt.show()
    
    return
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    assert sys.version_info >= (3, 5)
    main(sys.argv[1:])
