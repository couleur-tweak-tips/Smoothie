
<h1 align="center">
    <img alt="Smoothie" src="https://i.imgur.com/K20ymPM.png" width="100" />
    <br>
  Smoothie
</h1>
<p align="center">
Apply motion-blur efficiently on gameplay footage, however you want it.
</p>
<h4 align="center">
  <a href="https://github.com/couleur-tweak-tips/Smoothie/wiki">Docs</a> |
  <a href="https://www.youtube.com/playlist?list=PLrsLsEZL_o4M_yTqZGwN5cM5ZxJTqkWkZ">Demo Playlist</a> |
  <a href="https://ctt.cx">Website</a>
</h4>
<p align="center">
    <a href="https://discord.com/invite/aPVMJy78Pa">
        <img src="https://img.shields.io/discord/774315187183288411?color=7389D8&labelColor=6A7EC2&label=Discord&logo=discord&logoColor=white alt="Discord" />
    </a>
    <a href="https://github.com/couleur-tweak-tips/TweakList/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/couleur-tweak-tips/TweakList.svg" alt="License" />
    </a>
</p>

---



Smoothie is a cross-platform fork of [blur](https://github.com/f0e/blur) rewritten in Python, it is useable through the CLI but there's tons of wrappers so you never have to open and type anything yourself:


### 5 wrappers for feeding footage to Smoothie:
* Launching Smoothie from the start menu to queue whole folders
* "Send To" option in Explorer ([example](https://i.imgur.com/MnyYgfr.mp4))
* `sm` on the command line, see [docs](https://github.com/couleur-tweak-tips/Smoothie/wiki/%F0%9F%8E%B9-Using-Smoothie-from-the-command-line)
* Cut and export on MPV via my sister project [suckless-cut](https://github.com/couleur-tweak-tips/suckless-cut)
* One-button script to render and replace videos in your video-editor `WIP for VEGAS Pro`


### Differences compared to blur:

- Haven't bothered adding blur's "color grading" options feel free to PR
- No drag & drop interace (conhost does not support multiple files at once)
- Instead there's a file picker, which support whole folders
- Static YAML config (instead of per folder)
- FlowBlur option (RSMB-like motion blur) with artifact masking (see /masks/)
- `-override` argument to change on the fly some recipe setting(s), useful in shortcuts!!
- Linux: tested on Arch & Ubuntu, should work where Python & VapourSynth do
- Windows: Completely portable and automated installation via Scoop


## Installation

To automatically install Smoothie and its [dependencies](https://github.com/couleur-tweak-tips/Smoothie/wiki/%F0%9F%93%A6-Bundling-Smoothie-yourself) for Windows, run this command in PowerShell:

```powershell
iex(irm tl.ctt.cx); Get Smoothie
```
[This](https://github.com/couleur-tweak-tips/TweakList/blob/master/modules/Installers/Get.ps1#L71) will do the following for you:

* Set up Scoop, a portable package manager
* Install FFmpeg and add it to PATH if needed
* Install Smoothie, add it to PATH (`sm`), set up shortcuts and prompt you for misc plugins

If you don't want to run the installation script can also grab the latest portable zip from the repo's releases [here](https://github.com/couleur-tweak-tips/Smoothie/releases) (though be aware you'll need to set up shortcuts yourself)

🐧 See installation instructions for Linux [here](https://github.com/couleur-tweak-tips/Smoothie/wiki)

### Uninstalling Scoop & Smoothie

You should find Scoop (per default) in your `%USERPROFILE%` folder, if you want to delete Smoothie specificly it's in `...\scoop\apps\smoothie`


## Configuring Smoothie (recipe 😋)

If installed with Scoop, the main (default) recipe can be opened from the Run dialog (Windows+R):

![](https://i.imgur.com/P337omt.png)


You can learn what each setting does on it's [wiki page](https://github.com/couleur-tweak-tips/Smoothie/wiki/Configuring-Smoothie-(recipe))



## The default recipe

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
  process: ffmpeg # ffmpeg's executable path
  args: H264 CPU # You can replace with with your own -c:v/-vf FFmpeg filters

misc:
  mpv bin: mpv # mpv executable path, same deal as FFmpeg
  stay on top: true # if you don't want the progress bar always on top
  verbose: false # Can also be turned on with -verbose/-v on the CLI
  ding after: 1 # Minimum numbers of videos queued before it plays a little notification sound when all video(s) finished rendering
  folder: # Redirect all output videos to a specific folder
  deduplication: y # Frame deduplication (useful if you have a tiny little bit of encoding lag)
  container: .MP4 # Set this to .MKV to be able to watch the video before it even finishes rendering! (You'll need to remux them to .MP4 after to use the video in specific applications)
  prefix: # Empty by default, you can make your apex.mp4 be outputted as SM-apex.mp4
  suffix: detailed # Detailed will say some misc stuff about the settings used on it, can be replaced with your own string
  dedupthreshold: 0 # Turn that to 0.001 if you want frame deduplication like blur's

timescale: # Set the speed in/out, I like out @ 1.03 to speed a liiittle bit to look cool
  in: 1
  out: 1
```
