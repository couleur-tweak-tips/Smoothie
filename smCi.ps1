#requires -version 7.2 #! Needs you to install pwsh 7, does not come with Windows!
using namespace System.Net.Http # Used to download
param(
    [switch]$UPX, # Compress with UPX
    [switch]$Strip, # Remove unecessary components from Python runtime
    [switch]$BatLauncher, # Include simple batch files
    [version]$ver # version to name zip
)

$ErrorActionPreference = 'Stop'
$smDir = Get-Item "D:\GitHub\Smoothie" -ErrorAction Stop

function SetupEnvironment {
    param(
        [Array]$Links,
        $DLFolder = "$env:TMP\smDeps",
        $BuildDir = "$env:TMP\smBuild",
        $Script
    )

    if (-not (Test-Path $DLFolder)){
        New-Item -ItemType Directory -Path $DLFolder -ErrorAction Stop
    }

    if (-not (Test-Path $BuildDir)){
        New-Item -ItemType Directory -Path $BuildDir -ErrorAction Stop
    }


    $jobs = @()
    ForEach($File in $Links.Keys){

        $LinkPath = (Join-Path $DLFolder $File)

        if (-not(Test-Path $LinkPath)){

            $URL = if ($Links.$File -is [Hashtable]){

                $Parameters = $Links.$File
                Get-Release @Parameters
            }else {
                $Links.$File
            }
            $table = @{
                Uri = $URL
                Outfile = (Join-Path $DLFolder $File)
            }
            Write-Warning "Downloading from $($table.uri)"
            $jobs += Start-ThreadJob -Name $File -ScriptBlock {
                $params = $using:table
                
                Invoke-WebRequest @params -Verbose
            }
        }
    }
    
    Get-ChildItem $DLFolder | ForEach-Object {
        Set-Variable -Name $_.BaseName -Value $_
    }

    

    Push-Location $BuildDir

    if ($Script -is [ScriptBlock]){
        & $Script
    }

    Pop-Location
}
function Get-Release{
    param(
        $Repo, # Username or organization/Repository
        $Pattern # Wildcard pattern
    )
    Write-Host "Getting $Pattern from $Repo"
    $Latest = (Invoke-RestMethod https://api.github.com/repos/$Repo/releases/latest -ErrorAction Stop).assets.browser_download_url |
        Where-Object {$_ -Like "*$Pattern"}

    if ($Latest.Count -gt 1){
        $Latest
        throw "Multiple patterns found"
    }
    return $Latest
}

SetupEnvironment -Links @{
    'py3109.exe' = 'https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe'
    'getpip.py'  = 'https://bootstrap.pypa.io/get-pip.py'
    'svp.7z'     = 'https://github.com/bjaan/smoothvideo/blob/main/SVPflow_LastGoodVersions.7z?raw=true'
    'vsA6.zip'   = @{ Repo = "AmusementClub/vapoursynth-classic"; Pattern = "release-x64.zip"}
    'akexpr.7z'  = "https://github.com/AkarinVS/vapoursynth-plugin/releases/download/v0.96/akarin-release-lexpr-amd64-v0.96b.7z"#@{ Repo = "AkarinVS/vapoursynth-plugin"; Pattern = "akarin-release-lexpr-amd64-v*.7z"}
    'lsmash.zip' = "https://github.com/AkarinVS/L-SMASH-Works/releases/download/vA.3k/release-x86_64-cachedir-tmp.zip"
    'mvtools.7z' = @{ Repo = "dubhater/vapoursynth-mvtools"; Pattern = "vapoursynth-mvtools-v*-win64.7z"}
    'remap.zip'  = @{ Repo = "Irrational-Encoding-Wizardry/Vapoursynth-RemapFrames"; Pattern = "Vapoursynth-RemapFrames-v*-x64.zip"}
    # 'vsfbd.dll'= @{Repo = "couleurm/vs-frameblender" ; Pattern="vs-frameblender-*.dll"}
    'rife.7z'    = @{Repo = "HomeOfVapourSynthEvolution/VapourSynth-RIFE-ncnn-Vulkan"; Pattern="RIFE-r*-win64.7z"}

} -Script {

    Set-Location $env:TMP\smShip
    Write-Warning "Setting up dirs"
    mkdir ./VapourSynth | Out-null
    $VS = Get-Item ./VapourSynth
    mkdir ./_/ | Out-Null
    $Temp = Get-Item ./_/

    Write-Warning "Python"

    dark -nologo -x $Temp $py3109 | Out-Null

    @('path', 'pip', 'dev', 'doc', 'launcher', 'test', 'tools', 'tcltk') |
        ForEach-Object {Remove-Item "$Temp/AttachedContainer/$_.msi"}

    Get-ChildItem "$Temp/AttachedContainer/*.msi" |
        ForEach-Object {
                "Extracing $($_.Name)"
                lessmsi x $_ $Temp | Out-Null
        }

    Copy-Item $Temp/SourceDir/* $VS -ErrorAction Ignore -Recurse
    Expand-Archive $vsA6 -DestinationPath $VS -Force
    Write-Warning "Copying Smoothie"
    mkdir ./Smoothie

    Copy-Item @(
        "$smDir\masks\"
        "$smDir\src\"
        "$smDir\models\"
        "$smDir\LICENSE"
        "$smDir\recipe.yaml"
    ) -Destination ./Smoothie -Recurse

    Write-Warning "VS Plugins"
    Push-Location $VS/vapoursynth64/plugins
    $null = 7z e -y $svp -r svpflow1_vs.dll svpflow2_vs.dll .
    $akexpr, $lsmash, $mvtools, $rife, $remap | 
        ForEach-Object { 7z x $_ }

    Pop-Location
    Write-Warning "Pip"
    $py = Get-Item "$VS/python.exe"

    & $py $getpip --no-warn-script-location

    @(
        'yaspin'
        'pyyaml'
        "https://github.com/SubNerd/PyTaskbar/releases/download/0.0.8/PyTaskbarProgress-0.0.8-py3-none-any.whl"#(Get-Release SubNerd/PyTaskbar PyTaskbarProgress-*-py3-none-any.whl)
    ) | ForEach-Object {
        & $py -m pip install $_
    }
    & $py -m pip install vsutil --no-dependencies

    Write-Warning "Finalizing"
    Move-Item ./Smoothie/LICENSE ./Smoothie/src/
    Set-Content ./Smoothie/src/lastargs.txt -Value "" -Force
    Get-ChildItem ./Smoothie/masks/*.ffindex | Remove-Item
    Get-ChildItem . -Recurse -Include "__pycache__" | Remove-Item -Force -Recurse
    if ($UPX){
        Write-Warning "UPX Compression"
        Get-ChildItem $VS/vapoursynth64/ -Recurse -Include *.dll |
            Where-Object Length -gt 1MB | #
            ForEach-Object { upx.exe -q -9 $PSItem}
    }
    if ($Strip){
        Write-Warning "Stripping"
        @(
            "/Lib/site-packages/pip"
            "/Lib/site-packages/setuptools"
            "/Lib/site-packages/wheel"
            "/doc/"
            "/Scripts/"
            "/Lib/pydoc_data/"
            "/Lib/ensurepip/"
            "/Lib/unittest/"
            "/Lib/venv/"
            "/Lib/2to3/"
            "/NEWS.txt"
        ) | ForEach-Object {
            (Join-Path $VS $_)
        } | ForEach-Object {
            if (Test-Path $_){
                Remove-Item $_ -Recurse -Force -Verbose
            }
        }
    }
    if ($BatLauncher){
        Write-Warning "Bat Launcher"
        Set-Content ./Smoothie/Smoothie-Launcher.cmd @"
@echo off
title Smoothie's simple Batch Launcher
"%CD%\..\VapourSynth\python.exe" "%CD%\src\main.py" -cui
"@
    Set-Content ./Smoothie/Smoothie-Launcher-Verbose.cmd @"
@echo off
if "check" == "%~1check" (
    echo Drag a video on the file!
    pause>nul
    exit
)
title Smoothie's simple Batch Launcher [VERBOSE]
cd /D "%~dp0"
"%CD%\..\VapourSynth\python.exe" "%CD%\src\main.py" -v -i "%~1"
if %ERRORLEVEL% == 0 (exit) else (pause)
"@
    }
    7z a "Smoothie-$ver`.7z" .\Smoothie\ .\VapourSynth\ -t7z -mx=8 -sae -- 
 # Compress-Archive -Path ./Smoothie, ./VapourSynth/ -DestinationPath ./Smoothie-$ver`.zip



}