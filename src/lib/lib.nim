import winim/[lean, shell]
import strutils

proc openFileDialog*(title: cstring = "Open", filters: cstring = "All Files (*.*)|*.*", dir: cstring = "."): cstring {.exportc, dynlib.} =
    var 
        opf: OPENFILENAME
        buf = T(65536)
        fpd, fps: string
        fpsseq: seq[string]

    opf.lStructSize = sizeof(OPENFILENAME).DWORD
    opf.lpstrTitle = title
    opf.lpstrFilter = ("$1\0" % $filters).replace("|", "\0")
    opf.lpstrInitialDir = dir
    opf.lpstrFile = &buf
    opf.nMaxFile = len(buf).DWORD
    opf.Flags = OFN_EXPLORER or OFN_ALLOWMULTISELECT or OFN_LONGNAMES
    GetOpenFileName(opf)

    fpsseq = string(buf).strip(chars={'\0'}).split("\0\0")
    fpd = fpsseq[0].replace("\0", "")
    if len(fpsseq) != 1:
        for i in fpsseq[1..^1]:
            fps = fps & "$1\\$2\n" % [fpd, i.replace("\0", "")]
    else: fps = fpd & "\n"
    return cstring(fps)

proc setSmTop*(debug: bool): void {.exportc, dynlib .}=
    var cy: int32 = 60
    if debug: cy = 720
    SetWindowPos(GetForegroundWindow(), -1, 0, 0, 1000, cy, 0)

proc setSmDebug*(debug: bool): void {.exportc, dynlib .}=
    var cy: int32 = 60
    if debug: cy = 720
    SetWindowPos(GetForegroundWindow(), -1, 0, 0, 1000, cy, 0)
