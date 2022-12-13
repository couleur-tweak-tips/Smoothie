{.compile: "lib.c".}
import winim/[lean, shell]
import strutils

SetProcessDPIAware()

proc openFileDialog*(title: cstring = "Open", filters: cstring = "All Files (*.*)or*.*", dir: cstring = "."): cstring {.exportc, dynlib.} =
    var 
        opf: OPENFILENAME
        buf = T(65536)
        fpd, fps: string
        fpsseq: seq[string]

    opf.lStructSize = sizeof(OPENFILENAME).DWORD
    opf.hwndOwner = GetConsoleWindow()
    opf.lpstrTitle = title
    opf.lpstrFilter = ("$1\0" % $filters).replace("or", "\0")
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

proc GetDpiForSystem(): UINT {.winapi, stdcall, dynlib: "user32", importc.}
proc SetWndStyle(hwnd: HWND, nIndex: int32, style: LONG_PTR): void {.importc.}

proc setSMWndParams*(ontop: bool, borderless: bool, width: int, height: int): void {.exportc, dynlib.} =
    let 
        s =  GetDpiForSystem() / 96
        hwnd = GetConsoleWindow()
        cx = int32(float(width) * s)
        cy = int32(float(height) * s)
    var 
        mi: MONITORINFO
        hwndpos = 0
    mi.cbSize = sizeof(mi).DWORD
    if borderless:
        SetWndStyle(hwnd, GWL_STYLE, WS_OVERLAPPEDWINDOW)
        SetWndStyle(hwnd, GWL_EXSTYLE, WS_EX_DLGMODALFRAME or WS_EX_COMPOSITED or WS_EX_OVERLAPPEDWINDOW or WS_EX_LAYERED or WS_EX_STATICEDGE or WS_EX_TOOLWINDOW or WS_EX_APPWINDOW)
    if ontop: hwndpos = HWND_TOPMOST
    GetMonitorInfo(MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST), &mi)
    SetWindowPos(hwnd, hwndpos, mi.rcMonitor.right-cx, mi.rcmonitor.bottom-(cy+40), cx, cy, SWP_FRAMECHANGED)
