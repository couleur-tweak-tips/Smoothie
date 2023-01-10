# Pre-Renderer for VEGAS Pro

## ⚠ WORK IN PROGRESS

You can export your timeline full of laggy high FPS clips to Smoothie and let it render them down to a more reasonable framerate and replace them all on your timeline, this has two majors benefits:
- Save considerable amounts of rendering time, Smoothie is much (much) faster than VEGAS' resampling
- Reduce preview lag significantly, since you're frame blending your clips down to 30, 60 FPS (or 120 if you're doing some velocity)

#### Installation

If you have VEGAS Pro installed correctly and used the Scoop installer, it should already have done the first step for you 👍

1. The "Pre-Renderer" comes as a C# (.cs) script you can put in a folder named `Vegas Script Menu` in your Documents folder for VEGAS Pro to locate it
2. You can run it by heading to ``Tools`` -> ``Scripting`` -> ``Smoothie - Pre Renderer`` or add it to your toolbar for easy access like so (start by double left-clicking to the right of your toolbar):

![](https://i.imgur.com/iZvVwoP.gif)