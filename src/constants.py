recipe = '''
interpolation:
  enabled: yes
  fps: 480
  mask: yes
  speed: medium
  tuning: weak
  algorithm: 23
  gpu: true

frame blending:
  enabled: yes
  fps: 60
  intensity: 1.0
  weighting: equal

flowblur:
  enabled: no
  amount: 100
  mask: cian

encoding:
  process: ffmpeg
  args: H264 CPU

misc:
  verbose: false
  container: .MKV
  flavors: fruits
  folder: 
  deduplication: no
  dedupthreshold: 0.001

timescale:
  in: 1.0
  out: 1.0
'''

EncPresets = { # Same setup as TweakList's Get-EncArgs
    'H264': {
        'NVENC':       "h264_nvenc -preset p7 -rc vbr -b:v 250M -cq 18",
        'AMF':         "h264_amf -quality quality -qp_i 12 -qp_p 12 -qp_b 12",
        'QuickSync':   "h264_qsv -preset veryslow -global_quality:v 15",
        'CPU':         "libx264 -preset slower -x264-params aq-mode=3 -crf 15 -pix_fmt yuv420p10le"
    },
    'H265': {
        'NVENC':       "hevc_nvenc -preset p7 -rc vbr -b:v 250M -cq 18",
        'AMF':         "hevc_amf -quality quality -qp_i 16 -qp_p 18 -qp_b 20",
        'QuickSync':   "hevc_qsv -preset veryslow -global_quality:v 18",
        'CPU':         "libx265 -preset slow -x265-params aq-mode=3 -crf 18 -pix_fmt yuv420p10le"
    }
}