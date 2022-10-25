
# 🧋 Smoothie [WIP]

Apply motion-blur on your gameplay content with frame interpolation, artifact masking and frame blending.
> It is a cross-platform fork of [blur](https://github.com/f0e/blur) rewritten in Python with a focus on ease of use and integration in your existing routine.


### 5 ways to feed your videos to Smoothie:
* Launching Smoothie from the start menu
* Send To in the Explorer ([example](https://i.imgur.com/MnyYgfr.mp4))
* `sm` on the command line, see it's [wiki page](https://github.com/couleur-tweak-tips/Smoothie/wiki)
* [MPV Trimmer](https://files.catbox.moe/t45q4k.mp4)
* One-button script to render and replace videos in your NLE `WIP`

### Differences compared to blur:
```diff
- Preview (Set container to .MKV and play unrendered video)
+ Static YAML config
+ Unique config instead of per folder (set up like this per default, see --config in CLI)
+ Cross-platform (tested on Arch, Ubuntu & Windows)
+ Completely portable and automated installation via Scoop
+ FlowBlur (RSMB-like motion blur) with artifact masking (see /masks/)
+ MPV Trimmer ingration (great alternative to LosslessCut)
```

## Installation

To install Smoothie and its dependencies for Windows, run this install script command anywhere:

```powershell
powershell -noe iex(irm tl.ctt.cx);Get Smoothie
```
🐧 See for Linux [here](https://github.com/couleur-tweak-tips/Smoothie/wiki)

## Configuring Smoothie

The default recipe can be opened from the Run dialog (Windows+R):
![](https://i.imgur.com/P337omt.png)


<details>
<summary> It's default recipe looks like so (comments are only present here) </summary>

> Learn what each setting does on it's [wiki page](https://github.com/couleur-tweak-tips/Smoothie/wiki/Configuring-Smoothie-(recipe))

```yaml
interpolation: # Tries to guess frames in between existing ones to increase FPS
  enabled: yes # If you want to interpolate or not
  fps: 960 # The FPS you wish to interpolate to
  speed: medium # What accuracy you want (fast, faster and fastest will take less time, but make worse frames)
  tuning: weak # This and 'algorithm' are different ways to make interpolation, check the wiki
  algorithm: 23 # Same deal
  use gpu: yes # GPU acceleration

frame blending: # Converts high FPS footage (e.g 240, 960) to a lower frame rate (e.g 30, 60 for YT) with motion blur
  enabled: yes # If you want want it to frame blend or not
  fps: 60 # The FPS you want it blended down to
  intensity: 1.27 # 1.0 is what you're used to, more will make a longer kind of "ghoserfz", I love 1.5 @ 60FPS
  weighting: equal # How each blur frame's opacity is decided (default is every one of them is equal)

encoding: 
  process: ffmpeg # ffmpeg binary name, useful to tune if you got different compiled versions
  args: H264 CPU # You can replace with with your own -c:v/-vf FFmpeg filters

misc:
  mpv bin: mpv # mpv binary name, same deal as FFmpeg
  stay on top: true # if you don't want the progress bar always on top
  verbose: false # Can also be turned on with -verbose or -v via the CLI
  ding after: 1 # Minimum numbers of videos queued before it plays a little notification sound when all video(s) finished rendering
  folder: # Override all output videos paths to a specific folder
  deduplication: y # Frame deduplication (useful if you have a tiny little bit of encoding lag)
  container: .MP4 # Set this to .MKV to be able to watch the video before it even finishes rendering! (You'll need to remux them to .MP4 after to use the video in specific applications)
  prefix: # Empty by default, you can make your apex.mp4 be outputted as SM-apex.mp4
  suffix: detailed # Detailed will say some misc stuff about the settings used on it, can be replaced with your own string
  dedupthreshold: 0 # Turn that to 0.001 if you want frame deduplication like blur's

timescale: # Set the speed in/out, I like out @ 1.03 to speed a liiittle bit to look cool
  in: 1
  out: 1
```
</details>
