import ctypes, glob, os, sys, fugashi

def find_dicdir():
    for mod_name in ('unidic', 'unidic_lite'):
        try:
            return __import__(mod_name).DICDIR
        except ImportError:
            continue
    return None

pkg = os.path.dirname(fugashi.__file__)
patterns = [
    os.path.join(pkg, '.dylibs', 'libmecab*'),            # macOS wheels
    os.path.join(pkg, '..', 'fugashi.libs', 'libmecab*'), # linux wheels
    os.path.join(pkg, 'libmecab*'),                       # in-tree / some builds
    os.path.join(pkg, '*.dll'),                           # windows
]
hits = [p for pat in patterns for p in glob.glob(pat)]
if not hits:
    sys.exit(f'no bundled libmecab under {pkg}')

lib = ctypes.CDLL(hits[0])
lib.mecab_do.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
lib.mecab_do.restype  = ctypes.c_int

prefix = []
dicdir = find_dicdir()
if dicdir:
    prefix = ['-r', os.path.join(dicdir, 'mecabrc'), '-d', dicdir]

user_args = sys.argv[1:] or ['--help']
argv = [b'mecab'] + [a.encode() for a in prefix + user_args]
Arr  = ctypes.c_char_p * len(argv)
sys.exit(lib.mecab_do(len(argv), Arr(*argv)))
