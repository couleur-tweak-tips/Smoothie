
# 🧋 Smoothie [WIP]

Smoothie is a cross-platform fork of [blur](https://github.com/f0e/blur) rewritten in Python with a focus on ease of use and integration in your existing routine.


### 5 ways to feed your videos to Smoothie:
* MPV Trimmer (most recommended)
* Dead simple open file dialog when launching it from Start
* Send To (accepts multiple input)
* `sm` on the command line
* Pre-Renderer integration to your NLE

```diff
- Preview (just set extension to .MKV and play unfinished video)
+ Pretty YAML config
+ Unique config instead of per folder (set up like this per default, see --config in CLI)
+ Cross-platform (tested on Arch, Ubuntu & Windows)
+ Completely portable and automated installation via Scoop
+ FlowBlur (RSMB-like motion blur)
+ MPV Trimmer ingration (great alternative to LosslessCut)
+ 
```


<details>
<summary> It also has a simplified configuration, here called a "recipe" ;) </summary>

> Learn what each setting does on it's [wiki page](https://github.com/couleur-tweak-tips/Smoothie/wiki/Configuring-Smoothie-(recipe))

```ini
[interpolation] # Tries to guess frames in between existing ones to increase FPS
enabled=yes # If you want to interpolate or not
fps=960 # The FPS you wish to interpolate to
speed=medium # What accuracy you want (fast, faster and fastest will take less time, but make worse frames)
tuning=weak # This and 'algorithm' are different ways to make interpolation, check the wiki
algorithm=23
gpu=yes # GPU acceleration

[frame blending] # Converts high FPS footage (e.g 240, 960) to a lower frame rate (e.g 30, 60 for YT) with motion blur
enabled=yes # If you want want it to frame blend or not
fps=60 # The FPS you want it blended down to
intensity=1.27 # 1.0 is what you're used to, more will make a longer kind of "ghoserfz", I love 1.5 @ 60FPS
weighting=equal # How each blur frame's opacity is decided (default is every one of them is equal)

[encoding]
process=ffmpeg # ffmpeg binary name
args=-c:v libx264 -preset slow -crf 15 # You can even add -vf to add any FFmpeg filter!

[misc]
folder= # Override all output videos to a specific folder
deduplication=y # Frame deduplication (useful if you have a tiny little bit of encoding lag)
container=.mp4 # Set this to .MKV to be able to watch the video before it even finishes rendering!
flavors=fruits # Set the value to nothing if you want your rendered suffixes to be '- Smoothie.ext'

[timescale] # Set the speed in/out
in=1
out=1
```
</details>


## Installation

### Windows
To install Smoothie and its dependencies for Windows, run this install script command anywhere:

```powershell
powershell "irm smoothie.ctt.cx|iex"
```
### Linux


For Linux users and those who seek for a manual installation/already have a Python 3.9/VapourSynth, check the [wiki](https://github.com/couleur-tweak-tips/Smoothie/wiki)

## Using Smoothie
You can simply select one multiple videos and right click and of them -> Send To -> Smoothie

using Smoothie from the command line:

``sm "D:\Video\input1.mp4" "D:\Video\input2.mp4" ...``
    Simply give in the path of the videos you wish to queue to smoothie

``sm myrecipe.ini "D:\Video\input1.mp4" "D:\Video\input2.mp4" ...``
    You can also make the first argument be your custom config file's name, it'll look for it in the settings folder

A lot more ways to use it via the CLI are available on the [wiki](https://github.com/couleur-tweak-tips/Smoothie/wiki)


<details>
<summary>Dependencies </summary>

- [Python](https://www.python.org/downloads) (3.9)
- [FFmpeg](https://ffmpeg.org/download.html)
- [VapourSynth x64](https://www.vapoursynth.com) (R54)

VapourSynth plugins
- [FFMS2](https://github.com/FFMS/ffms2)
- [HAvsFunc](https://github.com/HomeOfVapourSynthEvolution/havsfunc)
- [SVPFlow](https://github.com/bjaan/smoothvideo/blob/main/SVPflow_LastGoodVersions.7z)
- [vs-frameblender](https://github.com/couleurm/vs-frameblender)
- [weighting.py](https://github.com/couleur-tweak-tips/Smoothie/blob/master/plugins/weighting.py)
- [filldrops.py](https://github.com/couleur-tweak-tips/Smoothie/blob/master/plugins/filldrops.py)
</details>

