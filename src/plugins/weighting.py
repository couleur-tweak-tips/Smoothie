import math
import warnings
from numbers import Number


def normalize(weights: list):
    """
    Normalize a list of weights to sum to 1
    """

    if min(weights) < 0:
        absmin = abs(min(weights))
        weights = [w + absmin + 1 for w in weights] # remove negative weights

    tot = sum(weights)
    return [w / tot for w in weights]


def scale_range(n: int, start: Number, end: Number):
    """
    Returns a list of `n` numbers from `start` to `end`
    >>> res = scale_range(5, 0, 1)
    >>> assert res[0] == 0 and res[-1] == 1
    >>> assert len(res) == 5
    """
    if n <= 1: return [start] * n
    return [(x * (end - start) / (n - 1)) + start for x in range(n)]

def vegas_weights(input_fps: int, out_fps: int, blur_amt: int = 1) -> list[float]:
    weights: list
    n_weights = int(input_fps / out_fps * blur_amt)
    if n_weights % 2 == 0:
        weights = [1] + [2] * (n_weights - 1) + [1]
    else:
        weights = [1] * n_weights

    return [1 / w for w in weights]

def scaleWeights(frames):
    tot = sum(frames)
    return [frame / tot for frame in frames]

# modified functions taken from https://github.com/siveroo/HFR-Resampler

# returns a list of values like below:
# [0, 1, 2, 3, ..., frames] -> [a, ..., b]
def scaleRange(frames, a, b):
    return [(x * (b - a) / (frames - 1)) + a for x in range(0, frames)]
    
def ascending(frames):
    r = [*range(frames+1)] # Increments frames by 1
    r = r[1:] # Skips first element
    return r
    
def equal(frames):
    return [1 / frames] * frames

def gaussian(frames, standard_deviation = 2, bound = [0, 2]):
    r = scaleRange(frames, bound[0], bound[1])
    val = [math.exp(-((x) ** 2) / (2 * (standard_deviation ** 2))) for x in r]
    return scaleWeights(val)

def gaussianSym(frames, standard_deviation = 2, bound = [0, 2]):
    max_abs = max(bound)
    r = scaleRange(frames, -max_abs, max_abs)
    val = [math.exp(-((x) ** 2) / (2 * (standard_deviation ** 2))) for x in r]
    return scaleWeights(val)

def pyramid(frames, reverse = False):
    val = []
    if reverse:
        val = [x for x in range(frames, 0, -1)]
    else:
        val = [x for x in range(1, frames + 1)]
    return scaleWeights(val)

def pyramidSym(frames):
    val = [((frames - 1) / 2 - abs(x - ((frames - 1) / 2)) + 1) for x in range(0, frames)]
    return scaleWeights(val)

def funcEval(func, nums):
    try:
        return eval(f"[({func}) for x in nums]")
    except NameError as e:
        raise InvalidCustomWeighting

def custom(frames, func = "", bound = [0, 1]):
    r = scaleRange(frames, bound[0], bound[1])
    val = funcEval(func, r)
    if min(val) < 0: val -= min(val)
    return scaleWeights(val)

# stretch the given array (weights) to a specific length (frames)
# example : frames = 10, weights = [1,2]
# result : val = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2], then normalize it to [0.0667,
# 0.0667, 0.0667, 0.0667, 0.0667, 0.1333, 0.1333, 0.1333, 0.1333, 0.1333]
def divide(frames, weights):
    r = scaleRange(frames, 0, len(weights) - 0.1)
    val = []
    for x in range(0, frames):
        scaled_index = int(r[x])
        val.append(weights[scaled_index])

    if min(val) < 0: val -= min(val)

    return scaleWeights(val)