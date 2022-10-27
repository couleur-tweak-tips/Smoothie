# Contain Nim functions for Smoothie.
import winlean, os, strutils

type TOPENFILENAME = object
    lStructSize: DWORD
    hwndOwner: HANDLE
    hInstance: HANDLE
    lpstrFilter: cstring
    lpstrCustomFilter: cstring
    nMaxCustFilter: DWORD
    nFilterIndex: DWORD
    lpstrFile: cstring
    nMaxFile: DWORD
    lpstrFileTitle: cstring
    nMaxFileTitle: DWORD
    lpstrInitialDir: cstring
    lpstrTitle: cstring
    flags: DWORD
    nFileOffset: int16
    nFileExtension: int16
    lpstrDefExt: cstring
    lCustData: ByteAddress
    lpfnHook: pointer
    lpTemplateName: cstring
    pvReserved: pointer
    dwreserved: DWORD
    flagsEx: DWORD

proc getOpenFileName(para1: ptr TOPENFILENAME): WINBOOL{.stdcall,
    dynlib: "comdlg32", importc: "GetOpenFileNameA".}

proc GetForegroundWindow(): HANDLE {.stdcall, dynlib: "user32", importc:
    "GetForegroundWindow".}

proc SetWindowPos(hwnd: HANDLE, hWndInsertAfter: HANDLE, x: int, y: int,
    cx: int, cy: int, uFlags: int32): void {.stdcall, dynlib: "user32",
    importc: "SetWindowPos".}

proc setSMOnTop* : void {. exportc, dynlib .} =
    SetWindowPos(GetForegroundWindow(), -1, 0, 0, 1000, 60, 0)

proc setSMDebug* : void {. exportc, dynlib .} =
    SetWindowPos(GetForegroundWindow(), -1, 0, 0, 1000, 720, 0)

proc filedialog* (title: cstring = "Open", filters: cstring = "", dir: cstring = ""): cstring {. exportc, dynlib .} =
    # "C++ Files\0*.cpp;\0Header Files\0*.h\0\0"
    var
        opf: TOPENFILENAME
        buf: array[0..2047*4, char]
        files: seq[string]
        path: string
    opf.lStructSize = sizeof(opf).int32
    if dir.len > 0:
        opf.lpstrInitialDir = dir
    opf.lpstrTitle = title
    opf.lpstrFilter = cstring(($filters).replace("|", "\0") & "All Files (*.*)\0*.*\0")
    opf.flags = 0x00001000 or 0x00000200 or 0x00080000
    opf.lpstrFile = addr buf
    opf.nMaxFile = sizeof(buf).int32
    var res = getOpenFileName(addr(opf))
    if res != 0:
        var
            i = 0
            s: string
            path = ""
        while buf[i] != '\0':
            add(path, buf[i])
            inc(i)
        inc(i)
        if buf[i] != '\0':
            while true:
                s = ""
                while buf[i] != '\0':
                    add(s, buf[i])
                    inc(i)
                files.add(s)
                inc(i)
                if buf[i] == '\0': break
            for i in 0..files.len-1: files[i] = os.joinPath(path, files[i])
    else: files.add(path)
    return cstring(files.join("\n"))