### Info
This library just provides Smoothie with a `File Dialog` and `Always On Top` support.

Currently this library only supports `Windows` at the moment.

### Build
1. Install Nim using: https://github.com/dom96/choosenim      
    > Recommended: Run the installer, 2~3 times to ensure all dependencies and files are correctly installed.
2. Install `winim`:
    ```
    nimble install winim
    ```
3. Open a `cmd | powershell` window in `src/lib`.
4. Run the following command:
    ```ps
    nim c -d:release -d:strip --opt:size --app:lib lib.nim
    ```
    > Optional: Compress using UPX for a smaller footprint!        
    `upx -9 lib.dll`
5. Once the command finishes executing, you will get a `lib.dll` file.
#### Testing
Check if the compiled library works without any issues by running the `libtest.py` file.