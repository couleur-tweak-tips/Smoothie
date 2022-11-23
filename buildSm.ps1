function SetupEnvironment {
    param(
        [Array]$Links,
        $DLFolder,
        $Script
    )
    $LinkPaths = @{}
    ForEach($File in $Links.Keys){
        $LinkPath = (Join-Path $DLFolder $File)
        if (-not(Test-Path $LinkPath)){
            Invoke-WebRequest $Links.$File -OutFile $LinkPath -Verbose
        }
        Set-Variable -Name (Get-Item $LinkPath).BaseName -Value (Get-Item $LinkPath)
    }
    mkdir ("$env:TMP\$()")
    if ($Script.GetType().Name -eq 'ScriptBlock'){
        & $Script -Files $LinkPaths
    }
}
function Get-Release($Repo, $Pattern){
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
    'vsA6.zip'   = Get-Release AmusementClub/vapoursynth-classic release-x64.zip
    'akexpr.7z'  = Get-Release AkarinVS/vapoursynth-plugin akarin-release-lexpr-amd64-v*.7z
    'py3110.exe' = 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe'
    'getpip.py'  = 'https://bootstrap.pypa.io/get-pip.py'
    'svp.7z'     = 'https://github.com/bjaan/smoothvideo/blob/main/SVPflow_LastGoodVersions.7z?raw=true'
    'lsmash.zip' = 'https://github.com/AkarinVS/L-SMASH-Works/releases/download/vA.3j/release-x86_64-cachedir-tmp.zip'
    'mvtools.7z' = Get-Release dubhater/vapoursynth-mvtools vapoursynth-mvtools-v*-win64.7z
    'remap.zip'  = Get-Release Irrational-Encoding-Wizardry/Vapoursynth-RemapFrames Vapoursynth-RemapFrames-v*-x64.zip
    'vsfbd.dll'  = Get-Release couleurm/vs-frameblender  vs-frameblender-*.dll
    'rife'       = Get-Release HomeOfVapourSynthEvolution/VapourSynth-RIFE-ncnn-Vulkan RIFE-r*-win64.7z

} -Script {
    $Pips = @(
        'vsutil'
        'yaspin'
        (Get-Release SubNerd/PyTaskbar PyTaskbarProgress-*-py3-none-any.whl)

    )
    $smDir = Get-Item "D:\GitHub\Smoothie" -ErrorAction Stop
    Expand-Archive $vsA6 -DestinationPath ./VS/
    ForEach($Directory in @('VapourSynth_portable.egg-info','doc')){
        Remove-Item "./VS/$Directory" -Force -Recurse -Verbose -Confirm
    }
    dark -nologo -x (Conver-Path ./_/) $py3110 | Out-Null

    @('path', 'pip', 'dev', 'doc', 'launcher', 'test', 'tools', 'tcltk') |
        ForEach-Object {Remove-Item "./_/AttachedContainer/$_.msi"}

    Get-ChildItem "./_/AttachedContainer/*.msi" |
        ForEach-Object {
                "Extracing $($_.Name)"
                lessmsi x $_ (convert-path  ./_/) | Out-Null
        }

    Move-Item ./_/SourceDir/* ./VS/

    # @(
    #     "/Lib/pydoc_data/"
    #     "/Lib/ensurepip/"
    #     "/Lib/unittest/"
    #     "/Lib/venv/"
    #     "/Lib/2to3/"
    #     "NEWS.txt"
    # ) | ForEach-Object {
    #   Remove-Item "./$_" -Recurse -Force
    # }

    mkdir ./Smoothie

    Copy-Item @(
        "$smDir\masks\"
        "$smDir\src\"
        "$smDir\models\"
        "$smDir\recipe.HELLLLLLLLOOOOOOOOOOOHELLLLLLLLOOOOOOOOOOOHELLLLLLLLOOOOOOOOOOOHELLLLLLLLOOOOOOOOOOO\"
    ) -Destination ./Smoothie

    Move-Item ./Smoothie/LICENSE ./Smoothie/src/
    Get-ChildItem . -Recurse -Include "__pycache__" | Remove-Item -Force -Recurse
    Rename-Item -Path ./VS/ -NewName VapourSynth
    Compress-Archive -Path ./Smoothie, ./VapourSynth/ -DestinationPath ./Smoothie-$ver.zip
}