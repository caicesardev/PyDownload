$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$appDirectory = Join-Path $projectRoot "app"
$distDirectory = Join-Path $projectRoot "dist"
$buildDirectory = Join-Path $projectRoot "build"
$version = (Select-String -Path (Join-Path $appDirectory "constants.py") -Pattern 'VERSION = "(.+)"').Matches[0].Groups[1].Value
$bundleDirectory = Join-Path $distDirectory "PyDownload"
$archivePath = Join-Path $distDirectory "PyDownload-$version-windows-x64.zip"
$keptLocales = @("en-US", "es", "es-419")

function Remove-UnusedQtFiles([string] $qtDirectory) {
    Remove-Item (Join-Path $qtDirectory "qml") -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem (Join-Path $qtDirectory "resources") -Include "*.debug.*", "qtwebengine_devtools_resources*" -Recurse |
        Remove-Item -Force
    Get-ChildItem (Join-Path $qtDirectory "translations\qtwebengine_locales") -Filter "*.pak" |
        Where-Object { $keptLocales -notcontains $_.BaseName } |
        Remove-Item -Force
    Get-ChildItem (Join-Path $qtDirectory "translations") -Filter "*.qm" |
        Where-Object { $_.BaseName -notmatch "_(es|en)$" } |
        Remove-Item -Force
}

python -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --name PyDownload `
    --icon (Join-Path $projectRoot "res\images\app.ico") `
    --paths $appDirectory `
    --collect-data imageio_ffmpeg `
    --distpath $distDirectory `
    --workpath $buildDirectory `
    --specpath $buildDirectory `
    (Join-Path $appDirectory "main.py")
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed with exit code $LASTEXITCODE"
}

Remove-UnusedQtFiles (Join-Path $bundleDirectory "_internal\PySide6")

$denoExecutable = python -c "import deno; print(deno.find_deno_bin())"
Copy-Item $denoExecutable $bundleDirectory
Copy-Item (Join-Path $projectRoot "LICENSE") $bundleDirectory

Compress-Archive -Path $bundleDirectory -DestinationPath $archivePath -Force
Write-Host "Build ready: $archivePath"
