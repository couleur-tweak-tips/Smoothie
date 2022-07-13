recipe = '''
interpolation:
  enabled: {ip_enabled}
  fps: {ip_fps}
  speed: {ip_speed}
  tuning: {ip_tuning}
  algorithm: {ip_algo}
  gpu: {ip_gpu}

frame blending:
  enabled: {fb_enabled}
  fps: {fb_fps}
  intensity: {fb_intensity}
  weighting: {fb_weighting}

flowblur:
  enabled: {flb_enabled}
  amount: {flb_amount}
  mask: {flb_mask}

encoding:
  process: {process}
  args: {args}

misc:
  mpv bin: {mpv_bin}
  stay on top: {stay_on_top}
  verbose: {verbose}
  ding after: {ding_after}
  folder: {folder}
  container: {container}
  flavors: {flavors}
  dedupthreshold: {deduplthreshold}

timescale:
  in: {timescale_in}
  out: {timescale_out}
'''

def elements_values(ip, fb, flb, ms, enc, ts): return {
    # Interpolation
    'ip_enabled': ip.enabled(),
    'ip_gpu': ip.gpu(),
    'ip_fps': ip.fps(),
    'ip_speed': ip.speed(),
    'ip_tuning': ip.tuning(),
    'ip_algo': ip.algo(),

    # Frame Blending
    'fb_enabled': fb.enabled(),
    'fb_fps': fb.fps(),
    'fb_intensity': fb.intensity(),
    'fb_weighting': fb.weighting(),

    # Flowblur
    'flb_enabled': flb.enabled(),
    'flb_mask': flb.mask(),
    'flb_amount': flb.amount(),

    # Deduplication
    'deduplthreshold': ms.deduplthreshold(),

    # Timescale
    'timescale_in': ts.input(),
    'timescale_out': ts.output(),

    # Video
    'folder': ms.folder(),
    'container': ms.container(),
    'flavors': ms.flavors(),

    # Encoding
    'process': enc.process(),
    'args': enc.args(),

    # Settings
    'verbose': ms.verbose(),
    'stay on top': ms.stay_on_top(),
    'mpv bin': ms.mpv_bin()}


def config_values(function): return {
    # Interpolation
    'ip_enabled': function('ip_enabled'),
    'ip_gpu': function('ip_gpu'),
    'ip_fps': function('ip_fps'),
    'ip_speed': function('ip_speed').lower(),
    'ip_tuning': function('ip_tuning').lower(),
    'ip_algo': function('ip_algo').split(':')[0],

    # Frame Blending
    'fb_enabled': function('fb_enabled'),
    'fb_fps': function('fb_fps'),
    'fb_intensity': round(function('fb_intensity'), 2),
    'fb_weighting': function('fb_weighting').lower(),

    # Flowblur
    'flb_enabled': function('flb_enabled'),
    'flb_mask': function('flb_mask'),
    'flb_amount': function('flb_amount'),

    # Deduplication
    'deduplthreshold': round(function('deduplthreshold'), 2),

    # Timescale
    'timescale_in': round(function('timescale_in'), 2),
    'timescale_out': round(function('timescale_out'), 2),

    # Output
    'folder': function('folder'),
    'container': function('container'),
    'flavors': function('flavors').lower(),

    'process': function('process'),
    'args': function('args'),

    # Settings
    'verbose': function('verbose'),
    'stay_on_top': function('stay on top'),
    'mpv_bin': function('mpv bin'),
    'ding_after': function('ding after')}
