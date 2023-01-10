{.compile: "lib.c".}
import winim/[lean, shell]
import strutils

SetProcessDPIAware()

proc openFileDialog*(title: cstring = "Open", filters: cstring = "All Files (*.*)|*.*", dir: cstring = "."): cstring {.exportc, dynlib.} =
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

proc setSMWndParams*(ontop: bool, borderless: bool, width: int, height: int, pos: int = 1): void {.exportc, dynlib.} =
    let 
        s =  GetDpiForSystem() / 96
        hwnd = GetConsoleWindow()
        cx = (float(width) * s).LONG
        cy = (float(height) * s).LONG
        hout = GetStdHandle(STD_OUTPUT_HANDLE)

    var 
        mi: MONITORINFO
        ci: CONSOLE_SCREEN_BUFFER_INFO
        buf: COORD
        hwndpos = 0
        x, y: LONG

    mi.cbSize = sizeof(mi).DWORD
    GetMonitorInfo(MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST), &mi)

    if ontop: hwndpos = HWND_TOPMOST
    if borderless:
        SetWndStyle(hwnd, GWL_STYLE, WS_OVERLAPPEDWINDOW)
        SetWndStyle(hwnd, GWL_EXSTYLE, WS_EX_DLGMODALFRAME or WS_EX_COMPOSITED or WS_EX_OVERLAPPEDWINDOW or WS_EX_LAYERED or WS_EX_STATICEDGE or WS_EX_TOOLWINDOW or WS_EX_APPWINDOW)
        SetWindowPos(hwnd, 0, 0, 0, 0, 0, SWP_NOACTIVATE or SWP_NOMOVE or SWP_NOREPOSITION)     
    case pos:
        of 1:
            x = mi.rcMonitor.left
            y = mi.rcMonitor.top
        of 2:
            x = mi.rcMonitor.left 
            y = mi.rcMonitor.bottom - (cy + 40)
        of 3:
            x = mi.rcMonitor.right - cx
            y = mi.rcMonitor.top
        of 4:
           x = mi.rcMonitor.right - cx 
           y = mi.rcMonitor.bottom - (cy + 40)
        else:
            discard

    SetWindowPos(hwnd, hwndpos, x, y, cx, cy, 0)
    GetConsoleScreenBufferInfo(hout, &ci)

    # Minimum Buffer sizes for removing the scrollbar.
    if borderless and width >= 185 and height >= 20:
        buf.X = ci.dwSize.X
        buf.Y = (ci.srWindow.Bottom - ci.srWindow.Top) + 1
        SetConsoleScreenBufferSize(hout, buf)


