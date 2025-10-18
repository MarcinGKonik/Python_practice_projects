import ctypes

# Load the ODAS library
try:
    odas_lib = ctypes.CDLL('odas/build/lib/libodas.so')
except OSError:
    print("Could not load the ODAS library. Make sure it is compiled and the path is correct.")
    exit()

# Define the necessary data structures
class MicsObj(ctypes.Structure):
    _fields_ = [
        ("nChannels", ctypes.c_uint),
        ("nPairs", ctypes.c_uint),
        ("mu", ctypes.POINTER(ctypes.c_float)),
        ("sigma2", ctypes.POINTER(ctypes.c_float)),
        ("direction", ctypes.POINTER(ctypes.c_float)),
        ("thetaAllPass", ctypes.POINTER(ctypes.c_float)),
        ("thetaNoPass", ctypes.POINTER(ctypes.c_float)),
    ]

class SamplerateObj(ctypes.Structure):
    _fields_ = [
        ("mu", ctypes.c_uint),
        ("sigma2", ctypes.c_float),
    ]

class SoundspeedObj(ctypes.Structure):
    _fields_ = [
        ("mu", ctypes.c_float),
        ("sigma2", ctypes.c_float),
    ]

class SpatialfiltersObj(ctypes.Structure):
    _fields_ = [
        ("nFilters", ctypes.c_uint),
        ("direction", ctypes.POINTER(ctypes.c_float)),
        ("thetaAllPass", ctypes.POINTER(ctypes.c_float)),
        ("thetaNoPass", ctypes.POINTER(ctypes.c_float)),
    ]

class ModSSLCfg(ctypes.Structure):
    _fields_ = [
        ("mics", ctypes.POINTER(MicsObj)),
        ("samplerate", ctypes.POINTER(SamplerateObj)),
        ("soundspeed", ctypes.POINTER(SoundspeedObj)),
        ("spatialfilters", ctypes.POINTER(SpatialfiltersObj)),
        ("interpRate", ctypes.c_uint),
        ("epsilon", ctypes.c_float),
        ("nLevels", ctypes.c_uint),
        ("levels", ctypes.POINTER(ctypes.c_uint)),
        ("deltas", ctypes.POINTER(ctypes.c_int)),
        ("nMatches", ctypes.c_uint),
        ("probMin", ctypes.c_float),
        ("nRefinedLevels", ctypes.c_uint),
        ("nThetas", ctypes.c_uint),
        ("gainMin", ctypes.c_float),
    ]

class FreqsObj(ctypes.Structure):
    _fields_ = [
        ("nSignals", ctypes.c_uint),
        ("halfFrameSize", ctypes.c_uint),
        ("array", ctypes.POINTER(ctypes.POINTER(ctypes.c_float))),
    ]

class MsgSpectraObj(ctypes.Structure):
    _fields_ = [
        ("timeStamp", ctypes.c_ulonglong),
        ("fS", ctypes.c_uint),
        ("freqs", ctypes.POINTER(FreqsObj)),
    ]

class MsgSpectraCfg(ctypes.Structure):
    _fields_ = [
        ("halfFrameSize", ctypes.c_uint),
        ("nChannels", ctypes.c_uint),
        ("fS", ctypes.c_uint),
    ]

class PotsObj(ctypes.Structure):
    _fields_ = [
        ("nPots", ctypes.c_uint),
        ("array", ctypes.POINTER(ctypes.c_float)),
    ]

class MsgPotsObj(ctypes.Structure):
    _fields_ = [
        ("timeStamp", ctypes.c_ulonglong),
        ("fS", ctypes.c_uint),
        ("pots", ctypes.POINTER(PotsObj)),
    ]

class MsgPotsCfg(ctypes.Structure):
    _fields_ = [
        ("nPots", ctypes.c_uint),
        ("fS", ctypes.c_uint),
    ]


class ModSSLObj(ctypes.Structure):
    pass


# Define the function prototypes
odas_lib.mod_ssl_construct.argtypes = [ctypes.POINTER(ModSSLCfg), ctypes.POINTER(MsgSpectraCfg), ctypes.POINTER(MsgPotsCfg)]
odas_lib.mod_ssl_construct.restype = ctypes.POINTER(ModSSLObj)

odas_lib.mod_ssl_destroy.argtypes = [ctypes.POINTER(ModSSLObj)]
odas_lib.mod_ssl_destroy.restype = None

odas_lib.mod_ssl_process.argtypes = [ctypes.POINTER(ModSSLObj)]
odas_lib.mod_ssl_process.restype = ctypes.c_int

odas_lib.mod_ssl_connect.argtypes = [ctypes.POINTER(ModSSLObj), ctypes.POINTER(MsgSpectraObj), ctypes.POINTER(MsgPotsObj)]
odas_lib.mod_ssl_connect.restype = None

odas_lib.mod_ssl_disconnect.argtypes = [ctypes.POINTER(ModSSLObj)]
odas_lib.mod_ssl_disconnect.restype = None

odas_lib.mod_ssl_enable.argtypes = [ctypes.POINTER(ModSSLObj)]
odas_lib.mod_ssl_enable.restype = None

odas_lib.mod_ssl_disable.argtypes = [ctypes.POINTER(ModSSLObj)]
odas_lib.mod_ssl_disable.restype = None

odas_lib.mod_ssl_cfg_construct.argtypes = []
odas_lib.mod_ssl_cfg_construct.restype = ctypes.POINTER(ModSSLCfg)

odas_lib.mod_ssl_cfg_destroy.argtypes = [ctypes.POINTER(ModSSLCfg)]
odas_lib.mod_ssl_cfg_destroy.restype = None

odas_lib.msg_spectra_construct.argtypes = [ctypes.POINTER(MsgSpectraCfg)]
odas_lib.msg_spectra_construct.restype = ctypes.POINTER(MsgSpectraObj)

odas_lib.msg_spectra_destroy.argtypes = [ctypes.POINTER(MsgSpectraObj)]
odas_lib.msg_spectra_destroy.restype = None

odas_lib.msg_pots_construct.argtypes = [ctypes.POINTER(MsgPotsCfg)]
odas_lib.msg_pots_construct.restype = ctypes.POINTER(MsgPotsObj)

odas_lib.msg_pots_destroy.argtypes = [ctypes.POINTER(MsgPotsObj)]
odas_lib.msg_pots_destroy.restype = None


# Python wrapper functions
def mod_ssl_construct(mod_ssl_config, msg_spectra_config, msg_pots_config):
    return odas_lib.mod_ssl_construct(mod_ssl_config, msg_spectra_config, msg_pots_config)

def mod_ssl_destroy(obj):
    odas_lib.mod_ssl_destroy(obj)

def mod_ssl_process(obj):
    return odas_lib.mod_ssl_process(obj)

def mod_ssl_connect(obj, in_obj, out_obj):
    odas_lib.mod_ssl_connect(obj, in_obj, out_obj)

def mod_ssl_disconnect(obj):
    odas_lib.mod_ssl_disconnect(obj)

def mod_ssl_enable(obj):
    odas_lib.mod_ssl_enable(obj)

def mod_ssl_disable(obj):
    odas_lib.mod_ssl_disable(obj)

def mod_ssl_cfg_construct():
    return odas_lib.mod_ssl_cfg_construct()

def mod_ssl_cfg_destroy(cfg):
    odas_lib.mod_ssl_cfg_destroy(cfg)

def msg_spectra_construct(cfg):
    return odas_lib.msg_spectra_construct(cfg)

def msg_spectra_destroy(obj):
    odas_lib.msg_spectra_destroy(obj)

def msg_pots_construct(cfg):
    return odas_lib.msg_pots_construct(cfg)

def msg_pots_destroy(obj):
    odas_lib.msg_pots_destroy(obj)
