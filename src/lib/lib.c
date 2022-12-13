#include <windows.h>

void SetWndStyle(HWND hwnd, int nIndex, LONG_PTR Style)
{
    SetWindowLongPtr(hwnd, nIndex,
                     GetWindowLongPtr(hwnd, nIndex) &
                         ~(Style));
}