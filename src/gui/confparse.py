yes = ['true', 'yes', 'y', '1']
no = ['false', 'no', 'n', '0', 'null', '', None]


class interpolation:
    def __init__(self, config) -> None:
        self.ip = config['interpolation']

    def enabled(self):
        if str(self.ip['enabled']).lower() in yes:
            return True
        else:
            return False

    def gpu(self):
        if str(self.ip['gpu']).lower() in yes:
            return True
        else:
            return False

    def fps(self):
        fps = int(self.ip['fps'])
        if fps <= 120:
            return 120
        else:
            return fps

    def speed(self):
        speed = self.ip['speed']
        if speed.lower() not in ['medium', 'fast', 'faster']:
            return 'Medium'
        else:
            return speed.capitalize()

    def tuning(self):
        tuning = self.ip['tuning']
        tuning_values = ['film', 'animation', 'smooth', 'weak']
        if tuning not in tuning_values:
            return 'Weak'
        else:
            return tuning.capitalize()

    def algo(self):
        algo = int(self.ip['algorithm'])
        if algo not in [1, 2, 10, 11, 13, 21, 23]:
            return '23'
        else:
            return str(algo)


class frame_blending:
    def __init__(self, config) -> None:
        self.fb = config['frame blending']

    def enabled(self):
        if str(self.fb['enabled']).lower() in yes:
            return True
        else:
            return False

    def fps(self):
        fps = int(self.fb['fps'])
        if fps <= 30:
            return 30
        else:
            return fps

    def intensity(self):
        intensity = float(self.fb['intensity'])
        if intensity <= 1.2:
            return 1.2
        else:
            return intensity

    def weighting(self):
        weighting = self.fb['weighting']
        if weighting not in ['equal', 'gaussian', 'gaussian_sym', 'pyramid', 'pyramid_sym']:
            return 'Equal'
        else:
            return ' '.join([word.capitalize()
                             for word in weighting.replace('_', ' ').split(' ')])


class flowblur():
    def __init__(self, config):
        self.flblur = config['flowblur']

    def enabled(self):
        if str(self.flblur['enabled']).lower() in yes:
            return True
        else:
            return False

    def amount(self):
        return int(self.flblur['amount'])

    def mask(self):
        return self.flblur['mask']


class encoding:
    def __init__(self, config):
        self.enc = config['encoding']

    def process(self):
        return self.enc['process']

    def args(self):
        return self.enc['args']


class misc:
    def __init__(self, config):
        self.ms = config['misc']

    def mpv_bin(self):
        return self.ms['mpv bin']

    def stay_on_top(self):
        if str(self.ms['stay on top']).lower() in yes:
            return True
        else:
            return False

    def ding_after(self):
        return int(self.ms['ding after'])

    def folder(self):
        return self.ms['folder']

    def container(self):
        return self.ms['container'].lower()

    def deduplthreshold(self):
        return float(self.ms['dedupthreshold'])

    def prefix(self):
        prefix = self.ms['prefix']
        if prefix != None:
            return prefix.capitalize()
        else:
            return prefix

    def suffix(self):
        suffix = self.ms['suffix']
        if suffix != None:
            return str(suffix).capitalize()
        else: 
            return suffix
        
    def verbose(self):
        if str(self.ms['verbose']).lower() in yes:
            return True
        else:
            return False


class timescale:
    def __init__(self, config):
        self.ts = config['timescale']

    def input(self):
        return float(self.ts['in'])

    def output(self):
        return float(self.ts['out'])
