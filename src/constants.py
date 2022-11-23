from os import path
from platform import system as ossystem

ENC_PRESETS = {
    'h264': {
        'nvenc':     "-c:v h264_nvenc -preset p7 -rc vbr -b:v 250M -cq 18",
        'amf':       "-c:v h264_amf -quality quality -qp_i 16 -qp_p 18 -qp_b 22",
        'quicksync': "-c:v h264_qsv -preset veryslow -global_quality:v 15",
        'cpu':       "-c:v libx264 -preset slow -aq-mode 3 -crf 18"
    },
    'h265': {
        # the '-pix_fmt yuv420p10le' bit makes it a lil more efficient, but may introduce incompatibility with your NLE
        'nvenc':     "-c:v hevc_nvenc -preset p7 -rc vbr -b:v 250M -cq 20 -pix_fmt yuv420p10le",
        'amf':       "-c:v hevc_amf -quality quality -qp_i 18 -qp_p 20 -qp_b 24 -pix_fmt yuv420p10le",
        'quicksync': "-c:v hevc_qsv -preset veryslow -global_quality:v 18 -pix_fmt yuv420p10le",
        'cpu':       "-c:v libx265 -preset medium -x265-params aq-mode=3:no-sao=1 -crf 20 -pix_fmt yuv420p10le"
    }
}

FRUITS = 'Berry',      'Cherry',   'Cranberry',   'Coconut',   'Kiwi',      \
         'Avocado',    'Durian',   'Lemon',       'Fig',       'Lime'       \
         'Mirabelle',  'Banana',   'Pineapple',   'Pitaya',    'Blueberry', \
         'Raspberry',  'Apricot',  'Strawberry',  'Melon',     'Papaya',    \
         'Apple',      'Pear',     'Orange',      'Mango',     'Plum',      \
         'Peach',      'Grape',    'Tomato',      'Cucumber',  'Eggplant',  \
         'Guava',      'Honeydew', 'Lychee',      'Nut',       'Quince',    \
         'Olive',      'Passion',  'Plum',        'Pomelo',    'Raisin'

IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.webp', '.tiff', '.bmp', '.jxl', '.avif')
VIDEO_EXTS = ('.mp4', '.mkv', '.mov', '.mkv', '.wmv', '.webm', '.ts')

# Can all be absolute
VSPIPE_PATH_LINUX = 'vspipe'
DEFAULT_VPY_NAME = 'vitamix.vpy' # Can be overriden with -vpy 
DEFAULT_RECIPE = "recipe.yaml" 

# These are not really constants but w/e, they workie 😋
SRCDIR = path.dirname(__file__)
SMDIR = path.dirname(SRCDIR) # That's ../../ if you look at it relative from Smoothie/src/main.py
MASKDIR = path.join(SMDIR, "masks") # Except this one

ISLINUX = ossystem() == 'Linux'
ISWIN = ossystem() == 'Windows'