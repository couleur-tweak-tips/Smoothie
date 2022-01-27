@echo off
py -OO -m nuitka --onefile --follow-imports --include-plugin-files=Modules\config.py --include-plugin-files=Modules\encoder.py --include-plugin-files=Modules\vspipe.py --include-plugin-files=Modules\render.py main.py --output-dir="%TEMP%" -o "Smoothie.exe"
timeout 5